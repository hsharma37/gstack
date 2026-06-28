# AGENTS.md — ICTOS AI Agent Behavior Contract

This file governs how AI coding agents (Claude Code + gstack, Codex, Cursor, etc.)
behave when working in this repository. All agents must comply.

---

## Mandatory: gstack TechCEO workflow

Every session must start by verifying gstack is installed:

```bash
test -d ~/.claude/skills/gstack/bin && echo "GSTACK_OK" || echo "GSTACK_MISSING"
```

If GSTACK_MISSING, stop and tell the user to install gstack per `CLAUDE.md`.

When spawning Claude Code sessions for coding work, always use gstack skills:
- Security audit: "Load gstack. Run /cso"
- Code review: "Load gstack. Run /review"
- QA test the UI: "Load gstack. Run /qa"
- Build a feature end-to-end: "Load gstack. Run /office-hours then /autoplan, implement the plan, then run /ship"
- Plan before building: "Load gstack. Run /office-hours then /spec. Save the plan, don't implement."

---

## Hard Rules — Never Break These

### Rule 1: AI never owns execution decisions
No agent, at any time, may generate, suggest, or commit code that causes AI to
autonomously execute, modify, or cancel a live trade order.

The only valid execution path is:
```
signal (AI advisory) → suggestion (UI) → human approval → deterministic Python → MT5 bridge
```

### Rule 2: Deterministic safety rules are immutable
No agent may modify, disable, bypass, or add configuration toggles to:
- Position sizing formulas in `risk_service.py`
- Daily loss limit enforcement in `risk_service.py`
- Trading lockout logic in `daily_risk_ledger`
- Stop-loss enforcement in `execution_service.py`
- MT5 bridge connection guards in `mt5-bridge/`

Any such change requires: `/review` + `/cso` + explicit human sign-off in PR description.

### Rule 3: Protect the database schema for financial data
No agent may generate a migration that:
- Drops or renames columns in `trades`, `daily_risk_ledger`, or `trading_plans`
- Changes a NOT NULL constraint on financial fields without a migration + human review
- Removes audit trail fields (created_at, updated_at, closed_at, etc.)

### Rule 4: Use /guard for protected paths
Before editing any file in:
- `backend/app/services/risk_service.py`
- `backend/app/services/execution_service.py`
- `mt5-bridge/`

...activate `/guard` to enable `/careful` (destructive command warnings) and
`/freeze` (edit lock to that directory).

---

## AI Advisory Boundaries

AI **may** do the following (advisory, never autonomous):
- Generate setup grading scores and explanations
- Generate journal review narratives
- Answer ICT concept questions via RAG
- Suggest position sizes (user must confirm)
- Surface confluences and pattern observations
- Generate research hypotheses for backtesting

AI **must not** do the following:
- Place, modify, or cancel live orders
- Override daily risk limits
- Mark a trade as closed without a verified MT5 confirmation
- Write or store embeddings that include raw account credentials, API keys, or PII

---

## Phase 3 Agent Workflow

When building Phase 3 features (Analytics + Research Engine):

1. Start with `/office-hours` — define the exact ICT research question
2. Run `/spec` — get a precise backlog-ready spec before writing any code
3. Run `/plan-eng-review` — lock the data flow and test plan
4. Implement in `analytics_service` or `research_service` per `ARCHITECTURE.md`
5. Run `/review` — catch bugs and correctness issues
6. Run `/qa` — browser QA of Analytics/Research pages
7. Run `/benchmark` — verify backtest performance (target: 1000 trades < 30s)
8. Run `/ship` — sync, test, PR
9. Run `/document-release` — keep ARCHITECTURE.md and MIGRATION_ROADMAP.md current

---

## Security

- Run `/cso` before merging any PR touching `risk_service`, `execution_service`, or `mt5-bridge`
- `/cso` runs OWASP Top 10 + STRIDE threat model, 8/10+ confidence gate
- Prompt injection defenses in `/browse` are active — always use `/browse`, never raw browser MCP tools

---

## References

- `CLAUDE.md` — Full TechCEO skill routing, ICTOS principles, and dev commands
- `ARCHITECTURE.md` — Service boundaries, data flow, and stack decisions
- `MIGRATION_ROADMAP.md` — Phase definitions and success criteria
