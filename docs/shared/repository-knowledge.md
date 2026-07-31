---
title: Repository-Wissensmodell
doc_type: reference
status: active
canonical: true
---

<!--
Agent: GitHub Copilot CLI
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-07-30T09:02:07+02:00
Zweck / Warum: Vendor-neutrale Trennung von Fachwissen, Arbeitsstatus und Agentenanweisungen.
-->

# Repository-Wissensmodell

Dieses Modell hält zwei Ziele gleichzeitig ein:

1. **Fachliche Klarheit:** Ein Agent muss Ziel, Anforderungen, Grenzen und Änderungen zuverlässig
   finden und darf sie nicht bei jeder Session neu interpretieren.
2. **Lösungsfreiheit:** Der User muss nicht jede Umsetzung vorgeben. Der Agent darf innerhalb der
   belegten Anforderungen selbstständig entwerfen, implementieren und verbessern.

Je unklarer oder folgenreicher eine Anforderung ist, desto wichtiger sind sichtbare Annahmen,
Akzeptanzkriterien und gegebenenfalls eine Rückfrage. Nicht jede frühe Idee braucht sofort einen
formalen Anforderungskatalog.

## Defaults unter Kontrolle des Repository-Owners

Dieses Modell ist ein gemeinsames **Best-Practice-Gerüst, kein Zwangsprofil**. Es verhindert,
dass jedes Team dieselben Grundfragen unabhängig und widersprüchlich neu lösen muss. Der
autorisierte Repository-Owner entscheidet dennoch abschließend über Arbeitsweise, Dokumentation
und Agentennutzung in seinem Scope.

Die allgemeine Semantik für Erben, Ergänzen, Überschreiben und Negieren steht ausschließlich
unter [Hierarchische Vererbung](inheritance.md).

- Ohne lokalen Override gelten die geerbten Workspace-/Parent-Defaults.
- Ein Repo darf einzelne Defaults übernehmen, konkretisieren, ersetzen oder deaktivieren.
- Ein Repo darf Agentenzugriff auf `read-only` setzen oder mit `AI-ACCESS: denied` vollständig
  ausschließen.
- Ein Repo darf andere Dateien und Prozesse verwenden, wenn seine kanonischen Quellen und
  lokalen Regeln eindeutig geroutet sind.
- Repo-Typ, Reifegrad und Risiko liefern Empfehlungen, aber keine automatisch erzwungenen
  Artefakte oder Berechtigungen.
- Ein Agent darf Owner-Policies weder selbst einführen noch seine Rechte erweitern.

Nur übergeordnete Sicherheits-, Rechts-, Datenschutz- und Secret-Schutzgrenzen sowie explizite
User-Vorgaben bleiben unverhandelbar. Die genaue Policy-Semantik steht im anwendbaren
Workspace-/Parent-Router; Vendor-Adapter dürfen sie nicht verändern.

## Welche Information gehört wohin?

| Information | Kanonischer Ort | Nicht dafür verwenden |
|---|---|---|
| Vision, Zweck, Zielgruppen, Ziele, Nicht-Ziele | `docs/project/project-brief.md` oder gleichwertige verlinkte Datei | `AGENTS.md`, Taskboard, Changelog |
| Fachliche Anforderungen und akzeptierte Changes | bei kleinen Projekten im Project Brief, sonst `docs/project/requirements.md` | Vendor-Instructions, Agent-Memory |
| Architektur und technische Grenzen | `docs/project/architecture.md` oder gleichwertig | Requirements als Implementierungsdiktat |
| Folgenreiche Entscheidungen und verworfene Alternativen | `docs/engineering/decision-log.md` oder ADRs | nachträglich umgeschriebene Requirements |
| Aktuelle Aufgaben und Fortschritt | `docs/project/taskboard.md`, Issue-Tracker oder Handover | Project Brief |
| Ausgelieferte Änderungen | `docs/project/changelog.md` oder Releases | Requirements |
| Aktueller Einstieg, Policy, lokale Arbeitsregeln und Verweise | nächste anwendbare `AGENTS.md` | vollständige Fachspezifikation |
| Vendor- oder dateispezifische Agentenregeln | dünne Adapter oder scoped Rule-Dateien | zweite fachliche Wahrheit |

