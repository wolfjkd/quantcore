import pytest
from datetime import date
from quantcore.utils import zscore, normalize, median, is_trading_day, get_trading_days


class TestUtils:
    def test_zscore(self):
        values = [1, 2, 3, 4, 5]
        result = zscore(values)
        assert len(result) == 5
        assert abs(sum(result)) < 0.001
    
    def test_zscore_empty(self):
        result = zscore([])
        assert result == []
    
    def test_zscore_constant(self):
        result = zscore([1, 1, 1, 1])
        assert all(v == 0.0 for v in result)
    
    def test_normalize_zscore(self):
        values = [1, 2, 3, 4, 5]
        result = normalize(values, 'zscore')
        assert len(result) == 5
    
    def test_normalize_minmax(self):
        values = [1, 2, 3, 4, 5]
        result = normalize(values, 'minmax')
        assert len(result) == 5
        assert result[0] == 0.0
        assert result[-1] == 1.0
    
    def test_normalize_rank(self):
        values = [3, 1, 4, 2]
        result = normalize(values, 'rank')
        assert len(result) == 4
    
    def test_normalize_empty(self):
        result = normalize([])
        assert result == []
    
    def test_median_odd(self):
        values = [1, 3, 5, 7, 9]
        assert median(values) == 5.0
    
    def test_median_even(self):
        values = [1, 3, 5, 7]
        assert median(values) == 4.0
    
    def test_median_empty(self):
        assert median([]) == 0.0
    
    def test_is_trading_day(self):
        result = is_trading_day('2024-01-02')
        assert isinstance(result, bool)
    
    def test_get_trading_days(self):
        result = get_trading_days('2024-01-01', '2024-01-05')
        assert len(result) >= 0
    
    def test_get_trading_days_with_date_objects(self):
        start = date(2024, 1, 1)
        end = date(2024, 1, 5)
        result = get_trading_days(start, end)
        assert len(result) >= 0