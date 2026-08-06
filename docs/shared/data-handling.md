---
title: Datenhandhabung
doc_type: reference
status: active
canonical: true
---

<!-- Agent: OpenCode | Model: github-copilot/gpt-5.6-sol | Auftraggeber: [private user] | Datum + Uhrzeit: 2026-07-30T00:14:16+02:00 | Zweck / Warum: Kanonische Regeln für Klassifizierung, persönliche Daten und Memory-Grenzen. -->

# Datenhandhabung

## Klassifizierung

| Klasse | Umgang |
|---|---|
| `public` | Darf nach Prüfung auf Secrets, Rechte und personenbezogene Daten veröffentlicht werden. |
| `internal` | Bleibt im Workspace oder freigegebenen Teamkontext. |
| `confidential` | Nur aufgabenbezogen nach Kenntnisbedarf (Need-to-know); kein allgemeines Cross-Repo-Memory. |
| `restricted` | Nur ausdrücklich autorisierte Personen/Geltungsbereiche; kein Export ohne explizite Freigabe. |

Ein abgeleitetes Artefakt erbt die höchste Klassifizierung seiner Quellen. Redaktion oder
Bereinigung senkt die Klasse erst nach Prüfung; `AI-MEMORY-EXPORT: sanitized` allein macht
Inhalt nicht öffentlich. Die nächste `DATA-CLASSIFICATION` darf verschärfen, nicht still
herabstufen.

## Sensible Userdaten

Sensible Userdaten sind insbesondere Identifikatoren, Kontaktdaten, Familie, Gesundheit,
Finanzen, Beschäftigungsdetails, private Termine und nicht öffentliche Verhaltensprofile.
`store_user_sensitive_data` steuert ausschließlich **kuratierte Ableitungen**. Private
Rohchats werden unabhängig durch `AI-CHAT-LOGGING` gesteuert.

| Wert | Persistenz |
|---|---|
| `none` | Keine sensiblen kuratierten Ableitungen dauerhaft speichern. |
| `only_at_user_memory` | Nur in einer freigegebenen privaten User-Kontextquelle. |
| `only_at_agent_memory` | Legacy-Wert; bis zur Schemamigration nicht für neue Daten verwenden. |
| `all` | Legacy-Wert; neue Konfigurationen verwenden stattdessen explizite Quellen und Rollen. |

Bewusst veröffentlichte Rollen- oder Projektidentität gilt nicht als sensible Userdaten; ihre
Weiterverwendung bleibt zweckgebunden. Secrets, Zugangsdaten und private Schlüssel sind keine
Memory-Daten und werden bei keinem Wert gespeichert. Es gilt Datenminimierung: so wenig
Detail und so kurze Aufbewahrung wie für den konkreten Zweck nötig.

Bei `AI-CHAT-LOGGING: transcript` liegt der native Rohchat im privaten `chat_private_dir`.
Best-Practice ist `transcript_secret_handling: redact`; ein autorisierter User darf für seinen
entsprechend geschützten privaten Speicher `preserve` wählen und übernimmt dafür die
Verantwortung. Eine bereinigte WHY-Zusammenfassung im Shared-Repo ist eine neue öffentliche
oder interne Ableitung und enthält weder personenbezogene noch vertrauliche oder sensible
Informationen.

## Grenzen

- Projektinformationen bleiben im Projekt, sofern `AI-MEMORY-EXPORT` nichts Weiteres erlaubt.
- Userdaten und agentenspezifische Selbstkorrektur bleiben getrennte Zuständigkeitsdomänen.
- Metadaten dürfen bei `metadata-only` nur Existenz, Klasse, Zeitpunkt und zuständigen Geltungsbereich
  nennen, keine geschützten technischen oder persönlichen Details.
- Öffentliches Teilen erfordert `DATA-CLASSIFICATION: public`, passende Export-Policy und eine
  Secret-/Datenschutzprüfung.
