from __future__ import annotations

import datetime as dt
import multiprocessing
from pathlib import Path
import shutil
import sys
import unittest
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent))
import local_model_lease as lease


def _contending_acquire(root: str, start, results, owner: str) -> None:
    manager = lease.LeaseManager(Path(root))
    start.wait(5)
    try:
        metadata = manager.acquire(
            "local-llm",
            owner,
            f"ollama/{owner}",
            ttl_seconds=30,
            wait_seconds=0,
        )
        results.put(("acquired", metadata.lease_id))
    except lease.LeaseBusyError:
        results.put(("busy", None))


class MutableClock:
    def __init__(self) -> None:
        self.value = dt.datetime(2026, 8, 2, 10, 0, tzinfo=dt.timezone.utc)

    def __call__(self) -> dt.datetime:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += dt.timedelta(seconds=seconds)


class LocalModelLeaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = (
            Path(__file__).resolve().parent
            / ".test-state"
            / f"local-model-lease-{uuid.uuid4().hex}"
        )
        self.clock = MutableClock()
        self.manager = lease.LeaseManager(self.root, clock=self.clock)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def test_contention_surfaces_owner_and_preserves_active_lease(self) -> None:
        first = self.manager.acquire(
            "local-llm",
            "agent-a",
            "ollama/model-a",
            ttl_seconds=60,
            wait_seconds=0,
        )

        with self.assertRaises(lease.LeaseBusyError) as caught:
            self.manager.acquire(
                "local-llm",
                "agent-b",
                "llama.cpp/model-b",
                ttl_seconds=60,
                wait_seconds=0,
            )

        self.assertIn("agent-a", str(caught.exception))
        self.assertEqual(self.manager.status("local-llm").lease_id, first.lease_id)

    def test_concurrent_acquisition_has_exactly_one_winner(self) -> None:
        context = multiprocessing.get_context("spawn")
        start = context.Event()
        results = context.Queue()
        workers = [
            context.Process(
                target=_contending_acquire,
                args=(str(self.root), start, results, f"agent-{index}"),
            )
            for index in range(2)
        ]
        for worker in workers:
            worker.start()
        start.set()
        outcomes = [results.get(timeout=10) for _ in workers]
        for worker in workers:
            worker.join(timeout=10)
            self.assertEqual(worker.exitcode, 0)

        self.assertEqual([item[0] for item in outcomes].count("acquired"), 1)
        self.assertEqual([item[0] for item in outcomes].count("busy"), 1)

    def test_release_requires_matching_lease_id(self) -> None:
        first = self.manager.acquire(
            "local-llm",
            "agent-a",
            "ollama/model-a",
            ttl_seconds=60,
            wait_seconds=0,
        )

        with self.assertRaises(lease.LeaseOwnershipError):
            self.manager.release("local-llm", "not-the-owner")

        self.assertEqual(self.manager.status("local-llm").lease_id, first.lease_id)
        self.assertTrue(self.manager.release("local-llm", first.lease_id))
        self.assertIsNone(self.manager.status("local-llm"))

    def test_expired_lease_is_atomically_recovered(self) -> None:
        first = self.manager.acquire(
            "local-llm",
            "agent-a",
            "ollama/model-a",
            ttl_seconds=5,
            wait_seconds=0,
        )
        self.clock.advance(6)

        second = self.manager.acquire(
            "local-llm",
            "agent-b",
            "llama.cpp/model-b",
            ttl_seconds=60,
            wait_seconds=0,
        )

        self.assertNotEqual(second.lease_id, first.lease_id)
        self.assertEqual(self.manager.status("local-llm").lease_id, second.lease_id)
        with self.assertRaises(lease.LeaseOwnershipError):
            self.manager.release("local-llm", first.lease_id)


if __name__ == "__main__":
    unittest.main()
