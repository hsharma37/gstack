from typing import Any
from datetime import datetime


def validate_order(order: dict[str, Any]) -> dict[str, Any]:
    """Validate a trade order before execution."""
    errors = []

    if not order.get("symbol"):
        errors.append("Symbol is required")
    if order.get("position_size", 0) <= 0:
        errors.append("Position size must be positive")
    if order.get("stop_loss", 0) <= 0:
        errors.append("Stop loss is required")
    if order.get("direction") not in ["long", "short"]:
        errors.append("Direction must be 'long' or 'short'")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "order": order,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
