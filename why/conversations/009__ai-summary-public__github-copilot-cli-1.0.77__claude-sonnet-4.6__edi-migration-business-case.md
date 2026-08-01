# WHY — Evidenzbasierte Bewertung: EDI-Migration Business Case

| Feld | Wert |
|---|---|
| Agent | GitHub Copilot CLI 1.0.77 |
| Model | anthropic/claude-sonnet-4.6 |
| Auftraggeber | private user |
| Datum | 2026-08-01T05:26+02:00 |
| Zweck | Kritische Bewertung der These: Erzwungene Migration VB.NET-Changetool → Jira und Oracle → PostgreSQL besitzt keinen belastbaren Business Case; Bestandsschutz und KI-Kompetenz seien wichtiger. |

## Warum

Eine erzwungene, kurzfristige Migration wurde als Handlungsoption diskutiert. Statt die These
zu bestätigen oder zu verwerfen, wurde sie anhand des tatsächlichen Quellbestands in `C:\git\edi`
und der zugehörigen KI-Infrastruktur evidenzbasiert geprüft. Alle Aussagen wurden mit
konkreten Datei- und Metrikquellen belegt oder als `[UNSICHER]` markiert.

## Was

- Vollständige Hierarchie `C:\git\AGENTS.md` und alle Projektketten wurden gelesen.
- EDI-Bestandsanalyse (327 Repos, 10,5 Mio. Netto-LOC, 6,55 Mio. SQL/PL-SQL-Zeilen) aus
  bereits vorliegendem Benchmark-Run (`gpt-5.6-sol__20260731-171535__edi-analysis`) ausgewertet.
- BISRTE-Architektur (`CKerDatabase.h`, `libKernel/`, 148 Consumer-Plugins, `AGENTS.md`)
  auf Oracle-Abhängigkeiten untersucht.
- Lokaler KI-Migrationspilot (`OracleMigration/`, `postgre/`, 7 Benchmark-Runs) als
  Kompetenzindikator bewertet.
- Changetool-Kontext geklärt: kein VB.NET-Produktivcode im Bestand; AutoIt3-basiert.
- Alle Dateien wurden ausschließlich gelesen; keine Änderungen vorgenommen.

## Kernergebnisse

**Belege für Bestandsschutz (These gestützt):**
- Oracle-OCI tief in libKernel verdrahtet; kein Datenbank-Adapter-Interface vorhanden.
- 6.480 Trigger, 11.365 `EXECUTE IMMEDIATE`, 993 Autonomous Transactions, 9.577 BULK COLLECT —
  kein naiver Lift-and-Shift möglich; 98.648 Risikopunkte (Heuristik).
- 148 Consumer-Plugins müssen bei DB-Schnittstellen-Änderung einzeln geprüft werden.
- VB.NET-Changetool nicht im Bestand gefunden; Scope der Jira-Migrations-These unklar.
- KI-Kompetenz wächst bereits organisch; Investitionen in diesen Stack sind No-Regret.

**Gegenargumente (These partiell geschwächt):**
- Oracle-Lizenzkosten und Vendor-Lock-in sind reale Langfristrisiken — nicht quantifiziert.
- 167 sensible Dateien ohne systematisches Secret-Management: Security-Hygiene-Risiko.
- Oracle-Version und Maintenance-Status unbekannt: EOL-Risiko nicht ausgeschlossen.

## Entscheidungen

- Erzwungene Vollmigration heute: kein belastbarer Business Case.
- Richtige Strategie: Adapter-Interface in libKernel, Secret-Management, Oracle-EOL-Klärung,
  ITIL-Einführung und KI-Kompetenzaufbau — danach Migrationsplan mit echten Daten.
- Jira-Migration: erst nach vollständiger Dokumentation des bestehenden Changetools.
- Entscheidungspunkt für Vollmigration frühestens 2027 Q3, wenn 8 definierte Kriterien erfüllt.

## Verworfene Alternativen

- Sofortige Vollmigration Oracle → PostgreSQL ohne Adapter-Interface.
- These blind bestätigen ohne Quellenprüfung.
- Jira-Migration ohne definierten Scope des Quellsystems.

## Validierung

- Alle Aussagen gegen konkrete Dateipfade und Metriken referenziert.
- Unsichere Aussagen (Oracle-Version, Lizenzkosten) als `[UNSICHER]` markiert.
- Kein Code, keine Konfiguration verändert; ausschließlich lesende Analyse.

## Referenzierte Quellen

| Quelle | Relevanz |
|---|---|
| `edi/bisrte/bisrte/source/common/libKernel/CKerDatabase.h` | OCI-Lock-in-Nachweis |
| `edi/bisrte/bisrte/AGENTS.md` | 148 Plugins, Architektur |
| `llm-benchmarks/gpt-5.6-sol__20260731-171535__edi-analysis/data/metrics.json` | Bestandsmetriken |
| `OracleMigration/README.md` | KI-Migrationspilot |
| `postgre/README.md` | Benchmark-Tooling |
| `edi/bisrte/controlcenter/ControlCenter_BIS.au3` | Changetool-Kontext |

## Follow-up

Sofortige No-Regret-Maßnahmen ohne Migrations-Entscheid:
1. Oracle-Version und EOL-Status dokumentieren.
2. 167 sensible Dateien inventarisieren; Secret-Rotation planen.
3. AutoIt3-Changetool reverse-engineeren und dokumentieren.
4. OCI-Adapter-Interface in libKernel vorbereiten.
5. Lokalen LLM-Migrations-Stack auf Produktions-PL/SQL-Objekten benchmarken.
