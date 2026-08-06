"""
Docs-Qualitätstest — lokal ausführen nach Änderungen.

Prüft:
  1. mkdocs build läuft durch (keine Fehler)
  2. Alle nav-Seiten wurden gebaut und sind nicht leer
  3. Keine kaputten internen Links in der gebauten Site
  4. AGENTS.md-Pflichtabschnitte vorhanden
  5. Workspace-Settings entsprechen dem Schema

Ausführen:
  python "$env:ENGINEERING_GOVERNANCE_ROOT\\scripts\\test_docs.py"

Oder mit pytest:
  pytest scripts\\test_docs.py -v
"""

import subprocess
import sys
import re
import atexit
import shutil
import tempfile
from urllib.parse import urlparse
from pathlib import Path
from html.parser import HTMLParser

# ── Pfade ──────────────────────────────────────────────────────────────────
SCRIPT_REPO_ROOT = Path(__file__).parent.parent
WORKING_DIR = Path.cwd()
REPO_ROOT   = WORKING_DIR if (WORKING_DIR / "AGENTS.md").exists() else SCRIPT_REPO_ROOT
SITE_DIR    = Path(tempfile.mkdtemp(prefix="mkdocs-docs-test-"))
DOCS_DIR    = REPO_ROOT / "docs"
MKDOCS_YML  = REPO_ROOT / "mkdocs.yml"
AGENTS_MD   = REPO_ROOT / "AGENTS.md"
SETTINGS_VALIDATOR = SCRIPT_REPO_ROOT / "scripts" / "validate_settings.py"
MKDOCS_RUNNER = SCRIPT_REPO_ROOT / "scripts" / "run_mkdocs.py"
atexit.register(shutil.rmtree, SITE_DIR, ignore_errors=True)


def get_site_path_prefix():
    """Return the path prefix from site_url, e.g. /engineering-governance."""
    if not MKDOCS_YML.exists():
        return ""
    match = re.search(r"^site_url:\s*[\"']?([^\s\"']+)", MKDOCS_YML.read_text(encoding="utf-8"), re.MULTILINE)
    return urlparse(match.group(1)).path.rstrip("/") if match else ""


# ── Hilfsklasse: interne Links aus HTML extrahieren ────────────────────────
class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, val in attrs:
                if attr == "href" and val and not val.startswith(("http", "#", "mailto")):
                    self.links.append(val)


# ── Tests ──────────────────────────────────────────────────────────────────

