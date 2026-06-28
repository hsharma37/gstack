# ICT Trading OS — Migration Roadmap

> **Version**: 1.0
> **Date**: 2026-06-26
> **Status**: Phase 1 Ready

---

## Overview

This document defines the **4-phase migration** from the current HTML-first prototype (`ICT_Trading_OS_v7.html`) to a modern **React + FastAPI + PostgreSQL + AI** architecture.

Each phase is designed to be **independently deployable and functional**, so you can use the system at every milestone without waiting for the full rewrite.

---

## Phase 0: Current State (Baseline)

### What Exists Today

| Component | Status | Notes |
|-----------|--------|-------|
| `ICT_Trading_OS_v7.html` | ✅ Single-file dashboard | All UI, logic, and state in one HTML file (~300KB) |
| `server.js` | ✅ Basic API | Market data, trade CRUD, MT5 proxy |
| `mt5bridgeScript.py` | ✅ MT5 bridge | Order execution + Telegram notifications |
| `.env` + `.env.example` | ✅ Config | Manual env variable management |
| Knowledge Base | ✅ localStorage only | Transcript chunks survive browser restart |
| Lot Calculator | ✅ Leverage 1-100x | Slider-based, affects all calculations |
| Telegram | ✅ Bot integration | Test endpoint + debug logging |
| SQLite | ⚠️ Ad-hoc | No migrations, no schema definition |

### Pain Points to Solve

1. **Business logic lives in HTML/JS** — position sizing, risk rules, and planner logic are browser-side.
2. **No schema evolution** — adding a new field means manual localStorage or SQLite patching.
3. **No real-time updates** — manual refresh for price, trades, and alerts.
4. **AI is ad-hoc** — no structured RAG pipeline, no vector search, no agent orchestration.
5. **Testing is manual** — no unit tests, no CI, no reproducible builds.
6. **Single file limit** — ~300KB HTML is becoming unmaintainable; adding features is painful.
7. **No concurrent access** — SQLite locks, no multi-process safety.

---

## Phase 1: Product Foundation (Weeks 1-4)

**Goal**: Extract the current UI into a proper React frontend, move domain logic into FastAPI, replace SQLite with PostgreSQL, and establish real-time updates via WebSockets.

### 1.1 Project Structure

```
ict-os/
├── docker-compose.yml          # Local orchestration
├── .env                        # Centralized config
├── .env.example                # Template for new setups
├── Makefile                    # Common dev commands
│
├── frontend/                   # React + Vite + TypeScript
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── main.tsx            # App entry
│   │   ├── App.tsx             # Router + layout
│   │   ├── components/         # Reusable UI components
│   │   │   ├── ui/             # shadcn/ui primitives
│   │   │   ├── charts/         # TradingView + ECharts wrappers
│   │   │   ├── tables/         # TanStack Table configs
│   │   │   └── forms/          # Form components
│   │   ├── pages/              # Route-level pages
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Plan.tsx
│   │   │   ├── Execute.tsx
│   │   │   ├── Journal.tsx
│   │   │   ├── Knowledge.tsx
│   │   │   ├── Analytics.tsx
│   │   │   └── Settings.tsx
│   │   ├── hooks/              # Custom React hooks
│   │   │   ├── useMarketData.ts
│   │   │   ├── useTrades.ts
│   │   │   └── useWebSocket.ts
│   │   ├── stores/             # Zustand stores
│   │   │   ├── uiStore.ts
│   │   │   └── authStore.ts
│   │   ├── api/                # TanStack Query + API clients
│   │   │   ├── client.ts       # Axios/fetch setup
│   │   │   ├── queries/        # Query definitions
│   │   │   └── mutations/      # Mutation definitions
│   │   ├── types/              # TypeScript interfaces
│   │   └── utils/              # Helpers, formatters
│   └── public/
│       └── favicon.ico
│
├── backend/                    # FastAPI + SQLModel + Alembic
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── alembic/
│   │   ├── env.py
│   │   ├── versions/           # Migration files
│   │   └── script.py.mako
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app entry
│   │   ├── config.py           # Pydantic settings
│   │   ├── database.py         # SQLModel engine + session
│   │   ├── models/             # SQLModel table definitions
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── plan.py
│   │   │   ├── trade.py
│   │   │   ├── journal.py
│   │   │   └── kb.py
│   │   ├── schemas/            # Pydantic request/response models
│   │   │   ├── __init__.py
│   │   │   ├── plan_schemas.py
│   │   │   ├── trade_schemas.py
│   │   │   └── journal_schemas.py
│   │   ├── api/                # Route definitions
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── plans.py
│   │   │   │   ├── trades.py
│   │   │   │   ├── risk.py
│   │   │   │   ├── journal.py
│   │   │   │   ├── market.py
│   │   │   │   ├── analytics.py
│   │   │   │   ├── telegram.py
│   │   │   │   └── mt5.py
│   │   │   └── websocket.py    # WebSocket endpoints
│   │   ├── services/           # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── planner_service.py
│   │   │   ├── execution_service.py
│   │   │   ├── risk_service.py
│   │   │   ├── journal_service.py
│   │   │   ├── market_data_service.py
│   │   │   ├── telegram_service.py
│   │   │   └── analytics_service.py
│   │   ├── core/               # Shared utilities
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   └── tests/              # Pytest suite
│   │       ├── __init__.py
│   │       ├── test_plans.py
│   │       ├── test_trades.py
│   │       └── test_risk.py
│   └── scripts/
│       ├── init_db.py          # Seed initial data
│       └── migrate_data.py     # Migrate from old SQLite/localStorage
│
├── mt5-bridge/                 # MT5 bridge (refactored from current)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── mt5_bridge.py           # Main bridge script
│   ├── telegram_bot.py         # Telegram notification handler
│   └── config.py               # Bridge config
│
└── infra/                      # Docker, nginx, compose
    ├── docker/
    │   ├── Dockerfile.frontend
    │   └── Dockerfile.backend
    └── nginx/
        └── nginx.conf
```

