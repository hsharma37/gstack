from typing import Any
from datetime import datetime


def calculate_expectancy(trades: list[dict[str, Any]]) -> dict[str, Any]:
    wins = [t for t in trades if t.get("pnl", 0) > 0]
    losses = [t for t in trades if t.get("pnl", 0) <= 0]
    total = len(trades)

    if total == 0:
        return {
            "trades": 0,
            "win_rate": 0.0,
            "avg_win": 0.0,
            "avg_loss": 0.0,
            "expectancy": 0.0,
            "r_factor": 0.0,
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

    avg_win = sum(t.get("pnl", 0) for t in wins) / len(wins) if wins else 0.0
    avg_loss = sum(t.get("pnl", 0) for t in losses) / len(losses) if losses else 0.0
    win_rate = len(wins) / total
    expectancy = win_rate * avg_win + (1 - win_rate) * avg_loss

    r_wins = [t.get("r_multiple", 0) for t in wins if t.get("r_multiple")]
    r_losses = [abs(t.get("r_multiple", 0)) for t in losses if t.get("r_multiple")]
    r_factor = (
        (sum(r_wins) / len(r_wins)) / (sum(r_losses) / len(r_losses))
        if r_wins and r_losses and sum(r_losses) > 0
        else 0.0
    )

    return {
        "trades": total,
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "expectancy": expectancy,
        "r_factor": r_factor,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def calculate_heatmap(trades: list[dict[str, Any]]) -> dict[str, Any]:
    buckets: dict[str, dict[str, Any]] = {}
    for trade in trades:
        session = trade.get("session", "unknown")
        if session not in buckets:
            buckets[session] = {"count": 0, "wins": 0, "losses": 0, "pnl": 0.0}
        buckets[session]["count"] += 1
        pnl = trade.get("pnl", 0)
        buckets[session]["pnl"] += pnl
        if pnl > 0:
            buckets[session]["wins"] += 1
        else:
            buckets[session]["losses"] += 1

    for session in buckets:
        count = buckets[session]["count"]
        buckets[session]["win_rate"] = buckets[session]["wins"] / count if count > 0 else 0.0

    return {
        "sessions": buckets,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def calculate_confluence(trades: list[dict[str, Any]]) -> dict[str, Any]:
    """Score which confluence levels correlate with better performance."""
    scores: dict[int, dict[str, Any]] = {}
    for trade in trades:
        score = trade.get("confluence_score", 0)
        if score not in scores:
            scores[score] = {"count": 0, "wins": 0, "total_pnl": 0.0}
        scores[score]["count"] += 1
        pnl = trade.get("pnl", 0)
        scores[score]["total_pnl"] += pnl
        if pnl > 0:
            scores[score]["wins"] += 1

    for score in scores:
        count = scores[score]["count"]
        scores[score]["win_rate"] = scores[score]["wins"] / count if count > 0 else 0.0
        scores[score]["avg_pnl"] = scores[score]["total_pnl"] / count if count > 0 else 0.0

    return {
        "confluence_scores": scores,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def calculate_drawdown(trades: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate max drawdown and drawdown duration from equity curve."""
    if not trades:
        return {
            "max_drawdown": 0.0,
            "max_drawdown_duration": 0,
            "equity_curve": [],
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

    sorted_trades = sorted(trades, key=lambda t: t.get("entry_time", ""))
    equity = 0.0
    peak = 0.0
    max_dd = 0.0
    dd_start = 0
    max_dd_duration = 0
    equity_curve = []

    for i, trade in enumerate(sorted_trades):
        equity += trade.get("pnl", 0)
        equity_curve.append({"trade": i + 1, "equity": equity})
        if equity > peak:
            peak = equity
            dd_start = i
        dd = peak - equity
        if dd > max_dd:
            max_dd = dd
            max_dd_duration = i - dd_start

    return {
        "max_drawdown": max_dd,
        "max_drawdown_duration": max_dd_duration,
        "equity_curve": equity_curve,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def calculate_kelly(trades: list[dict[str, Any]]) -> dict[str, Any]:
    wins = [t for t in trades if t.get("pnl", 0) > 0]
    losses = [t for t in trades if t.get("pnl", 0) <= 0]
    total = len(trades)
    win_rate = len(wins) / total if total > 0 else 0.0
    avg_win = sum(t.get("pnl", 0) for t in wins) / len(wins) if wins else 0.0
    avg_loss = abs(sum(t.get("pnl", 0) for t in losses) / len(losses)) if losses else 0.0

    if total == 0 or avg_win == 0.0:
        fraction = 0.0
    elif not losses:
        fraction = 1.0
    else:
        odds = avg_win / avg_loss if avg_loss > 0 else 0.0
        fraction = win_rate - (1 - win_rate) / odds if odds > 0 else 0.0
    fraction = max(min(fraction, 1.0), 0.0)

    return {
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "kelly_fraction": fraction,
        "kelly_half": fraction / 2,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
