# Engineering Workspace Router

- **SCOPE:** `${ENGINEERING_REPOS_ROOT}`
- **CANONICAL-GOVERNANCE:** `${ENGINEERING_GOVERNANCE_ROOT}/AGENTS.md`

## Start

1. `ENGINEERING_REPOS_ROOT` und `ENGINEERING_GOVERNANCE_ROOT` prüfen.
2. `${ENGINEERING_GOVERNANCE_ROOT}/AGENTS.md` vollständig lesen.
3. Nächste anwendbare Repo- und Modul-`AGENTS.md` lesen.
4. Optionalen User- oder Memory-Kontext nur gemäß Governance, Rolle und Aufgabe laden.

Fehlt die Initialisierung, fragt nur der primäre interaktive Agent nach. Subagenten raten
keine Pfade und verändern keine globale Konfiguration.

Diese Datei routet ausschließlich. Policies werden nur im Governance-Repository gepflegt.