### 1.2 Milestones

#### Week 1: Scaffold + Database
- Initialize monorepo, Docker Compose with PostgreSQL + Redis + pgvector
- Create SQLModel models for User, TradingPlan, Trade, JournalEntry, DailyRiskLedger
- Initialize Alembic and baseline migration
- Set up Vite + React + TypeScript + Tailwind + shadcn/ui
- Configure TanStack Query and Zustand

#### Week 2: Core API + Frontend Shell
- Implement planner_service + `/api/v1/plans` CRUD
- Implement execution_service + `/api/v1/trades` CRUD + close
- Implement risk_service + `/api/v1/risk/validate` + lot-size calculator
- Implement journal_service + `/api/v1/journal` CRUD + grading
- Build React layout, Dashboard, Plan, Execute, Journal pages
- Connect frontend to all API endpoints via TanStack Query

#### Week 3: Realtime + MT5 Bridge Integration
- Add WebSocket endpoints for price and trade updates
- Implement Redis pub/sub
- Refactor mt5bridgeScript.py into mt5-bridge/ service
- Add Telegram notifications
- Build Journal page with real-time updates

#### Week 4: Polish + Data Migration
- Migrate data from old SQLite/localStorage to PostgreSQL
- Add analytics_service with expectancy + session stats endpoints
- Build Analytics page
- Add Settings page
- Write Pytest tests, Docker health checks, README

### 1.3 Phase 1 Deliverables
- Docker Compose stack
- React frontend
- FastAPI backend
- PostgreSQL database with Alembic migrations
- MT5 bridge as standalone service
- Telegram integration
- Pytest coverage

---

## Phase 2: Knowledge + AI Brain (Weeks 5-8)

**Goal**: Add AI-powered knowledge system — transcript ingestion, RAG query, vector search, and AI chat for ICT concepts.

#### Week 5: Ingestion Pipeline
- Set up Ollama in Docker Compose
- Add kb_sources and kb_chunks tables with pgvector VECTOR columns
- Build transcript ingestion service (YouTube + manual text)
- Semantic chunking (512 tokens, 50 overlap)
- Generate embeddings via Ollama (nomic-embed-text)
- Build Knowledge page with source uploader

#### Week 6: RAG + Search
- Semantic search over kb_chunks using pgvector cosine similarity
- Build POST /api/v1/kb/search endpoint
- Integrate Haystack retriever pipeline
- Build Knowledge page search panel
- Implement POST /api/v1/kb/query endpoint (RAG)

#### Week 7: LangGraph Orchestration
- Design full LangGraph RAG workflow: query → retrieve → grade → answer → self-correct
- Implement query router, retrieval grading, answer generation
- Implement hallucination check and self-correction loop
- Connect to Ollama LLM (llama3.1:8b)
- Build AI chat UI with streaming responses

#### Week 8: AI Use Cases
- Implement POST /api/v1/agent/grade-setup
- Implement POST /api/v1/agent/journal-review
- Implement POST /api/v1/agent/chat
- Build AI panels in Plan, Journal pages
- Write tests for all AI services (mock LLM for CI)

### 2.2 Phase 2 Deliverables
- Ollama integration
- Haystack pipeline
- LangGraph RAG
- pgvector semantic search
- AI chat panel with citations
- Setup grading + journal review
- Celery workers

---

## Phase 3: Analytics + Research Engine — ICTOS Core (Weeks 9-12)

> **This is where ICT Trading OS becomes ICTOS.**

**Goal**: Add quantitative analytics, research tools, and backtesting capabilities.

#### Week 9: Analytics Engine
- Build analytics_service with core metrics: expectancy, win rate, R-factor, avg R
- Session heatmap analytics (time-of-day, day-of-week)
- Confluence scoring analytics
- Drawdown analysis and equity curve simulation
- Implement endpoints: /api/v1/analytics/expectancy, /sessions, /heatmap
- Build Analytics page with ECharts

#### Week 10: Research Stack (vectorbt)
- Integrate vectorbt for fast backtesting
- Build research_service with hypothesis testing framework
- ICT-derived indicator backtesting (MSS, FVG, OB detection)
- Parameter sweep and optimization
- Build Research page with backtest config + results
- Add Sharpe, Sortino, Calmar ratio calculations
- Monte Carlo simulation for trade sequences
- Walk-forward analysis

