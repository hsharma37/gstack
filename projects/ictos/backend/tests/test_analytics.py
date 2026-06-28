from app.services.analytics_service import (
    calculate_expectancy,
    calculate_heatmap,
    calculate_kelly,
    calculate_confluence,
    calculate_drawdown,
)


def test_calculate_expectancy():
    trades = [
        {"pnl": 100, "session": "london", "confluence_score": 2, "entry_time": "2024-01-01T10:00:00"},
        {"pnl": -50, "session": "ny", "confluence_score": 1, "entry_time": "2024-01-02T10:00:00"},
        {"pnl": 200, "session": "london", "confluence_score": 3, "entry_time": "2024-01-03T10:00:00"},
    ]
    result = calculate_expectancy(trades)
    assert result["trades"] == 3
    assert result["win_rate"] == 2 / 3
    assert result["expectancy"] > 0


def test_calculate_expectancy_empty():
    result = calculate_expectancy([])
    assert result["trades"] == 0
    assert result["expectancy"] == 0.0


def test_calculate_heatmap():
    trades = [
        {"pnl": 100, "session": "london"},
        {"pnl": -50, "session": "london"},
        {"pnl": 200, "session": "ny"},
    ]
    result = calculate_heatmap(trades)
    assert result["sessions"]["london"]["count"] == 2
    assert result["sessions"]["ny"]["count"] == 1


def test_calculate_kelly():
    trades = [
        {"pnl": 100},
        {"pnl": -50},
        {"pnl": 100},
    ]
    result = calculate_kelly(trades)
    assert 0 <= result["kelly_fraction"] <= 1


def test_calculate_confluence():
    trades = [
        {"pnl": 100, "confluence_score": 2},
        {"pnl": -50, "confluence_score": 2},
        {"pnl": 200, "confluence_score": 3},
    ]
    result = calculate_confluence(trades)
    assert 2 in result["confluence_scores"]
    assert 3 in result["confluence_scores"]


def test_calculate_drawdown():
    trades = [
        {"pnl": 100, "entry_time": "2024-01-01"},
        {"pnl": -150, "entry_time": "2024-01-02"},
        {"pnl": 200, "entry_time": "2024-01-03"},
    ]
    result = calculate_drawdown(trades)
    assert result["max_drawdown"] >= 50
    assert len(result["equity_curve"]) == 3
