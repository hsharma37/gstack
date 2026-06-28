# ICTOS — TechCEO Skill Routing (CLAUDE.md)

> This file configures Claude Code / gstack as the **TechCEO** for the ICTOS project.

---

## gstack Installation Check

```bash
test -d ~/.claude/skills/gstack/bin && echo "GSTACK_OK" || echo "GSTACK_MISSING"
```

If **GSTACK_MISSING**, install before any AI-assisted work:

```bash
git clone --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup
```

---

## Skill Routing Table

| Skill | Command | When to Use |
|-------|---------|-------------|
| **Office Hours** | `/office-hours` | Start any new feature — define the research question |
| **Spec** | `/spec` | Write backlog-ready specs with test criteria |
| **Plan Review** | `/plan-eng-review` | Review data flows, sequence diagrams, failure modes |
| **Code Review** | `/review` | Structural + correctness review before merge |
| **QA** | `/qa` | Browser QA of Analytics/Research/Journal pages |
| **Benchmark** | `/benchmark` | Verify backtest performance (target: 1000 trades < 30s) |
| **Ship** | `/ship` | Run tests, create PR, merge |
| **Document** | `/document-release` | Keep ARCHITECTURE.md and MIGRATION_ROADMAP.md current |
| **Security Audit** | `/cso` | OWASP Top 10 + STRIDE threat model before risky changes |
| **Guard** | `/guard` | Protect `risk_service.py`, `execution_service.py`, `mt5-bridge/` |

---

## ICTOS-Specific Dev Commands

### Backend
```bash
cd projects/ictos/backend
uvicorn app.main:app --reload --port 8000
pytest -v
```

### Frontend
```bash
cd projects/ictos/frontend
npm install
npm run dev
```

### Full Stack
```bash
cd projects/ictos
docker compose up --build
make dev
```

---

## Safety Rules

1. **Never let AI execute trades** — The execution path is: `signal → UI suggestion → human approval → deterministic Python → MT5 bridge`
2. **Protected paths require `/guard`** — Before editing `risk_service.py`, `execution_service.py`, or `mt5-bridge/`
3. **Risk rules are immutable** — No config toggle can override daily loss limits or position sizing
4. **All DB schema changes to financial tables require human review**

---

## Project Context

ICTOS is a **local-first trading workstation** for ICT-methodology traders. Phase 3 adds the Analytics + Research Engine:

- **Analytics**: Expectancy, win rate, R-factor, session heatmaps, confluence scoring, drawdown
- **Research**: vectorbt backtesting, Backtrader simulation, Monte Carlo, Kelly Criterion
- **Risk**: Position sizing, daily loss limits, lockout enforcement
- **Execution**: Order validation, deterministic safety checks

See `AGENTS.md` for the full AI agent behavior contract.
