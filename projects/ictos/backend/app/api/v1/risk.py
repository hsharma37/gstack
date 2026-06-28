from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any
from ...services.risk_service import calculate_position_size, validate_daily_risk

router = APIRouter()

class PositionSizeRequest(BaseModel):
    account_balance: float
    risk_percent: float
    stop_loss_pips: float
    pip_value: float = 10.0

class DailyRiskRequest(BaseModel):
    daily_pnl: float
    daily_loss_limit: float
    trades_taken: int
    max_trades: int

@router.post("/position-size")
async def position_size(request: PositionSizeRequest) -> dict[str, Any]:
    return calculate_position_size(
        request.account_balance,
        request.risk_percent,
        request.stop_loss_pips,
        request.pip_value,
    )

@router.post("/validate-daily")
async def validate_daily(request: DailyRiskRequest) -> dict[str, Any]:
    return validate_daily_risk(
        request.daily_pnl,
        request.daily_loss_limit,
        request.trades_taken,
        request.max_trades,
    )