Andere Dateinamen sind zulässig. Entscheidend sind **eine kanonische Quelle pro Thema** und
eindeutige Verweise aus der Repo-`AGENTS.md`.

### Dateinamen

- Eigene technische Dateien verwenden lowercase ASCII-Kebab-Case, zum Beispiel
  `project-brief.md`, `requirements.md`, `todo.md` und `handover.md`.
- Pfad und Dateiname folgen gemeinsam SSOT und DRY: Der Pfad trägt den Kontext, der Dateiname
  nur die darin noch nötige Rolle. Kontextpräfixe werden nicht ohne unterscheidenden Nutzen
  wiederholt.
- Reservierte oder weithin automatisch erkannte Ökosystemnamen bleiben unverändert:
  `AGENTS.md`, `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md` und `CODEOWNERS`.
- Vendor-Dateien verwenden exakt die vom Werkzeug erwartete Schreibweise und Endung.
- Bestehende Dateien werden nur mit Nutzen und vollständig aktualisierten Verweisen umbenannt,
  nicht für reine Kosmetik.

## Empfohlener Artefakt-Katalog: nur bei echtem Bedarf

Der Katalog ist ein Satz konsistenter Defaults für typische Software- und Betriebsprojekte, aber
kein Pflicht-Dateibaum. Der Repository-Owner entscheidet, welche Artefakte Nutzen bringen, welche
gleichwertig anders gelöst und welche vollständig weggelassen werden. Eine Datei entsteht nur,
wenn sie eine eigene kanonische Aufgabe erfüllt.

| Artefakt | Zweck | Wann anlegen |
|---|---|---|
| `AGENTS.md` | Vendor-neutraler Router, Policy, Scope, Fachanker | Bei Agentenarbeit im Scope |
| `README.md` | Menschlicher Einstieg, Nutzen, Setup, Quickstart | Fast immer |
| `LICENSE` | Nutzungsrechte | Bei veröffentlichter oder geteilter Software |
| `CONTRIBUTING.md` | Beitrags-, Review- und Entwicklungsablauf | Bei mehreren Beitragenden |
| `SECURITY.md` | Meldeweg und unterstützte Versionen für Schwachstellen | Bei veröffentlichter/produktiver Software |
| `CODEOWNERS` | Review-/Ownership-Zuordnung | Wenn Plattform und Team es nutzen |
| `CHANGELOG.md` oder Releases | Ausgelieferte nutzerrelevante Änderungen | Wenn Releases/Versionen existieren |
| `project-brief.md` | Vision, Zweck, Zielgruppen, Ziele, Nicht-Ziele | Wenn README dafür nicht präzise genug ist |
| `requirements.md` | Wachsende, geänderte oder formal abgenommene Fachanforderungen | Ab mehreren rückverfolgbaren Requirements |
| `architecture.md` | Systemgrenzen, Komponenten, Datenfluss, technische Invarianten | Wenn Code allein das Systembild nicht erklärt |
| `decision-log.md` oder `adr/` | Folgenreiche Entscheidungen, Alternativen, Status | Bei langlebigen oder kontroversen Entscheidungen |
| `taskboard.md`, `todo.md` oder Issues | Eine kanonische Aufgabenquelle | Wenn offene Arbeit koordiniert werden muss |
| `handover.md` | Aktiver Wiederaufsetzpunkt | Nur bei unvollständiger/schwer rekonstruierbarer Arbeit |
| `runbook.md` | Normalbetrieb, Diagnose und wiederholbare Operator-Aktionen | Bei betriebenen Systemen |
| `recovery.md` | Restore/Disaster-Recovery mit RPO/RTO und Prüfung | Bei zustandsbehafteten oder kritischen Systemen |
| `test-strategy.md` oder `test-plan.md` | Testebenen, Risiken, Umgebungen, Abnahme | Wenn Tests nicht aus Build/CI und Requirements hervorgehen |
| `threat-model.md` | Assets, Trust Boundaries, Bedrohungen, Kontrollen | Bei relevanter Sicherheitswirkung |
| `data-model.md` / API-Spezifikation | Verträge für Daten und Schnittstellen | Bei gemeinsam genutzten oder externen Verträgen |
| `migration-plan.md` | Phasen, Kompatibilität, Cutover, Rollback | Bei Migrationen |
| `incident-log.md` / Postmortem | Evidenz-Timeline, Ursache, Wirkung, Maßnahmen | Bei relevanten Incidents |

