"""Shared, dependency-free lease for exclusive local model resources.

The metadata file is protected by a separate OS-level guard lock. All
cooperating writers take that guard before reading, replacing, or deleting
metadata, so an expired lease can be reclaimed without deleting a newer
process's active lease.
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
import errno
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import threading
import time
import uuid
from typing import Callable, Iterator, Optional, Sequence


SCHEMA_VERSION = 1
DEFAULT_RESOURCE_ID = "local-llm"
DEFAULT_TTL_SECONDS = 300.0
DEFAULT_WAIT_SECONDS = 3600.0
DEFAULT_POLL_SECONDS = 0.2


class LeaseError(RuntimeError):
    """Base class for lease failures."""


class LeaseBusyError(LeaseError):
    """Raised when an active lease remains held until the wait timeout."""


class LeaseLockError(LeaseError):
    """Raised when the operating-system guard lock cannot be used."""


class LeaseCorruptError(LeaseError):
    """Raised when lease metadata exists but is invalid."""


class LeaseOwnershipError(LeaseError):
    """Raised when a caller tries to change another owner's lease."""


class LeaseExpiredError(LeaseError):
    """Raised when a lease can no longer be renewed."""


class LeaseBlockedError(LeaseError):
    """Raised when a workspace blocker makes local model work unavailable."""


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def default_lease_root() -> Path:
    configured = os.environ.get("LOCAL_MODEL_LEASE_DIR")
    if configured:
        return Path(configured)
    repos_root = os.environ.get("ENGINEERING_REPOS_ROOT")
    if repos_root:
        return Path(repos_root) / ".runtime" / "local-model-leases"
    return Path.home() / ".local" / "state" / "engineering-workspace" / "local-model-leases"


def _iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).isoformat(timespec="milliseconds")


