from typing import Any
from datetime import datetime


def calculate_position_size(
    account_balance: float, risk_percent: float, stop_loss_pips: float, pip_value: float = 10.0
) -> dict[str, Any]:
    """Calculate position size based on account risk parameters."""
    risk_amount = account_balance * risk_percent
    position_size = risk_amount / (stop_loss_pips * pip_value) if stop_loss_pips > 0 else 0.0

    return {
        "account_balance": account_balance,
        "risk_percent": risk_percent,
        "risk_amount": risk_amount,
        "stop_loss_pips": stop_loss_pips,
        "pip_value": pip_value,
        "position_size": round(position_size, 2),
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def validate_daily_risk(
    daily_pnl: float, daily_loss_limit: float, trades_taken: int, max_trades: int
) -> dict[str, Any]:
    """Validate if trading should be allowed based on daily risk limits."""
    locked_out = daily_pnl <= -daily_loss_limit or trades_taken >= max_trades

    return {
        "daily_pnl": daily_pnl,
        "daily_loss_limit": daily_loss_limit,
        "trades_taken": trades_taken,
        "max_trades": max_trades,
        "locked_out": locked_out,
        "reason": (
            "Daily loss limit reached"
            if daily_pnl <= -daily_loss_limit
            else ("Max trades reached" if trades_taken >= max_trades else "OK")
        ),
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
