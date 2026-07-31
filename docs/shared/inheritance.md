---
title: Hierarchische Vererbung
doc_type: reference
status: active
canonical: true
---

<!--
Agent: GitHub Copilot CLI 1.0.77
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-07-31T09:18:22+02:00
Zweck / Warum: Ein gemeinsames Vererbungsmodell für Regeln, Einstellungen und Wissen definieren.
-->

# Hierarchische Vererbung

## Grundsatz

Markdown, YAML und andere hierarchische Konfigurations- oder Wissensdateien folgen demselben
Workspace-Prinzip: allgemeine Ebenen werden zuerst gelesen, spezifische Ebenen danach. Eine
Kindebene enthält nur das Delta zu ihren Eltern.

Pfad und Dateiname sind Teil der Information. Der Pfad bestimmt den Kontext; der Dateiname
beschreibt die Rolle innerhalb dieses Kontexts. Kontextpräfixe werden nicht wiederholt, wenn sie
keine zusätzliche Unterscheidung liefern.

## Operationen einer Kindebene

| Operation | Bedeutung | Sichtbare Form |
|---|---|---|
| Erben | Parent-Aussage gilt unverändert | Schlüssel oder Aussage fehlt im Kind |
| Ergänzen | Neue lokale Aussage kommt hinzu | neuer Schlüssel, Abschnitt oder Punkt |
| Überschreiben | Lokale Aussage ersetzt die Parent-Aussage | gleicher Schlüssel oder explizit benannter Override |
| Negieren | Parent-Aussage gilt lokal ausdrücklich nicht | `false`, `off`, `denied` oder klare textuelle Verneinung |

Schweigen bedeutet Vererbung, niemals Negation. Überschreiben und Negieren müssen sichtbar sein.
Bei strukturierten Dateien werden Mappings schlüsselweise zusammengeführt und Skalare ersetzt.
Listen werden standardmäßig ersetzt; Anhängen ist nur zulässig, wenn die jeweilige
Konfigurationsfamilie es ausdrücklich definiert.

Eine tiefere Ebene gewinnt nur innerhalb ihres autorisierten Geltungsbereichs. System-,
Sicherheits-, Rechts-, Datenschutz- und Secret-Grenzen können nicht abgeschwächt werden.

## SSOT und DRY

**Single Source of Truth (SSOT)** verlangt eine eindeutige maßgebliche Quelle für jede
Information. **Don’t Repeat Yourself (DRY)** verhindert, dass dieselbe Information in Pfaden,
Dateinamen oder Inhalten unnötig mehrfach gepflegt wird.

Beide Grundsätze gelten auch für Metadaten: `user-memory\settings.yml` ist klarer als
`user-memory\user-settings.yml`, weil der Pfad den User-Kontext bereits trägt. Bewusste
Wiederholung bleibt erlaubt, wenn ein Werkzeug einen festen Namen verlangt, mehrere Rollen im
selben Verzeichnis unterschieden werden müssen oder ein kurzer Sicherheitshinweis die
Fehlbedienung deutlich reduziert. Die Wiederholung verweist dann auf die kanonische Quelle,
statt eine zweite normative Wahrheit zu erzeugen.

## Drei Beispiele

### 1. `settings.yml`

```text
C:\GIT\standards\settings.yml
  C:\GIT\user-memory\settings.yml
    C:\GIT\user-memory\<username>\settings.yml
```

Die Standards-Datei enthält die vollständige Basis. `user-memory\settings.yml` überschreibt
globale User-Defaults. Eine optionale benutzerspezifische Datei ergänzt oder überschreibt nur
abweichende Werte. Vor dem Laden wird ihre Existenz geprüft. Fehlende Dateien und Schlüssel
bedeuten Vererbung; eine fehlende optionale Datei ist weder Fehler noch geladene Quelle.
Statusausgaben unterscheiden deshalb mögliche Pfade, geladene Quellen und geerbte Werte.

### 2. `AGENTS.md`

```text
C:\GIT\AGENTS.md
  C:\GIT\<repo>\AGENTS.md
    C:\GIT\<repo>\<module>\AGENTS.md
```

Der Repo-Router ergänzt Projektregeln. Ein Modul kann beispielsweise geerbten Netzwerkzugriff
mit `AI-NETWORK: denied` explizit negieren. `INHERITS` nennt die Elternquelle, `OVERRIDES`
benennt ersetzte Aussagen.

### 3. `README.md`

```text
C:\GIT\<repo>\README.md
  C:\GIT\<repo>\<module>\README.md
```

Das Modul-README wiederholt weder Projektzweck noch globales Setup. Es verlinkt das
Repo-README, ergänzt Modulbefehle und nennt ausdrücklich, wenn eine geerbte Annahme lokal nicht
gilt. Beide Dateien bleiben eigenständig lesbar, ohne konkurrierende Wahrheiten zu pflegen.

## Anwendung

Vererbung ist ein Workspace-Protokoll, keine blinde Dateikonkatenation. Jede Dateifamilie muss
Eltern, Reihenfolge und zulässige Overrides eindeutig festlegen. Werkzeuge dürfen das Modell
automatisch umsetzen; andernfalls lädt der Agent die Kette selbst von allgemein nach spezifisch.
