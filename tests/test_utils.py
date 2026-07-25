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
        # 周二，非节假日
        assert is_trading_day('2024-01-02') == True

    def test_is_trading_day_weekend(self):
        # 周六
        assert is_trading_day('2024-01-06') == False

    def test_is_trading_day_holiday_new_year(self):
        # 元旦休市
        assert is_trading_day('2024-01-01') == False

    def test_is_trading_day_holiday_spring_festival(self):
        # 春节休市
        assert is_trading_day('2024-02-10') == False

    def test_is_trading_day_holiday_national_day(self):
        # 国庆休市
        assert is_trading_day('2024-10-01') == False

    def test_is_trading_day_with_date_object(self):
        # date 对象入参
        assert is_trading_day(date(2024, 1, 2)) == True
        assert is_trading_day(date(2024, 1, 1)) == False

    def test_is_trading_day_2025_holidays(self):
        # 2025 春节
        assert is_trading_day('2025-01-28') == False
        # 2025 中秋+国庆连休
        assert is_trading_day('2025-10-08') == False

    def test_is_trading_day_2026_holidays(self):
        # 2026 元旦连休
        assert is_trading_day('2026-01-03') == False
        # 2026 春节
        assert is_trading_day('2026-02-20') == False

    def test_get_trading_days(self):
        result = get_trading_days('2024-01-01', '2024-01-07')
        # 1/2 周二 交易日
        assert '2024-01-02' in result
        # 1/6 周六 非交易日
        assert '2024-01-06' not in result
        # 1/1 元旦休市
        assert '2024-01-01' not in result

    def test_get_trading_days_with_date_objects(self):
        start = date(2024, 1, 1)
        end = date(2024, 1, 7)
        result = get_trading_days(start, end)
        assert '2024-01-02' in result
        assert '2024-01-01' not in result