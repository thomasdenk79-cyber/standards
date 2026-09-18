# CachyOS Workstation – wiederverwendbarer Setup-Baukasten

Zentrale Einstiegspunkte:

1. [`MASTER_PROMPT.md`](MASTER_PROMPT.md): Anforderungen, Phasen und Sicherheitsgrenzen.
2. [`AGENTS.md`](AGENTS.md): Regeln für Codex und andere Agenten.
3. `scripts/`: wiederverwendbare, idempotente Setup-/Diagnose-/Verifikationsskripte, vom Agenten schrittweise zu entwickeln.
4. `configs/`: generische, bereinigte Konfigurationsvorlagen, vom Agenten zu entwickeln.
5. `tests/`: Tests für die Skripte, vom Agenten zu entwickeln.
6. [`CHANGELOG.md`](CHANGELOG.md): versionierte Änderungen.

## Start nach einer Neuinstallation

Codex starten und eingeben:

> Klone oder aktualisiere `https://github.com/thomasdenk79-cyber/standards`, lies `docs/runbooks/cachyos-workstation/MASTER_PROMPT.md`, `README.md` und `AGENTS.md` vollständig. Prüfe den Git-Status. Beginne mit lesender Inventur. Pflege wiederverwendbare Skripte, Konfigurationen, Tests und Dokumentation in diesem Runbook, committe nachvollziehbar und pushe nach Prüfung und mit Berechtigung. Beachte sämtliche Freigabegrenzen.

Das Repository ist öffentlich. Niemals Secrets, Firmeninformationen oder ungefilterte lokale Diagnosedaten committen. `~/system-setup/` bleibt lokal. Kein Skript ungeprüft mit Root-Rechten ausführen. Skripte müssen wiederholbar und möglichst mit Dry-Run testbar sein. Nach Neustart Codex erneut starten und anhand lokaler TODO.md fortsetzen.

## Status

Master-Prompt und Agentenregeln angelegt. Die eigentlichen Setup-Skripte werden erst nach Inventur der Zielmaschine entwickelt und getestet; sie sind noch nicht vorhanden.