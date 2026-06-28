from app.services.research_service import run_monte_carlo


def test_run_monte_carlo():
    config = {
        "trials": 100,
        "scenario": {
            "win_rate": 0.55,
            "avg_win": 100,
            "avg_loss": 50,
            "num_trades": 50,
            "initial_capital": 10000,
        },
    }
    result = run_monte_carlo(config)
    assert result["status"] == "completed"
    assert "summary" in result
    assert 0 <= result["summary"]["probability_of_ruin"] <= 1
