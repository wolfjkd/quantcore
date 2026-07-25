import pytest
import random
from quantcore.indicators import ma, macd, kdj, rsi, boll, atr
from quantcore.metrics import sharpe_ratio, max_drawdown


def generate_closes(length=1000):
    return [10 + random.uniform(-0.5, 0.5) for _ in range(length)]


def generate_highs_lows(closes):
    highs = [c + random.uniform(0.1, 0.3) for c in closes]
    lows = [c - random.uniform(0.1, 0.3) for c in closes]
    return highs, lows


def generate_equity_curve(length=252):
    curve = [100000]
    for _ in range(length - 1):
        curve.append(curve[-1] * (1 + random.uniform(-0.02, 0.02)))
    return curve


class TestPerformance:
    def test_ma_performance(self, benchmark):
        closes = generate_closes(1000)
        
        @benchmark
        def run_ma():
            ma(closes, 20)
        
        assert benchmark.stats['mean'] < 0.05
    
    def test_macd_performance(self, benchmark):
        closes = generate_closes(1000)
        
        @benchmark
        def run_macd():
            macd(closes)
        
        assert benchmark.stats['mean'] < 0.05
    
    def test_kdj_performance(self, benchmark):
        closes = generate_closes(1000)
        highs, lows = generate_highs_lows(closes)
        
        @benchmark
        def run_kdj():
            kdj(highs, lows, closes)
        
        assert benchmark.stats['mean'] < 0.05
    
    def test_rsi_performance(self, benchmark):
        closes = generate_closes(1000)
        
        @benchmark
        def run_rsi():
            rsi(closes)
        
        assert benchmark.stats['mean'] < 0.05
    
    def test_boll_performance(self, benchmark):
        closes = generate_closes(1000)
        highs, lows = generate_highs_lows(closes)
        
        @benchmark
        def run_boll():
            boll(highs, lows, closes)
        
        assert benchmark.stats['mean'] < 0.05
    
    def test_atr_performance(self, benchmark):
        closes = generate_closes(1000)
        highs, lows = generate_highs_lows(closes)
        
        @benchmark
        def run_atr():
            atr(highs, lows, closes)
        
        assert benchmark.stats['mean'] < 0.05
    
    def test_sharpe_ratio_performance(self, benchmark):
        equity = generate_equity_curve(252)
        
        @benchmark
        def run_sharpe():
            sharpe_ratio(equity)
        
        assert benchmark.stats['mean'] < 0.01
    
    def test_max_drawdown_performance(self, benchmark):
        equity = generate_equity_curve(252)
        
        @benchmark
        def run_max_dd():
            max_drawdown(equity)
        
        assert benchmark.stats['mean'] < 0.01