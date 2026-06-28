from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class DailyRiskLedger(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(index=True, unique=True)
    starting_balance: float
    daily_pnl: float = Field(default=0.0)
    daily_loss_limit: float
    trades_taken: int = Field(default=0)
    max_trades: int = Field(default=5)
    locked_out: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
