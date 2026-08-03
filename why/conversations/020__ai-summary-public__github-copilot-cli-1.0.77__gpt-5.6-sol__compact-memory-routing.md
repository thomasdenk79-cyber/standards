---
Agent: github-copilot-cli
Model: github-copilot/gpt-5.6-sol
Auftraggeber: private user
Datum + Uhrzeit: 2026-08-03T19:20:18+02:00
Zweck / Warum: Startup-Tokenverbrauch durch kompakte Router und deaktiviertes automatisches Memory-Laden senken.
---

# Entscheidung

- Root- und Memory-Router auf kurze Fakten und Stichpunkte verdichtet.
- `load_user_memory: false` und `load_agent_memory: false` als Workspace-Defaults gesetzt.
- `standards/settings.yml`, `user-memory/settings.yml` und optionale User-Settings bleiben Teil der Settings-Kette.
- User-/Agent-Memory-Inhalte werden nur bei aktivem Flag, explizitem Auftrag oder direkter Repo-Arbeit gelesen.
- Settings-Schema, Resolver, Validator und Tests unterstützen die neuen Flags.

# Abnahme

- `python standards/scripts/test_settings.py`: 7/7 Tests bestanden.
- `python standards/scripts/validate_settings.py`: OK.
- Effektive Werte: beide Memory-Flags `false`; `user_chat_lang` und `markdown_lang` bleiben `de`.