Ein generisches `instructions.md` wird nicht als zusätzliche Standarddatei empfohlen: dauerhafte
Arbeitsregeln gehören in den Router oder in klar benannte Engineering-Dokumente; Vendor-Dateien
verwenden ihren exakten reservierten Pfad. Ebenso sind `state.md`, `progress.md` und `resume.md`
ohne klar getrennten Zweck meist redundante zweite Wahrheiten.

## Arbeitsstatus und Wiederaufnahme

Git, Session-Autosave und Projektdokumente lösen verschiedene Probleme:

| Quelle | Liefert | Liefert nicht zuverlässig |
|---|---|---|
| Git-Status, Diff und Log | geänderte Dateien, Inhalt, Historie | Absicht, letzter geprüfter Zustand, nächster Schritt |
| Issue-Tracker oder Taskboard | gemeinsamer Backlog und Status | lokaler uncommitteter Zwischenstand |
| `handover.md` | knapper aktiver Wiederaufsetzpunkt | langfristige Anforderungen oder vollständige Historie |
| nativer Session-Store/Transcript | Gespräch, Toolablauf und Crash-Recovery | aktuelle kanonische Wahrheit |
| Changelog/Releases | ausgelieferte Änderungen | offene Arbeit |

### Wann welche Zustandsdatei?

- **Taskboard/TODO:** genau eine gemeinsame Aufgabenquelle pro Scope. Kleine Repos dürfen eine
  kurze Markdown-Liste verwenden; Teams können Issues nutzen. Erledigte Einträge schließen oder
  archivieren, statt eine endlose Startdatei zu erzeugen.
- **Handover:** nur bei aktiver, unvollständiger oder schwer rekonstruierbarer Arbeit. Enthält
  Task/Requirement, letzten verifizierten Zustand, betroffene Dateien, Blocker und genau den
  nächsten Befehl. Die aktuelle Sicht wird aktualisiert; Git bewahrt ihre Historie.
- **`resume.md`:** standardmäßig nicht anlegen. Sie wäre semantisch ein zweiter Handover und
  würde driften.
- **`recovery.md`:** nur für technische Betriebswiederherstellung, etwa Datenbank, Deployment,
  Backup oder Maschine; nicht für gewöhnliche Agentenfortsetzung.
- **Progress-Log:** nur wenn eine unveränderliche fachliche Timeline benötigt wird. Normale
  Entwicklungsfortschritte stehen bereits in Git, Tasks und Changelog.

Projektgebundene Tasks bleiben im Fach-Repo. Repoübergreifende oder noch keinem Repo
zuordenbare Arbeit darf in einer gemeinsamen Agenten-Inbox liegen und wird verschoben oder
verlinkt, sobald ein fachlicher Owner existiert. Persönliches Agent-Memory ist keine gemeinsame
Taskquelle.

### Aufgabenbezogener Abruf

Optional bedeutet **bei Bedarf**, nicht **ignorierbar**. Eine Markdown-Datei wird geladen,
sobald ein direkter Verweis, die User-Frage oder die aktuelle Aufgabe ihren Inhalt relevant
macht. Der Agent sucht gezielt nach passenden Quellen, statt alle optionalen Dateien beim
Startup zu lesen.

Bei Fragen wie „Welche TODOs stehen an?“ umfasst die Suche im anwendbaren Scope mindestens:

- aktive `AGENTS.md`-Router und deren Fachanker;
- Memory-Indizes und die gemeinsame Inbox;
- `todo*.md`, `task*.md` und relevante `handover*.md`;
- den vom Projekt benannten Issue-Tracker oder Taskbereich.

Treffer werden über ihre kanonischen Verweise zusammengeführt. Historische Reports,
abgeschlossene Checklisten und duplizierte Handovers sind keine zusätzlichen aktuellen
Aufgabenquellen.

### Recovery-Reihenfolge nach Crash oder Agentenwechsel

1. Native Session fortsetzen, wenn sie verfügbar und gesund ist.
2. `git status`, `git diff` und jüngere relevante Commits prüfen.
3. Repo-Router und aktiven Task/Handover lesen.
4. Nur die verlinkten Requirements, Decisions und Tests laden.
5. Transcript gezielt durchsuchen, falls Absicht oder Begründung weiterhin fehlt.
6. Letzten dokumentierten Check erneut ausführen, bevor Erfolg behauptet wird.

