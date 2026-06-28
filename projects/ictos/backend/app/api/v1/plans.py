from fastapi import APIRouter, HTTPException
from typing import List
from sqlmodel import Session, select
from ...models.trading_plan import TradingPlan
from ...database import engine

router = APIRouter()

@router.get("/", response_model=list[TradingPlan])
async def list_plans() -> List[TradingPlan]:
    with Session(engine) as session:
        return session.exec(select(TradingPlan)).all()

@router.post("/", response_model=TradingPlan)
async def create_plan(plan: TradingPlan) -> TradingPlan:
    with Session(engine) as session:
        session.add(plan)
        session.commit()
        session.refresh(plan)
        return plan