def test_mkdocs_build():
    """mkdocs build muss fehlerfrei durchlaufen."""
    if not MKDOCS_YML.exists():
        print(f"  SKIP keine mkdocs.yml in {REPO_ROOT}")
        return

    result = subprocess.run(
        [
            sys.executable,
            str(MKDOCS_RUNNER),
            "build",
            "--strict",
            "--site-dir",
            str(SITE_DIR),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"mkdocs build fehlgeschlagen:\n{result.stdout}\n{result.stderr}"
    )


def test_all_nav_pages_exist():
    """Jede Seite aus der mkdocs.yml nav muss als HTML in site/ existieren."""
    if not MKDOCS_YML.exists():
        return  # kein mkdocs.yml → Test überspringen

    yml_text = MKDOCS_YML.read_text(encoding="utf-8")

    # Alle .md-Pfade aus nav extrahieren
    md_paths = re.findall(r":\s+([^\s]+\.md)", yml_text)

    missing = []
    for md in md_paths:
        # index.md → index.html, andere → {name}/index.html
        stem = Path(md).stem
        parent = Path(md).parent
        if stem.lower() in {"index", "readme"}:
            html_path = SITE_DIR / parent / "index.html"
        else:
            html_path = SITE_DIR / parent / stem / "index.html"

        if not html_path.exists():
            missing.append(f"{md} → {html_path.relative_to(SITE_DIR)}")

    assert not missing, (
        f"Folgende nav-Seiten fehlen in site/:\n" + "\n".join(f"  ✗ {m}" for m in missing)
    )


def test_no_empty_pages():
    """Keine gebaute HTML-Seite darf unter 500 Zeichen sein (leere/fehlerhafte Seite)."""
    if not SITE_DIR.exists():
        return

    small = [
        str(f.relative_to(SITE_DIR))
        for f in SITE_DIR.rglob("*.html")
        if f.stat().st_size < 500
    ]
    assert not small, (
        f"Verdächtig kleine HTML-Seiten (< 500 Zeichen):\n" + "\n".join(f"  ✗ {s}" for s in small)
    )


def test_no_broken_internal_links():
    """Interne Links in HTML-Seiten müssen auf existierende Dateien zeigen."""
    if not SITE_DIR.exists():
        return

    broken = []
    site_prefix = get_site_path_prefix()
    for html_file in SITE_DIR.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8", errors="ignore")
        extractor = LinkExtractor()
        extractor.feed(content)

        for link in extractor.links:
            # Anker und Query-Strings entfernen
            clean = link.split("?")[0].split("#")[0].rstrip("/")
            if not clean:
                continue

            # Relativen Pfad auflösen
            if link.startswith("/"):
                if site_prefix and (clean == site_prefix or clean.startswith(f"{site_prefix}/")):
                    clean = clean[len(site_prefix):].lstrip("/")
                target = SITE_DIR / clean.lstrip("/")
            else:
                target = html_file.parent / clean

            # Prüfe ob Datei oder index.html im Verzeichnis existiert
            exists = (
                target.exists()
                or (target / "index.html").exists()
                or target.with_suffix(".html").exists()
            )
            if not exists:
                broken.append(f"{html_file.relative_to(SITE_DIR)} → {link}")

    assert not broken, (
        f"Kaputte interne Links ({len(broken)}):\n" + "\n".join(f"  ✗ {b}" for b in broken[:20])
    )


def test_agents_md_mandatory_sections():
    """AGENTS.md muss die Pflichtabschnitte enthalten (Ebene-1 Repo-Format)."""
    if not AGENTS_MD.exists():
        return

    content = AGENTS_MD.read_text(encoding="utf-8")

    required = [
        (("Aktueller Stand", "Current state"), "Aktueller-Stand-Block fehlt"),
        (("Nächster Schritt", "Nächster Agent", "Next step", "Next benchmark actions"), "Nächster-Schritt-Eintrag fehlt"),
    ]
    recommended = [
        ("model:", "agent/model/role provenance is missing"),
    ]

    content_lower = content.lower()
    missing = [
        msg
        for alternatives, msg in required
        if not any(keyword.lower() in content_lower for keyword in alternatives)
    ]
    assert not missing, (
        "AGENTS.md Pflichtabschnitte fehlen:\n" + "\n".join(f"  x {m}" for m in missing)
    )

    for keyword, msg in recommended:
        if keyword not in content:
            print(f"  WARN {msg}")


def test_workspace_settings_schema():
    """Workspace defaults must match their canonical schema."""
    if not SETTINGS_VALIDATOR.exists():
        return
    result = subprocess.run(
        [sys.executable, str(SETTINGS_VALIDATOR)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


# ── Direktaufruf (ohne pytest) ─────────────────────────────────────────────
if __name__ == "__main__":
    import io, os
    # UTF-8 Output erzwingen (Windows-Konsole cp1252 umgehen)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    tests = [
        test_mkdocs_build,
        test_all_nav_pages_exist,
        test_no_empty_pages,
        test_no_broken_internal_links,
        test_agents_md_mandatory_sections,
        test_workspace_settings_schema,
    ]

    passed = failed = 0
    for test in tests:
        name = test.__name__
        try:
            test()
            print(f"  OK   {name}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL {name}\n     {e}")
            failed += 1
        except Exception as e:
            print(f"  ERR  {name} — unerwarteter Fehler: {e}")
            failed += 1

    print(f"\n{'─'*50}")
    print(f"  {passed} bestanden · {failed} fehlgeschlagen")
    sys.exit(1 if failed else 0)