Ein vollständiger Chat ist **append-only Evidenz**, aber kein Startup-Dokument. Laufzeiten sollen
ihn automatisch und crash-sicher speichern; manuelle Rekonstruktionen sind unzuverlässig. Exporte
werden getrennt von der kanonischen Projektdokumentation und gemäß Datenklassifizierung
aufbewahrt.

## Skalierbare Anforderungsführung

### Stufe 1: Rudimentäre Idee

Für einen frühen oder kleinen Wunsch genügen im Project Brief:

- gewünschtes Ergebnis und erkennbarer Nutzen;
- bekannte Grenzen oder Nicht-Ziele;
- Annahmen des Agents;
- offene, folgenreiche Fragen;
- ein prüfbares Beispiel oder Akzeptanzsignal, wenn bereits bekannt.

Der Agent darf vernünftige, reversible Details selbst entscheiden. Er fragt nach, wenn mehrere
plausible Antworten Ziel, Daten, Sicherheit, Kosten, Kompatibilität oder UX wesentlich
unterschiedlich verändern. Niedrigriskante Details blockieren die Umsetzung nicht.

### Stufe 2: Gewachsene oder geänderte Anforderungen

Eine eigene `requirements.md` ist sinnvoll, wenn mehrere Features, Stakeholder, Abhängigkeiten,
Changes oder wiederkehrende Missverständnisse entstehen. Dann braucht jede langfristig
rückverfolgbare Anforderung eine stabile ID, zum Beispiel `REQ-001`.

Empfohlene Felder:

| Feld | Zweck |
|---|---|
| ID und Titel | stabile Identität über Umformulierungen hinweg |
| Status | proposed, accepted, implemented, rejected oder superseded |
| Quelle und Erfassungsdatum | Herkunft und zeitlicher Kontext |
| Ziel/Nutzen | warum die Anforderung existiert |
| Anforderung | gewünschtes beobachtbares Ergebnis, nicht vorschnell die Implementierung |
| Akzeptanzkriterien/Beispiele | woran die Erfüllung erkennbar ist |
| Grenzen, Annahmen, offene Fragen | bewusster Interpretationsraum |
| Verweise | Tasks, ADRs, Tests, Releases und ablösende Anforderungen |

Nicht jedes Feld muss bei der ersten Äußerung vollständig sein. Unbekanntes bleibt sichtbar offen,
statt erfunden zu werden.

### Stufe 3: Hohes Risiko oder formale Abnahme

Bei Produktion, Regulierung, Verträgen, Migrationen oder sicherheitskritischen Änderungen können
zusätzlich Owner, Priorität, versionierte Baselines, eine Traceability-Matrix und formale
Freigaben nötig sein. Diese Strenge ist risikobasiert und kein Default für jedes Hobbyprojekt.

## Änderungen ohne Wissensverlust

- Neue Wünsche als neue oder geänderte Anforderung klassifizieren, nicht nur als TODO.
- Akzeptierte Inhalte nicht still überschreiben. Wesentliche Bedeutungsänderungen mit Datum,
  Grund und Status festhalten; ersetzte Anforderungen als `superseded` verlinken.
- Taskboard, Code, Tests und Changelog setzen Anforderungen um, ersetzen sie aber nicht.
- Fehlerkorrekturen auf die verletzte Anforderung oder das beobachtbare Sollverhalten beziehen.
- Bei Widerspruch zwischen Chat, Task und kanonischer Datei den Widerspruch sichtbar klären.
- Fachinformationen bleiben im Fach-Repo und beachten dessen Klassifizierung und Exportgrenzen.

## Rolle von `AGENTS.md`

`AGENTS.md` ist der vendor-neutrale **Router und Arbeitsvertrag** für seinen Verzeichnisbereich:

- Policy, Scope, Vererbung und lokale Overrides;
- knapper aktueller Zustand und nächster Einstieg;
- Links auf Vision, Requirements, Architektur, Decisions, Tasks und Tests;
- wenige wirklich lokale, dauerhaft geltende Arbeits- und Sicherheitsregeln.

