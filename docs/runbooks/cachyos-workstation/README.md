# CachyOS Workstation – wiederverwendbarer Setup-Baukasten

## Einzeiler für den Agenten (kopieren und einfügen)

> Lies https://raw.githubusercontent.com/thomasdenk79-cyber/standards/main/docs/runbooks/cachyos-workstation/MASTER_PROMPT.md vollständig und führe den dort beschriebenen Auftrag aus, einschließlich der verlinkten Agentenregeln, GitHub-Skriptpflege, Tests und Freigabegrenzen.

Der Link zeigt immer auf den aktuellen Stand des Master-Prompts auf `main`. Der Master-Prompt enthält die vollständige Aufgabenbeschreibung und verweist auf die weiteren Dateien. Der Agent muss Zugriff auf GitHub und für Änderungen entsprechende Schreibrechte haben.

## Zentrale Einstiegspunkte

1. [`MASTER_PROMPT.md`](MASTER_PROMPT.md): Anforderungen, Phasen und Sicherheitsgrenzen.
2. [`AGENTS.md`](AGENTS.md): Regeln für Codex und andere Agenten.
3. `scripts/`: wiederverwendbare, idempotente Setup-/Diagnose-/Verifikationsskripte, vom Agenten schrittweise zu entwickeln.
4. `configs/`: generische, bereinigte Konfigurationsvorlagen, vom Agenten zu entwickeln.
5. `tests/`: Tests für die Skripte, vom Agenten zu entwickeln.
6. [`CHANGELOG.md`](CHANGELOG.md): versionierte Änderungen.

## Ausführung nach einer Neuinstallation

Codex starten und den obigen Einzeiler einfügen. Der Agent soll das Repository klonen oder aktualisieren, `MASTER_PROMPT.md`, `README.md` und `AGENTS.md` lesen, den Git-Status prüfen und mit einer lesenden Inventur beginnen. Er pflegt wiederverwendbare Skripte, Konfigurationen, Tests und Dokumentation im Runbook und committet nachvollziehbar; Push nur nach Prüfung und mit Berechtigung.

Das Repository ist öffentlich. Niemals Secrets, Firmeninformationen oder ungefilterte lokale Diagnosedaten committen. `~/system-setup/` bleibt lokal. Kein Skript ungeprüft mit Root-Rechten ausführen. Skripte müssen wiederholbar und möglichst mit Dry-Run testbar sein. Nach Neustart Codex erneut starten und anhand lokaler TODO.md fortsetzen.

## Status

Master-Prompt und Agentenregeln angelegt. Die eigentlichen Setup-Skripte werden erst nach Inventur der Zielmaschine entwickelt und getestet; sie sind noch nicht vorhanden.