def _parse_iso(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return parsed.astimezone(dt.timezone.utc)


def _resource_key(resource_id: str) -> str:
    if not resource_id or not resource_id.strip():
        raise ValueError("resource_id must not be empty")
    digest = hashlib.sha256(resource_id.encode("utf-8")).hexdigest()[:20]
    return f"resource-{digest}"


@dataclasses.dataclass(frozen=True)
class LeaseMetadata:
    schema_version: int
    resource_id: str
    lease_id: str
    owner: str
    workload: str
    pid: int
    hostname: str
    acquired_at: str
    renewed_at: str
    expires_at: str
    ttl_seconds: float

    @classmethod
    def from_dict(cls, data: object) -> "LeaseMetadata":
        if not isinstance(data, dict):
            raise LeaseCorruptError("lease metadata must be a JSON object")
        try:
            metadata = cls(**data)
            _parse_iso(metadata.acquired_at)
            _parse_iso(metadata.renewed_at)
            _parse_iso(metadata.expires_at)
        except (TypeError, ValueError, KeyError) as exc:
            raise LeaseCorruptError(f"invalid lease metadata: {exc}") from exc
        if metadata.schema_version != SCHEMA_VERSION:
            raise LeaseCorruptError(
                f"unsupported lease schema {metadata.schema_version}; expected {SCHEMA_VERSION}"
            )
        if not metadata.resource_id or not metadata.lease_id or not metadata.owner:
            raise LeaseCorruptError("resource_id, lease_id, and owner are required")
        if metadata.ttl_seconds <= 0:
            raise LeaseCorruptError("ttl_seconds must be positive")
        return metadata

    def as_dict(self) -> dict:
        return dataclasses.asdict(self)


class _GuardLock:
    def __init__(
        self,
        path: Path,
        timeout_seconds: float,
        poll_seconds: float = 0.05,
        monotonic: Callable[[], float] = time.monotonic,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        self.path = path
        self.timeout_seconds = max(0.0, timeout_seconds)
        self.poll_seconds = max(0.01, poll_seconds)
        self.monotonic = monotonic
        self.sleeper = sleeper
        self.handle = None

    @staticmethod
    def _is_busy_error(exc: OSError) -> bool:
        return (
            isinstance(exc, BlockingIOError)
            or exc.errno in {errno.EACCES, errno.EAGAIN}
            or getattr(exc, "winerror", None) in {33, 36}
        )

    def _try_lock(self) -> None:
        assert self.handle is not None
        self.handle.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(self.handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

    def __enter__(self) -> "_GuardLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.handle = self.path.open("a+b")
            self.handle.seek(0, os.SEEK_END)
            if self.handle.tell() == 0:
                self.handle.write(b"\0")
                self.handle.flush()
                os.fsync(self.handle.fileno())
        except OSError as exc:
            raise LeaseLockError(f"cannot open lease guard {self.path}: {exc}") from exc

        deadline = self.monotonic() + self.timeout_seconds
        while True:
            try:
                self._try_lock()
                return self
            except OSError as exc:
                if not self._is_busy_error(exc):
                    self.handle.close()
                    self.handle = None
                    raise LeaseLockError(f"cannot lock lease guard {self.path}: {exc}") from exc
                remaining = deadline - self.monotonic()
                if remaining <= 0:
                    self.handle.close()
                    self.handle = None
                    raise LeaseLockError(
                        f"timed out locking lease guard {self.path} "
                        f"after {self.timeout_seconds:.3f}s"
                    ) from exc
                self.sleeper(min(self.poll_seconds, remaining))

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self.handle is None:
            return
        try:
            self.handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(self.handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
        except OSError as unlock_error:
            if exc is None:
                raise LeaseLockError(
                    f"cannot unlock lease guard {self.path}: {unlock_error}"
                ) from unlock_error
        finally:
            self.handle.close()
            self.handle = None


class LeaseManager:
    def __init__(
        self,
        root: Optional[Path] = None,
        *,
        clock: Callable[[], dt.datetime] = utc_now,
        monotonic: Callable[[], float] = time.monotonic,
        sleeper: Callable[[float], None] = time.sleep,
        availability_check: Optional[Callable[[], Optional[str]]] = None,
    ) -> None:
        self.root = Path(root) if root is not None else default_lease_root()
        self.clock = clock
        self.monotonic = monotonic
        self.sleeper = sleeper
        self.availability_check = availability_check

    def _ensure_available(self) -> None:
        if self.availability_check is None:
            return
        reason = self.availability_check()
        if reason:
            raise LeaseBlockedError(f"local model resource is blocked: {reason}")

    def _paths(self, resource_id: str) -> tuple[Path, Path]:
        key = _resource_key(resource_id)
        return self.root / f"{key}.json", self.root / f"{key}.guard"

    def _guard(self, resource_id: str, timeout_seconds: float) -> _GuardLock:
        _, guard_path = self._paths(resource_id)
        return _GuardLock(
            guard_path,
            timeout_seconds,
            monotonic=self.monotonic,
            sleeper=self.sleeper,
        )

    def _read(self, resource_id: str) -> Optional[LeaseMetadata]:
        lease_path, _ = self._paths(resource_id)
        try:
            raw = lease_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise LeaseLockError(f"cannot read lease metadata {lease_path}: {exc}") from exc
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LeaseCorruptError(f"invalid JSON in lease metadata {lease_path}: {exc}") from exc
        metadata = LeaseMetadata.from_dict(data)
        if metadata.resource_id != resource_id:
            raise LeaseCorruptError(
                f"lease metadata resource mismatch: {metadata.resource_id!r} != {resource_id!r}"
            )
        return metadata

    def _write(self, metadata: LeaseMetadata) -> None:
        lease_path, _ = self._paths(metadata.resource_id)
        lease_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = lease_path.with_name(
            f".{lease_path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp"
        )
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        try:
            fd = os.open(str(temp_path), flags, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                json.dump(metadata.as_dict(), handle, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, lease_path)
        except OSError as exc:
            with contextlib.suppress(OSError):
                temp_path.unlink()
            raise LeaseLockError(f"cannot atomically write lease {lease_path}: {exc}") from exc

    @staticmethod
    def _is_expired(metadata: LeaseMetadata, now: dt.datetime) -> bool:
        return _parse_iso(metadata.expires_at) <= now.astimezone(dt.timezone.utc)

    def status(self, resource_id: str) -> Optional[LeaseMetadata]:
        with self._guard(resource_id, 2.0):
            return self._read(resource_id)

    def acquire(
        self,
        resource_id: str,
        owner: str,
        workload: str,
        *,
        ttl_seconds: float = DEFAULT_TTL_SECONDS,
        wait_seconds: float = DEFAULT_WAIT_SECONDS,
        poll_seconds: float = DEFAULT_POLL_SECONDS,
        pid: Optional[int] = None,
    ) -> LeaseMetadata:
        if not owner or not owner.strip():
            raise ValueError("owner must not be empty")
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        if wait_seconds < 0:
            raise ValueError("wait_seconds must not be negative")
        deadline = self.monotonic() + wait_seconds

        while True:
            self._ensure_available()
            remaining = max(0.0, deadline - self.monotonic())
            with self._guard(resource_id, min(2.0, remaining)):
                now = self.clock().astimezone(dt.timezone.utc)
                existing = self._read(resource_id)
                if existing is None or self._is_expired(existing, now):
                    lease_id = uuid.uuid4().hex
                    expires = now + dt.timedelta(seconds=ttl_seconds)
                    metadata = LeaseMetadata(
                        schema_version=SCHEMA_VERSION,
                        resource_id=resource_id,
                        lease_id=lease_id,
                        owner=owner,
                        workload=workload,
                        pid=os.getpid() if pid is None else pid,
                        hostname=socket.gethostname(),
                        acquired_at=_iso(now),
                        renewed_at=_iso(now),
                        expires_at=_iso(expires),
                        ttl_seconds=float(ttl_seconds),
                    )
                    self._write(metadata)
                    return metadata
                busy = existing

            remaining = deadline - self.monotonic()
            if remaining <= 0:
                raise LeaseBusyError(
                    f"resource {resource_id!r} is leased by {busy.owner!r} "
                    f"for {busy.workload!r} (pid={busy.pid}, lease_id={busy.lease_id}, "
                    f"expires_at={busy.expires_at})"
                )
            self.sleeper(min(max(0.01, poll_seconds), remaining))

    def renew(
        self,
        resource_id: str,
        lease_id: str,
        *,
        ttl_seconds: Optional[float] = None,
    ) -> LeaseMetadata:
        self._ensure_available()
        with self._guard(resource_id, 2.0):
            existing = self._read(resource_id)
            if existing is None:
                raise LeaseOwnershipError(f"resource {resource_id!r} has no lease")
            if existing.lease_id != lease_id:
                raise LeaseOwnershipError(
                    f"resource {resource_id!r} is owned by lease {existing.lease_id}; "
                    f"refusing to renew {lease_id}"
                )
            now = self.clock().astimezone(dt.timezone.utc)
            if self._is_expired(existing, now):
                raise LeaseExpiredError(
                    f"lease {lease_id} for resource {resource_id!r} expired at "
                    f"{existing.expires_at}"
                )
            ttl = existing.ttl_seconds if ttl_seconds is None else ttl_seconds
            if ttl <= 0:
                raise ValueError("ttl_seconds must be positive")
            renewed = dataclasses.replace(
                existing,
                renewed_at=_iso(now),
                expires_at=_iso(now + dt.timedelta(seconds=ttl)),
                ttl_seconds=float(ttl),
            )
            self._write(renewed)
            return renewed

    def release(self, resource_id: str, lease_id: str) -> bool:
        lease_path, _ = self._paths(resource_id)
        with self._guard(resource_id, 2.0):
            existing = self._read(resource_id)
            if existing is None:
                return False
            if existing.lease_id != lease_id:
                raise LeaseOwnershipError(
                    f"resource {resource_id!r} is owned by lease {existing.lease_id}; "
                    f"refusing to release {lease_id}"
                )
            try:
                lease_path.unlink()
            except OSError as exc:
                raise LeaseLockError(f"cannot release lease {lease_path}: {exc}") from exc
            return True

    @contextlib.contextmanager
    def hold(
        self,
        resource_id: str,
        owner: str,
        workload: str,
        *,
        ttl_seconds: float = DEFAULT_TTL_SECONDS,
        wait_seconds: float = DEFAULT_WAIT_SECONDS,
        poll_seconds: float = DEFAULT_POLL_SECONDS,
    ) -> Iterator[LeaseMetadata]:
        metadata = self.acquire(
            resource_id,
            owner,
            workload,
            ttl_seconds=ttl_seconds,
            wait_seconds=wait_seconds,
            poll_seconds=poll_seconds,
        )
        stop = threading.Event()
        heartbeat_error: list[BaseException] = []
        interval = max(0.05, min(ttl_seconds / 3.0, 30.0))

        def heartbeat() -> None:
            while not stop.wait(interval):
                try:
                    self.renew(resource_id, metadata.lease_id, ttl_seconds=ttl_seconds)
                except BaseException as exc:
                    heartbeat_error.append(exc)
                    return

        thread = threading.Thread(
            target=heartbeat,
            name=f"lease-heartbeat-{_resource_key(resource_id)}",
            daemon=True,
        )
        thread.start()
        body_error: Optional[BaseException] = None
        try:
            yield metadata
        except BaseException as exc:
            body_error = exc
            raise
        finally:
            stop.set()
            thread.join(timeout=max(1.0, interval + 1.0))
            try:
                self.release(resource_id, metadata.lease_id)
            except LeaseOwnershipError:
                if body_error is None:
                    raise
            if heartbeat_error and body_error is None:
                raise LeaseError(
                    f"lease heartbeat failed for {resource_id!r}: {heartbeat_error[0]}"
                ) from heartbeat_error[0]


def _metadata_json(metadata: Optional[LeaseMetadata]) -> str:
    return json.dumps(
        None if metadata is None else metadata.as_dict(),
        indent=2,
        sort_keys=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None, help="Override lease-state directory.")
    subparsers = parser.add_subparsers(dest="command_name", required=True)

    def add_resource(command: argparse.ArgumentParser) -> None:
        command.add_argument("--resource", default=DEFAULT_RESOURCE_ID)

    acquire = subparsers.add_parser("acquire", help="Acquire a lease and print its metadata.")
    add_resource(acquire)
    acquire.add_argument("--owner", required=True)
    acquire.add_argument("--workload", required=True)
    acquire.add_argument("--ttl-seconds", type=float, default=DEFAULT_TTL_SECONDS)
    acquire.add_argument("--wait-seconds", type=float, default=DEFAULT_WAIT_SECONDS)

    release = subparsers.add_parser("release", help="Release only the matching lease ID.")
    add_resource(release)
    release.add_argument("--lease-id", required=True)

    renew = subparsers.add_parser("renew", help="Renew only the matching active lease ID.")
    add_resource(renew)
    renew.add_argument("--lease-id", required=True)
    renew.add_argument("--ttl-seconds", type=float, default=None)

    status = subparsers.add_parser("status", help="Print current metadata or null.")
    add_resource(status)

    run = subparsers.add_parser("run", help="Hold a renewable lease while running a command.")
    add_resource(run)
    run.add_argument("--owner", required=True)
    run.add_argument("--workload", default="")
    run.add_argument("--ttl-seconds", type=float, default=DEFAULT_TTL_SECONDS)
    run.add_argument("--wait-seconds", type=float, default=DEFAULT_WAIT_SECONDS)
    run.add_argument("command", nargs=argparse.REMAINDER)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    manager = LeaseManager(args.root)
    try:
        if args.command_name == "acquire":
            metadata = manager.acquire(
                args.resource,
                args.owner,
                args.workload,
                ttl_seconds=args.ttl_seconds,
                wait_seconds=args.wait_seconds,
            )
            print(_metadata_json(metadata))
            return 0
        if args.command_name == "release":
            released = manager.release(args.resource, args.lease_id)
            print(json.dumps({"released": released}))
            return 0
        if args.command_name == "renew":
            print(
                _metadata_json(
                    manager.renew(
                        args.resource,
                        args.lease_id,
                        ttl_seconds=args.ttl_seconds,
                    )
                )
            )
            return 0
        if args.command_name == "status":
            print(_metadata_json(manager.status(args.resource)))
            return 0
        if args.command_name == "run":
            command = list(args.command)
            if command and command[0] == "--":
                command = command[1:]
            if not command:
                raise ValueError("run requires a command after --")
            workload = args.workload or Path(command[0]).name
            with manager.hold(
                args.resource,
                args.owner,
                workload,
                ttl_seconds=args.ttl_seconds,
                wait_seconds=args.wait_seconds,
            ) as metadata:
                print(_metadata_json(metadata), flush=True)
                return subprocess.call(command)
    except (LeaseError, OSError, ValueError) as exc:
        print(f"LEASE ERROR: {exc}", file=sys.stderr)
        return 3
    raise AssertionError(f"unhandled command {args.command_name}")


if __name__ == "__main__":
    raise SystemExit(main())
