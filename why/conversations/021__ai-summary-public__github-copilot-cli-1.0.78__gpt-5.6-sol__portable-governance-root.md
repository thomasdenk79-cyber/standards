---
Agent: github-copilot-cli
Model: github-copilot/gpt-5.6-sol
Auftraggeber: private user
Datum + Uhrzeit: 2026-08-06T22:48:22+02:00
Zweck / Warum: Gemeinsame Governance und Workspace-Verweise ohne feste Checkout-Pfade portabel machen.
---

# Entscheidung

- Gemeinsame Policies liegen im eigenstaendigen Repository `engineering-governance`.
- Der Workspace-Root bleibt ein kurzer Router; Repo- und Modul-Router erben die Governance.
- `${ENGINEERING_REPOS_ROOT}` bezeichnet den Repository-Workspace,
  `${ENGINEERING_GOVERNANCE_ROOT}` den Governance-Checkout.
- Repo-interne relative Pfade bleiben erlaubt; zentrale Altpfade und feste Workspace-Laufwerke
  sind in aktiven Quellen verboten.
- Optionale User- und Semantic-Memory-Dateien werden rollenbasiert und begrenzt geladen; das
  bisherige automatische User-/Agent-Memory-Laden bleibt deaktiviert.
- Ein Bootstrap-Konzept fuer Provider-Router und plattformunabhaengige Initialisierung ist
  dokumentiert, aber bewusst noch nicht als Produktcode umgesetzt.

# Verworfene Alternativen

- Ein festes globales Checkout-Verzeichnis wurde wegen Umzuegen, Junctions und
  plattformuebergreifender Nutzung verworfen.
- Kopierte Provider- und Repo-Policies wurden wegen Drift und Tokenkosten verworfen.
- Unbegrenztes, von allen Rollen geladenes semantisches Memory wurde wegen Kontextkosten und
  unklarer Autoritaet verworfen.

# Abnahme

- Governance-Unit-Tests: 42 bestanden.
- Governance-Dokumentationspruefungen: 6 bestanden.
- Rekursiver Portabilitaetsaudit: 0 aktive, 599 bewusst historische Treffer.
- Betroffene Workbench-, TaskVision- und Terminal-Adaptertests bestanden.
