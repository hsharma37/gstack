from fastapi import APIRouter, HTTPException
from typing import List
from sqlmodel import Session, select
from ...models.trade import Trade
from ...database import engine

router = APIRouter()

@router.get("/", response_model=list[Trade])
async def list_trades() -> List[Trade]:
    with Session(engine) as session:
        return session.exec(select(Trade)).all()

@router.get("/{trade_id}", response_model=Trade)
async def get_trade(trade_id: int) -> Trade:
    with Session(engine) as session:
        trade = session.get(Trade, trade_id)
        if not trade:
            raise HTTPException(status_code=404, detail="Trade not found")
        return trade

@router.post("/", response_model=Trade)
async def create_trade(trade: Trade) -> Trade:
    with Session(engine) as session:
        session.add(trade)
        session.commit()
        session.refresh(trade)
        return trade
