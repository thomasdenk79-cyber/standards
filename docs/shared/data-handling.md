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
`store_user_sensitive_data` steuert ausschließlich **kuratierte Ableitungen** in User- und
Agent-Memory. Private Rohchats werden unabhängig durch `AI-CHAT-LOGGING` gesteuert.

| Wert | Persistenz |
|---|---|
| `none` | Keine sensiblen kuratierten Ableitungen dauerhaft speichern. |
| `only_at_user_memory` | Nur im privaten `user-memory`; dort dürfen notwendige Details erhalten bleiben. |
| `only_at_agent_memory` | Nur im privaten `agent-memory`, minimal und ausschließlich bei agentbezogenem Bedarf. |
| `all` | Vollständiger privater User-Kontext darf im `user-memory` erhalten bleiben; zusätzlich sind minimale agentbezogene Ableitungen im `agent-memory` erlaubt. |

Bewusst veröffentlichte Rollen- oder Projektidentität gilt nicht als sensible Userdaten; ihre
Weiterverwendung bleibt zweckgebunden. Secrets, Zugangsdaten und private Schlüssel sind keine
User-Memory-Daten und werden bei keinem Wert gespeichert. Es gilt Datenminimierung: so wenig
Detail und so kurze Aufbewahrung wie für den konkreten Zweck nötig.

Bei `AI-CHAT-LOGGING: transcript` liegt der native Rohchat unabhängig davon **1:1** im privaten
`chat_private_dir`; nur echte Secrets werden sichtbar redigiert. Eine bereinigte
WHY-Zusammenfassung im Shared-Repo ist eine neue, öffentliche Ableitung und enthält weder
personenbezogene noch vertrauliche oder sensible Informationen.

## Grenzen

- Projektinformationen bleiben im Projekt, sofern `AI-MEMORY-EXPORT` nichts Weiteres erlaubt.
- Userdaten und agentenspezifische Selbstkorrektur bleiben getrennte Zuständigkeitsdomänen.
- Metadaten dürfen bei `metadata-only` nur Existenz, Klasse, Zeitpunkt und zuständigen Geltungsbereich
  nennen, keine geschützten technischen oder persönlichen Details.
- Öffentliches Teilen erfordert `DATA-CLASSIFICATION: public`, passende Export-Policy und eine
  Secret-/Datenschutzprüfung.