#### Week 11: Backtrader Integration
- Integrate Backtrader for event-driven strategy simulation
- Broker-style simulation (slippage, commission, fill models)
- Multi-timeframe analysis
- Strategy template system
- Strategy performance comparison (A/B testing)
- Connect backtest results to journal entries

#### Week 12: Advanced Analytics
- Kelly Criterion calculator
- Risk-of-ruin simulation
- Portfolio-level analytics
- "What-if" scenario analysis
- AI-powered pattern recognition in journal entries
- Automated weekly/monthly performance reports
- Sentiment analysis integration

### 3.3 Phase 3 Deliverables
- Analytics engine
- vectorbt integration
- Backtrader integration
- Research page
- Kelly Criterion
- Monte Carlo
- Performance reports

---

## Phase 4: Execution Hardening + Automation (Weeks 13-16)

**Goal**: Harden execution layer, add alert automation, event bus, and fail-safe guards.

#### Week 13: Event Bus + Alert System
- Centralized event bus (Redis pub/sub + Python dataclasses)
- Define event types: TradeOpened, TradeClosed, AlertTriggered, DailyRiskBreached, PriceUpdate
- Build alert_service with rule engine
- Alert Manager page, WebSocket channel for alerts

#### Week 14: Execution Hardening
- Pre-trade validation checklist
- Replayable audit log
- Order state machine (pending → validated → submitted → filled → closed)
- MT5 bridge health monitoring
- Fail-safe guards: daily lockout, max drawdown halt, connection loss halt
- Manual override system with confirmation + audit logging

#### Week 15: Semi-Automated Decision Support
- "signal → suggestion → human approval → execution" workflow
- AI-generated setup confidence scores
- Confluence scoring automation
- Pre-trade risk summary popup
- Paper trading mode

#### Week 16: Production Hardening
- Comprehensive structured logging
- Prometheus-compatible metrics
- Health checks, graceful shutdown
- Rate limiting, input sanitization
- Integration tests, load tests
- CI/CD pipeline (GitHub Actions)
- PostgreSQL backup strategy

### 4.2 Phase 4 Deliverables
- Event bus, Alert system, Execution hardening, Semi-automation, Paper trading, Production ops, Integration tests

---

## Timeline Summary

| Phase | Duration | Focus | Key Output |
|-------|----------|-------|------------|
| **Phase 1** | Weeks 1-4 | Foundation | React + FastAPI + PostgreSQL + WebSockets + MT5 bridge |
| **Phase 2** | Weeks 5-8 | AI Brain | Ollama + RAG + LangGraph + Haystack + AI chat |
| **Phase 3** | Weeks 9-12 | Analytics | vectorbt + Backtrader + research engine + performance reports |
| **Phase 4** | Weeks 13-16 | Hardening | Event bus + alerts + fail-safes + semi-automation + production ops |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Complexity overwhelm | Each phase independently deployable |
| Data loss during migration | Keep old SQLite as backup; test on copy first |
| Ollama performance on Mac | Use smaller models (8B) first |
| MT5 bridge instability | Maintain current bridge as fallback |
| Frontend rebuild scope | Rebuild one screen at a time |
| Database migration complexity | Use Alembic from day 1 |
| AI hallucination in trading | Never let AI decide execution |
| Dependency conflicts | Pin all versions; use Docker |

---

## Success Criteria by Phase

### Phase 1 Success
- `docker compose up` starts full stack in < 2 minutes
- All current v7 features work in React frontend
- PostgreSQL persists data across restarts
- WebSocket live price updates < 1s latency
- MT5 bridge connects and executes orders
- 80%+ Pytest coverage on services

### Phase 2 Success
- YouTube transcript ingestion in < 5 min/video
- Semantic search in < 2 seconds
- RAG answers with source citations
- AI setup grading gives actionable feedback
- Ollama runs fully offline
- Celery processes jobs without blocking API

### Phase 3 Success
- Expectancy matches manual spreadsheet to 2 decimal places
- vectorbt backtest: 1000 trades in < 30 seconds
- Backtrader produces accurate fill records
- Session heatmap shows actionable patterns
- Kelly calculator suggests safe position sizes
- Research results auto-export to journal tags

### Phase 4 Success
- Alert triggers within 5 seconds
- Daily risk lockout prevents trades after limit
- Audit log captures every state change
- Paper trading mode produces identical logs
- System recovers from MT5 bridge disconnect
- CI/CD passes all tests before deploy
- Database backup runs automatically daily

---

## Next Steps

1. Review this roadmap
2. Approve Phase 1 scope
3. Initialize repo (create branch `phase-1/foundation`)
4. Set up Docker (PostgreSQL + Redis + pgvector)
5. First task: Create monorepo structure and Docker Compose file

---

**Related Documents**: `ARCHITECTURE.md`, `README.md`, `TELEGRAM_SETUP.md`, `MACBOOK-SETUP-GUIDE.md`
