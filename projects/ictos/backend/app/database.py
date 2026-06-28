from sqlmodel import SQLModel, create_engine, Session
from .config import settings

# Import models so SQLModel metadata is populated before creating tables.
from .models.trade import Trade  # noqa: F401
from .models.trading_plan import TradingPlan  # noqa: F401
from .models.journal_entry import JournalEntry  # noqa: F401
from .models.daily_risk_ledger import DailyRiskLedger  # noqa: F401

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, echo=settings.debug, connect_args=connect_args)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
