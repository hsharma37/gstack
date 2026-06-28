# ICTOS — ICT Operating System

> **Version**: 1.0
> **Date**: 2026-06-28
> **Status**: Phase 3 Active — Analytics + Research Engine

---

## What is ICTOS?

**ICTOS** is the ICT Operating System — an evolution of the ICT Trading OS from a
dashboard into a full research and execution operating system for ICT-methodology
traders.

| Layer | What it is |
|-------|-----------|
| Phase 1 Foundation | React + FastAPI + PostgreSQL + WebSockets + MT5 bridge |
| Phase 2 AI Knowledge Brain | Ollama + RAG + LangGraph + Haystack + AI chat |
| **Phase 3 Analytics + Research Engine** | **vectorbt + Backtrader + analytics engine (ICTOS core)** |
| Phase 4 Execution Hardening | Event bus + alerts + fail-safes + semi-automation |

ICTOS is not just a dashboard. It is a repeatable research operating system where
every ICT hypothesis — MSS confluence, FVG entry timing, killzone performance,
order block reliability — can be backtested, measured, and fed back into the
trading plan.

---

## TechCEO: How ICTOS Is Built

ICTOS uses [gstack](https://github.com/garrytan/gstack) as its "TechCEO" — a
structured AI engineering workflow that drives every feature through a disciplined
sprint lifecycle:

```
Think → Plan → Build → Review → Test → Ship → Reflect
```

Every Phase 3 feature follows this ritual:

```
/office-hours    →  define the research question precisely
/spec            →  backlog-ready spec with test criteria
/plan-eng-review →  data flow, sequence diagrams, failure modes
[implement]
/review          →  structural + correctness review
/qa              →  browser QA of Analytics/Research pages
/benchmark       →  verify backtest performance targets
/ship            →  tests, PR, merge
/document-release →  keep docs in sync
```

See `CLAUDE.md` for the full skill routing table and safety rules.

---

## Phase 3: ICTOS Analytics + Research Engine

Phase 3 turns ICTOS into a quantitative research platform for ICT trading.

### Analytics Engine (`analytics_service`)

Answers the question: **"How is my trading performing, and why?"**

| Metric | Description |
|--------|-------------|
| Expectancy | Expected R per trade, filtered by session / pair / setup type |
| Win Rate | Percentage of winning trades, segmented by ICT concept |
| R-Factor | Average win-to-loss R ratio |
| Session Heatmap | Time-of-day and day-of-week performance patterns |
| Confluence Scoring | Which ICT concept combinations correlate with higher R |
| Drawdown Analysis | Max drawdown, equity curve simulation, drawdown duration |

API endpoints:
- `GET /api/v1/analytics/expectancy`
- `GET /api/v1/analytics/sessions`
- `GET /api/v1/analytics/heatmap`
- `GET /api/v1/analytics/confluence`
- `GET /api/v1/analytics/drawdown`

### Research Engine (`research_service`)

Answers the question: **"Does this ICT hypothesis hold up under backtesting?"**

| Tool | Use case |
|------|----------|
| vectorbt | Fast exploratory backtesting, parameter sweeps, signal research |
| Backtrader | Event-driven simulation with slippage, commission, fill models |
| Monte Carlo | Trade sequence simulation for risk-of-ruin and edge validation |
| Kelly Criterion | Position sizing optimization from historical edge data |
| Walk-forward | Out-of-sample validation framework |

API endpoints:
- `POST /api/v1/research/backtest` — run a vectorbt or Backtrader backtest
- `POST /api/v1/research/montecarlo` — Monte Carlo simulation
- `GET /api/v1/research/kelly` — Kelly position sizing from trade history
- `GET /api/v1/research/results` — saved backtest results

### ICT Concept Definitions

All analytics and research correctly map ICT methodology:

| Concept | Definition used in code |
|---------|------------------------|
| MSS | Market Structure Shift — a structural break (swing high/low violation) confirming directional bias |
| FVG | Fair Value Gap — a 3-candle imbalance where candle 1 and 3 do not overlap |
| OB | Order Block — the last opposing candle before an MSS, treated as institutional origin |
| Killzone | Time window: London 02:00–05:00 ET, NY AM 07:00–10:00 ET, Asia 20:00–00:00 ET |
| Confluence | Integer count of ICT concepts aligned at a given entry (MSS + FVG + OB = 3) |

---

## Safety Contract

ICTOS is a personal trading workstation. Capital safety is non-negotiable.

| Rule | Enforcement |
|------|------------|
| AI never executes trades | Deterministic Python guards every order path |
| Daily loss limits cannot be overridden | Hardcoded in `risk_service.py`; no config toggle |
| Protected modules require /review + /cso | Enforced via `AGENTS.md` and `CLAUDE.md` |
| All execution changes require human sign-off | PR process + `/guard` during editing |

---

## Repository Structure

```
ICTOS/
├── CLAUDE.md               ← TechCEO config (gstack skills + ICTOS rules)
├── AGENTS.md               ← AI agent behavior contract
├── ARCHITECTURE.md         ← Full technical architecture
├── MIGRATION_ROADMAP.md    ← 4-phase migration plan
├── ICTOS_OVERVIEW.md       ← This file
│
├── backend/                ← FastAPI + SQLModel + Alembic
│   └── app/
│       ├── services/
│       │   ├── analytics_service.py     ← Phase 3: ICTOS Analytics Engine
│       │   ├── research_service.py      ← Phase 3: ICTOS Research Engine
│       │   ├── risk_service.py          ← PROTECTED: deterministic risk rules
│       │   └── execution_service.py     ← PROTECTED: order execution
│       └── api/v1/
│           ├── analytics.py
│           └── research.py
│
├── frontend/               ← React + Vite + TypeScript
│   └── src/pages/
│       ├── Analytics.tsx   ← Phase 3: Analytics page
│       └── Research.tsx    ← Phase 3: Research page
│
└── mt5-bridge/             ← PROTECTED: MT5 order bridge
```

---

## Quickstart

```bash
# Install gstack (required for all AI-assisted work)
git clone --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup

# Start ICTOS
cd /path/to/ICTOS
docker compose up

# Start a new Phase 3 feature with TechCEO
# Open Claude Code, then:
# /office-hours
```

---

## Related Documents

- [ARCHITECTURE.md](ARCHITECTURE.md) — Full stack architecture and service contracts
- [MIGRATION_ROADMAP.md](MIGRATION_ROADMAP.md) — Phase 1–4 milestones and success criteria
- [CLAUDE.md](CLAUDE.md) — TechCEO skill routing, gstack config, dev commands
- [AGENTS.md](AGENTS.md) — AI agent behavior rules and safety contract