Es ist keine vollständige Produktbeschreibung und kein Ersatz für Requirements. Kritische
Invarianten dürfen knapp wiederholt werden, müssen aber auf ihre fachliche Quelle verweisen.

## Vendor-Dateien und Markup

Vendor-Dateien sind Adapter. Sie enthalten nur Regeln, die das jeweilige Werkzeug technisch
benötigt, und verweisen ansonsten auf `AGENTS.md` oder die kanonischen Fachdateien.

| Werkzeug | Erkannte Dateien | Scope/Markup |
|---|---|---|
| OpenAI Codex | `AGENTS.md`, `AGENTS.override.md` | Verzeichnishierarchie, Markdown |
| GitHub Copilot | `AGENTS.md`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md` | repo-weit oder YAML-Frontmatter `applyTo` |
| Claude Code | `CLAUDE.md`, `.claude/rules/*.md` | Imports mit `@AGENTS.md`; Rules optional mit `paths`-Frontmatter |
| Gemini CLI | `GEMINI.md` | Markdown, Imports; `AGENTS.md` kann als Kontextdateiname konfiguriert werden |
| Cursor | `AGENTS.md`, `.cursor/rules/*.mdc` | verschachtelte Router oder MDC-Frontmatter mit `globs`/`alwaysApply` |
| Devin Desktop/Windsurf | `AGENTS.md`, `.devin/rules/*.md`, legacy `.windsurf/rules/*.md` | Verzeichnisscope oder Rule-Frontmatter |

Vendor-Adapter dürfen eine gemeinsame Regel nicht kopieren, wenn ein Link oder Import genügt.
Wo ein Tool `AGENTS.md` nicht nativ lädt, ist ein kleiner Adapter wie `CLAUDE.md` mit
`@AGENTS.md` vorzuziehen. Tool-Support und Frontmatter können sich ändern; vor neuen Adaptern
die aktuelle offizielle Dokumentation prüfen.

## Informationsbudget und Markup

- Wichtige Regeln und der aktuelle Zustand stehen früh; historische Details werden verlinkt.
- Kurze Überschriften, Tabellen, Listen, IDs, Statuswerte und exakte Pfade sind Freitext
  vorzuziehen.
- Fettdruck markiert wenige wirklich kritische Begriffe; flächige Hervorhebung zerstört das
  Signal.
- Pro Datei eine Aufgabe und pro Thema eine kanonische Quelle.
- Router und Startup-Kontext bleiben so kurz wie möglich; Details werden just-in-time geladen.
- Veraltete TODOs, doppelte Zusammenfassungen und lange Tool-Ausgaben werden nicht als Hot
  Context geführt.

Diese Struktur verbessert Auffindbarkeit und Attention-Signale, trainiert aber keine
Modellgewichte und ist nicht mit menschlichem visuellem Lernen gleichzusetzen.

## Mindestanker in jedem Fach-Repo

Die Repo-`AGENTS.md` nennt mindestens:

1. Vision/Zweck sowie Ziele/Nicht-Ziele;
2. akzeptierte Fachanforderungen und Changes;
3. Architektur/Entscheidungen;
4. aktuellen Arbeitsstatus;
5. relevante Tests oder Abnahmesignale.

Mehrere Punkte dürfen auf dieselbe kleine Datei zeigen. Fehlende Artefakte werden nicht
vorsorglich erzeugt; sie entstehen erst, wenn Umfang, Risiko oder Änderungsrate sie rechtfertigen.

## Vorlagen

- Project Brief: `docs/templates/project-brief-template.md`
- Requirements: `docs/templates/requirements-template.md`
- Handover: `docs/templates/handover-template.md`
- Repo-Router: `docs/templates/agents-template.md`

## Offizielle Referenzen

- [AGENTS.md](https://agents.md/)
- [OpenAI Codex: AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md/)
- [GitHub Copilot: Repository Instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
- [VS Code: Custom Instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
- [Claude Code: Memory](https://code.claude.com/docs/en/memory)
- [Gemini CLI: GEMINI.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md)
- [Cursor Rules](https://cursor.com/docs/rules)
- [Devin Desktop: AGENTS.md](https://docs.devin.ai/desktop/cascade/agents-md)
- [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [SWE-agent](https://arxiv.org/abs/2405.15793)
- [Agentless](https://arxiv.org/abs/2407.01489)
