from app.services.risk_service import calculate_position_size, validate_daily_risk


def test_calculate_position_size():
    result = calculate_position_size(10000, 0.01, 20)
    assert result["position_size"] > 0
    assert result["risk_amount"] == 100


def test_validate_daily_risk_pass():
    result = validate_daily_risk(-50, 200, 2, 5)
    assert result["locked_out"] is False


def test_validate_daily_risk_locked():
    result = validate_daily_risk(-250, 200, 2, 5)
    assert result["locked_out"] is True
    assert "loss limit" in result["reason"].lower()
