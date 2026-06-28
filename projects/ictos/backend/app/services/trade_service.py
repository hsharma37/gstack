from typing import List, Optional
from sqlmodel import Session, select
from .analytics_service import (
    calculate_expectancy,
    calculate_heatmap,
    calculate_kelly,
    calculate_confluence,
    calculate_drawdown,
)
from ..database import engine
from ..models.trade import Trade


def get_all_trades() -> List[Trade]:
    with Session(engine) as session:
        trades = session.exec(select(Trade)).all()
        return trades


def get_trade_by_id(trade_id: int) -> Optional[Trade]:
    with Session(engine) as session:
        return session.get(Trade, trade_id)


def create_trade(trade: Trade) -> Trade:
    with Session(engine) as session:
        session.add(trade)
        session.commit()
        session.refresh(trade)
        return trade


def calculate_trade_expectancy() -> dict:
    trades = [trade.model_dump() for trade in get_all_trades()]
    return calculate_expectancy(trades)


def calculate_trade_heatmap() -> dict:
    trades = [trade.model_dump() for trade in get_all_trades()]
    return calculate_heatmap(trades)


def calculate_trade_kelly() -> dict:
    trades = [trade.model_dump() for trade in get_all_trades()]
    return calculate_kelly(trades)


def calculate_trade_confluence() -> dict:
    trades = [trade.model_dump() for trade in get_all_trades()]
    return calculate_confluence(trades)


def calculate_trade_drawdown() -> dict:
    trades = [trade.model_dump() for trade in get_all_trades()]
    return calculate_drawdown(trades)
