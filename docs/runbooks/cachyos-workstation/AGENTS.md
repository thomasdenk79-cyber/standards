# Agentenregeln für CachyOS-Workstation

READ-WHEN: Immer bei Arbeit in diesem Runbook.

1. Lies `MASTER_PROMPT.md` und `README.md` vollständig. Aktuelle direkte Nutzeranweisungen haben Vorrang; Freigabegrenzen gelten unabhängig vom YOLO-Modus.
2. Kommuniziere und dokumentiere auf Deutsch; schreibe Code und Kommentare auf Englisch.
3. Arbeite Inventory → Plan → Apply → Verify → Document → Commit. Inventur zuerst ausschließlich lesend.
4. Pflege wiederverwendbare Skripte in `scripts/`, Vorlagen in `configs/`, Tests in `tests/`; lege diese Ordner erst mit echten Dateien an. Skripte idempotent, nachvollziehbar, mit `--help` und wo sinnvoll `--dry-run`; sichere bestehende Konfigurationen und liefere Rollback.
5. Prüfe Distribution, Hardware, installierte Pakete, Dateisysteme und Abhängigkeiten zur Laufzeit. Keine hardcodierten Gerätenamen, Benutzernamen, Partitionen oder Display-IDs. Keine unbegründeten Tuning-Parameter.
6. Vor Partitionen, LUKS, Bootloader, initramfs, Secure Boot, Kernelwechsel, VFIO, Unternehmenssoftware, Autologin und NOPASSWD-sudo explizite Zustimmung einholen. Kein stillschweigendes Einverständnis durch `--yolo`.
7. Prüfe Pakete und Installationswege anhand vertrauenswürdiger aktueller Quellen. Keine unkontrollierten Remote-Skripte als Root, keine automatischen gefährlichen Befehle.
8. Nach jedem Schritt Funktion und Wiederholbarkeit testen; reale Messwerte statt Behauptungen. Dokumentiere offene Punkte und Wiederanlauf nach Neustart in lokalem `~/system-setup/TODO.md`.
9. Das Repository ist öffentlich: niemals Secrets, Tokens, Zugangsdaten, Firmendaten, personenbezogene Daten, Hardware-IDs oder ungefilterte Logs committen. Lokale Inventur bleibt lokal. Vor Commit und Push Diff auf Geheimnisse prüfen.
10. Halte Änderungen auf `docs/runbooks/cachyos-workstation/` begrenzt. Kleine thematische Commits, nach Möglichkeit Feature-Branch und Pull Request; kein Force-Push. Push nur bei vorhandener Autorisierung. Änderungen am gemeinsamen Standards-Framework nur nach gesondertem Auftrag.
11. Keine automatische Ausführung privilegierter Skripte durch GitHub Actions. Dokumentiere genaue manuelle Ausführung, Voraussetzungen und Rückweg.
12. Bei fehlenden Tools, Zugängen, Geräten oder Reboot-Möglichkeit klar als offen dokumentieren, nicht vortäuschen, etwas sei erledigt.