# Router für gemeinsame Gesprächsverdichtungen

- **AI-ACCESS:** allowed
- **AI-CHAT-LOGGING:** summary
- **AI-MEMORY-EXPORT:** allowed
- **DATA-CLASSIFICATION:** public
- **INHERITS:** `${ENGINEERING_GOVERNANCE_ROOT}/AGENTS.md`
- **OVERRIDES:** dieser Unterbaum akzeptiert nur öffentliche, bereinigte Verdichtungen
- **SCOPE:** `${ENGINEERING_GOVERNANCE_ROOT}/why`

Hier gelten `${ENGINEERING_GOVERNANCE_ROOT}/docs/shared/chat-logging.md` und
`data-handling.md`. Private
Rohchats, Secrets, Personenkennungen und geschützte Projektdetails gehören nicht hierher.

Für jede Session mit versionierten Änderungen oder dauerhaften Entscheidungen entsteht eine
knappe WHY-Verdichtung. Sie beantwortet die W-Fragen, nennt verworfene Alternativen und
Validierung und kann aus materiellen Commit-Messages per `why-ref` referenziert werden.
