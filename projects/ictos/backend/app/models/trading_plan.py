from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class TradingPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(index=True)
    pair: str
    session: str
    bias: str = Field(default="neutral", description="bullish, bearish, neutral")
    key_levels: Optional[str] = None
    setup_conditions: Optional[str] = None
    risk_per_trade: float = Field(default=0.01, description="Risk as fraction of account")
    max_trades: int = Field(default=3)
    notes: Optional[str] = None
    grade: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
