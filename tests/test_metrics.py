import pytest
from quantcore.metrics import (
    total_return, annualized_return, volatility, downside_volatility,
    sharpe_ratio, sortino_ratio, max_drawdown, calmar_ratio,
    win_rate, profit_factor, expected_return
)


class TestMetrics:
    @pytest.fixture
    def equity_curve_up(self):
        return [100, 105, 108, 112, 115, 120, 125, 130, 135, 140]
    
    @pytest.fixture
    def equity_curve_down(self):
        return [100, 98, 95, 92, 90, 88, 85, 82, 80, 78]
    
    @pytest.fixture
    def equity_curve_flat(self):
        return [100, 100, 100, 100, 100]
    
    @pytest.fixture
    def equity_curve_with_drawdown(self):
        return [100, 105, 110, 108, 105, 102, 105, 110, 115, 120]
    
    @pytest.fixture
    def winning_trades(self):
        return [{'profit': 100}, {'profit': 200}, {'profit': 150}, {'profit': 50}, {'profit': 300}]
    
    @pytest.fixture
    def losing_trades(self):
        return [{'profit': -100}, {'profit': -200}, {'profit': -150}]
    
    @pytest.fixture
    def mixed_trades(self):
        return [
            {'profit': 100}, {'profit': -50}, {'profit': 200},
            {'profit': -80}, {'profit': 150}, {'profit': -30}
        ]
    
    def test_total_return_up(self, equity_curve_up):
        result = total_return(equity_curve_up)
        assert abs(result - 0.4) < 0.01
    
    def test_total_return_down(self, equity_curve_down):
        result = total_return(equity_curve_down)
        assert abs(result + 0.22) < 0.01
    
    def test_total_return_flat(self, equity_curve_flat):
        result = total_return(equity_curve_flat)
        assert result == 0.0
    
    def test_annualized_return(self, equity_curve_up):
        result = annualized_return(equity_curve_up)
        assert result > 0
    
    def test_volatility(self, equity_curve_up):
        result = volatility(equity_curve_up)
        assert result >= 0
    
    def test_downside_volatility(self, equity_curve_down):
        result = downside_volatility(equity_curve_down)
        assert result > 0
    
    def test_sharpe_ratio(self, equity_curve_up):
        result = sharpe_ratio(equity_curve_up)
        assert result > 0
    
    def test_sortino_ratio(self, equity_curve_with_drawdown):
        result = sortino_ratio(equity_curve_with_drawdown)
        assert result >= 0
    
    def test_max_drawdown(self, equity_curve_with_drawdown):
        result = max_drawdown(equity_curve_with_drawdown)
        assert 0 < result < 0.1
    
    def test_max_drawdown_no_dd(self, equity_curve_up):
        result = max_drawdown(equity_curve_up)
        assert result == 0.0
    
    def test_calmar_ratio(self, equity_curve_up):
        result = calmar_ratio(equity_curve_up)
        assert result > 0
    
    def test_win_rate_all_wins(self, winning_trades):
        result = win_rate(winning_trades)
        assert result == 1.0
    
    def test_win_rate_all_losses(self, losing_trades):
        result = win_rate(losing_trades)
        assert result == 0.0
    
    def test_win_rate_mixed(self, mixed_trades):
        result = win_rate(mixed_trades)
        assert result == 0.5
    
    def test_profit_factor_all_wins(self, winning_trades):
        result = profit_factor(winning_trades)
        assert result == float('inf')
    
    def test_profit_factor_all_losses(self, losing_trades):
        result = profit_factor(losing_trades)
        assert result == 0.0
    
    def test_profit_factor_mixed(self, mixed_trades):
        result = profit_factor(mixed_trades)
        assert result > 0
    
    def test_expected_return(self, mixed_trades):
        result = expected_return(mixed_trades)
        assert result > 0
    
    def test_empty_inputs(self):
        assert total_return([]) == 0.0
        assert annualized_return([]) == 0.0
        assert volatility([]) == 0.0
        assert downside_volatility([]) == 0.0
        assert sharpe_ratio([]) == 0.0
        assert sortino_ratio([]) == 0.0
        assert max_drawdown([]) == 0.0
        assert calmar_ratio([]) == 0.0
        assert win_rate([]) == 0.0
        assert profit_factor([]) == 0.0
        assert expected_return([]) == 0.0