from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Trade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True)
    direction: str = Field(default="long", description="long or short")
    entry_time: datetime
    exit_time: Optional[datetime] = None
    entry_price: float = Field(default=0.0)
    exit_price: Optional[float] = None
    pnl: float = Field(default=0.0)
    r_multiple: Optional[float] = None
    session: str = Field(default="unknown", index=True)
    setup: str = Field(default="unknown", description="MSS, FVG, OB, etc.")
    confluence_score: int = Field(default=0, description="Number of aligned concepts")
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    status: str = Field(default="open", description="open, closed, cancelled")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
