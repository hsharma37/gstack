from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class JournalEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trade_id: Optional[int] = Field(default=None, foreign_key="trade.id", index=True)
    date: datetime = Field(index=True)
    emotions: Optional[str] = None
    what_went_well: Optional[str] = None
    what_to_improve: Optional[str] = None
    setup_quality: Optional[int] = Field(default=None, ge=1, le=10)
    execution_quality: Optional[int] = Field(default=None, ge=1, le=10)
    management_quality: Optional[int] = Field(default=None, ge=1, le=10)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
