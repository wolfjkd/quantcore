import pytest
from quantcore.indicators import ma, ema, sma, wma, macd, kdj, rsi, boll, atr, vol_ma


class TestIndicators:
    @pytest.fixture
    def sample_closes(self):
        return [10.0, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 11.0]
    
    @pytest.fixture
    def sample_highs(self):
        return [10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 11.0, 11.1, 11.2]
    
    @pytest.fixture
    def sample_lows(self):
        return [9.8, 9.9, 10.0, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8]
    
    @pytest.fixture
    def sample_volumes(self):
        return [1000, 1200, 800, 1500, 1100, 900, 1300, 1400, 1600, 1200]
    
    def test_sma(self, sample_closes):
        result = sma(sample_closes, 5)
        assert len(result) == 7
        assert abs(result[-1] - 10.8) < 0.01
    
    def test_ema(self, sample_closes):
        result = ema(sample_closes, 5)
        assert len(result) == 7
    
    def test_ma_sma(self, sample_closes):
        result = ma(sample_closes, 5, 'sma')
        assert len(result) == 7
    
    def test_ma_ema(self, sample_closes):
        result = ma(sample_closes, 5, 'ema')
        assert len(result) == 7
    
    def test_ma_wma(self, sample_closes):
        result = ma(sample_closes, 5, 'wma')
        assert len(result) == 7
    
    def test_macd(self, sample_closes):
        result = macd(sample_closes)
        assert 'dif' in result
        assert 'dea' in result
        assert 'bar' in result
    
    def test_kdj(self, sample_highs, sample_lows, sample_closes):
        result = kdj(sample_highs, sample_lows, sample_closes, n=9)
        assert 'k' in result
        assert 'd' in result
        assert 'j' in result
        assert len(result['k']) == 11
    
    def test_kdj_length_mismatch(self, sample_highs, sample_lows):
        with pytest.raises(ValueError):
            kdj(sample_highs[:-1], sample_lows, sample_highs)
    
    def test_rsi(self, sample_closes):
        result = rsi(sample_closes, 5)
        assert len(result) == 6
        for r in result:
            assert 0 <= r <= 100
    
    def test_boll(self, sample_highs, sample_lows, sample_closes):
        result = boll(sample_highs, sample_lows, sample_closes, 5)
        assert 'mid' in result
        assert 'upper' in result
        assert 'lower' in result
    
    def test_boll_length_mismatch(self, sample_highs, sample_lows):
        with pytest.raises(ValueError):
            boll(sample_highs[:-1], sample_lows, sample_highs)
    
    def test_atr(self, sample_highs, sample_lows, sample_closes):
        result = atr(sample_highs, sample_lows, sample_closes, 5)
        assert len(result) > 0
        for v in result:
            assert v >= 0
    
    def test_atr_length_mismatch(self, sample_highs, sample_lows):
        with pytest.raises(ValueError):
            atr(sample_highs[:-1], sample_lows, sample_highs)
    
    def test_vol_ma(self, sample_volumes):
        result = vol_ma(sample_volumes, 5)
        assert len(result) == 6
    
    def test_sma_short_input(self):
        result = sma([1, 2, 3], 5)
        assert result == []
    
    def test_ema_short_input(self):
        result = ema([1, 2, 3], 5)
        assert result == []
    
    def test_rsi_short_input(self):
        result = rsi([1, 2, 3], 5)
        assert result == []