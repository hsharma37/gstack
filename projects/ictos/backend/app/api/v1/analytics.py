from fastapi import APIRouter
from typing import Any
from ...services.trade_service import (
    calculate_trade_expectancy,
    calculate_trade_heatmap,
    calculate_trade_kelly,
    calculate_trade_confluence,
    calculate_trade_drawdown,
)

router = APIRouter()

@router.get("/expectancy")
async def get_expectancy() -> dict[str, Any]:
    return calculate_trade_expectancy()

@router.get("/sessions")
async def get_sessions() -> dict[str, Any]:
    return calculate_trade_heatmap()

@router.get("/heatmap")
async def get_heatmap() -> dict[str, Any]:
    return calculate_trade_heatmap()

@router.get("/kelly")
async def get_kelly() -> dict[str, Any]:
    return calculate_trade_kelly()

@router.get("/confluence")
async def get_confluence() -> dict[str, Any]:
    return calculate_trade_confluence()

@router.get("/drawdown")
async def get_drawdown() -> dict[str, Any]:
    return calculate_trade_drawdown()
