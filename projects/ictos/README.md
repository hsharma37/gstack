# ICTOS — Phase 3 Analytics & Research Engine

> **TechCEO** project powered by [gstack](https://github.com/garrytan/gstack)

This is the **ICTOS (ICT Operating System)** Phase 3 implementation — a quantitative research and analytics platform for ICT-methodology traders, integrated into the gstack/TechCEO AI engineering workflow.

---

## Quick Start

```bash
# 1. Start the full stack
cd projects/ictos
docker compose up --build

# 2. Or start services individually
make dev          # Postgres + Redis + backend + frontend
make backend      # Backend only (FastAPI + Uvicorn)
make frontend     # Frontend only (Vite dev server)
make test         # Run pytest suite
```

### Services

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:4173 | React SPA (Dashboard, Analytics, Research, Journal, Plans) |
| Backend API | http://localhost:8000/api/v1 | FastAPI with auto-generated docs at `/docs` |
| PostgreSQL | localhost:5432 | Primary database (ictos/ictos) |
| Redis | localhost:6379 | Cache & pub/sub |

---

## Project Structure

```
projects/ictos/
├── backend/                 # FastAPI + SQLModel + PostgreSQL/SQLite
│   ├── app/
│   │   ├── main.py          # FastAPI app entry with CORS + health checks
│   │   ├── config.py        # Pydantic settings (dual DB support)
│   │   ├── database.py      # SQLModel engine + session dependency
│   │   ├── models/          # SQLModel table definitions
│   │   │   ├── trade.py
│   │   │   ├── trading_plan.py
│   │   │   ├── journal_entry.py
│   │   │   └── daily_risk_ledger.py
│   │   ├── services/        # Business logic layer
│   │   │   ├── analytics_service.py   # Expectancy, heatmap, confluence, drawdown, Kelly
│   │   │   ├── research_service.py    # vectorbt, Monte Carlo, Backtrader
│   │   │   ├── risk_service.py        # Position sizing, daily risk validation
│   │   │   ├── execution_service.py   # Order validation
│   │   │   └── trade_service.py       # Trade CRUD + analytics aggregation
│   │   └── api/v1/          # REST route definitions
│   │       ├── analytics.py
│   │       ├── research.py
│   │       ├── trades.py
│   │       ├── plans.py
│   │       ├── journal.py
│   │       ├── risk.py
│   │       └── health.py
│   ├── tests/               # Pytest suite
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
│
├── frontend/                # React 18 + Vite + TypeScript
│   ├── src/
│   │   ├── App.tsx          # React Router SPA with 5 routes
│   │   ├── api/client.ts    # Axios-based API client
│   │   ├── hooks/           # Custom React hooks (useAnalytics, useTrades)
│   │   └── pages/           # Route-level pages
│   │       ├── Dashboard.tsx
│   │       ├── Analytics.tsx
│   │       ├── Research.tsx
│   │       ├── Journal.tsx
│   │       └── Plans.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml       # Full stack: Postgres + Redis + Backend + Frontend
├── Makefile                 # Dev shortcuts (make dev, make test, make docker)
├── .env.example             # Environment template
│
└── docs/                    # Architecture & planning documents
    ├── AGENTS.md            # AI agent safety contract
    ├── CLAUDE.md            # TechCEO skill routing (gstack)
    ├── ICTOS_OVERVIEW.md    # Executive summary
    ├── MIGRATION_ROADMAP.md # 4-phase migration plan
    └── ARCHITECTURE.md      # Full technical architecture
```

---

## What's New in This Enhanced Phase 3

### Backend Enhancements

| Feature | Original | Enhanced |
|---------|----------|----------|
| Database | SQLite only | PostgreSQL + SQLite dual support |
| Models | 1 model (Trade) | 4 models (Trade, TradingPlan, JournalEntry, DailyRiskLedger) |
| Analytics | expectancy, heatmap, kelly | + confluence scoring, drawdown analysis, R-factor |
| Research | Pure stubs | Real vectorbt SMA crossover, numpy Monte Carlo, Backtrader strategy |
| Risk | Missing | Position sizing calculator + daily risk validation |
| Execution | Missing | Order validation with deterministic safety rules |
| API | 2 routers | 7 routers (analytics, research, trades, plans, journal, risk, health) |
| Tests | Empty | 8+ pytest tests covering analytics, research, and risk |

### Frontend Enhancements

| Feature | Original | Enhanced |
|---------|----------|----------|
| Routing | Tab switching | React Router with 5 routes |
| Charts | None | Recharts bar charts for session heatmap |
| API Client | Raw fetch | Axios with error interceptors |
| State | useState only | Custom hooks with async data loading |
| Pages | 2 (Analytics, Research) | 5 (Dashboard, Analytics, Research, Journal, Plans) |
| Styling | Inline styles | Consistent card-based design with responsive grid |

### Infrastructure

| Feature | Original | Enhanced |
|---------|----------|----------|
| Containers | None | Docker Compose with 4 services |
| Dev Tools | None | Makefile with dev, test, docker commands |
| Proxy | Vite proxy | Nginx reverse proxy for production |

---

## API Reference

### Analytics
- `GET /api/v1/analytics/expectancy` — Trade expectancy, win rate, avg R, R-factor
- `GET /api/v1/analytics/heatmap` — Session performance heatmap
- `GET /api/v1/analytics/kelly` — Kelly Criterion position sizing
- `GET /api/v1/analytics/confluence` — ICT concept confluence scoring
- `GET /api/v1/analytics/drawdown` — Max drawdown + equity curve

### Research
- `POST /api/v1/research/backtest` — vectorbt SMA crossover backtest
- `POST /api/v1/research/montecarlo` — Monte Carlo risk simulation
- `POST /api/v1/research/backtrader` — Backtrader event-driven simulation

### Risk
- `POST /api/v1/risk/position-size` — Calculate lot size from risk parameters
- `POST /api/v1/risk/validate-daily` — Check daily risk limits & lockouts

### CRUD
- `GET/POST /api/v1/trades/` — Trade management
- `GET/POST /api/v1/plans/` — Trading plan management
- `GET/POST /api/v1/journal/` — Journal entry management

---

## Safety & AI Agent Rules

This project follows the **ICTOS Safety Contract** (see `AGENTS.md`):

- **AI never executes trades** — Deterministic Python guards every order path
- **Daily loss limits are immutable** — No config toggle can override `risk_service.py`
- **Protected paths require `/guard`** — `risk_service.py`, `execution_service.py`, `mt5-bridge/`
- **All execution changes require human sign-off** — PR process + security audit (`/cso`)

---

## TechCEO Workflow

This project is managed using gstack's AI engineering workflow:

```bash
/office-hours    → Define the research question
/spec            → Backlog-ready spec with test criteria
/plan-eng-review → Data flow, diagrams, failure modes
[implement]
/review          → Structural + correctness review
/qa              → Browser QA of pages
/benchmark       → Verify backtest performance targets
/ship            → Tests, PR, merge
```

---

## Next Steps

1. **Seed test data** — Add sample trades to verify analytics accuracy
2. **Connect MT5 bridge** — Implement real-time trade ingestion
3. **Add charting library** — TradingView Lightweight Charts for price action
4. **Implement RAG pipeline** — Phase 2: Ollama + Haystack + LangGraph
5. **Add CI/CD** — GitHub Actions for pytest, build, and lint

---

**Related**: [ARCHITECTURE.md](ARCHITECTURE.md) | [MIGRATION_ROADMAP.md](MIGRATION_ROADMAP.md) | [AGENTS.md](AGENTS.md) | [CLAUDE.md](CLAUDE.md)
