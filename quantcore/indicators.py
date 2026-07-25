import math


def sma(closes, period):
    if len(closes) < period:
        return []
    result = []
    for i in range(period - 1, len(closes)):
        result.append(sum(closes[i - period + 1:i + 1]) / period)
    return result


def ema(closes, period):
    if len(closes) < period:
        return []
    result = []
    multiplier = 2.0 / (period + 1)
    prev_ema = sum(closes[:period]) / period
    result.append(prev_ema)
    for i in range(period, len(closes)):
        current_ema = closes[i] * multiplier + prev_ema * (1 - multiplier)
        result.append(current_ema)
        prev_ema = current_ema
    return result


def ma(closes, period, method='sma'):
    if method == 'sma':
        return sma(closes, period)
    elif method == 'ema':
        return ema(closes, period)
    elif method == 'wma':
        return wma(closes, period)
    else:
        return sma(closes, period)


def wma(closes, period):
    if len(closes) < period:
        return []
    result = []
    weight_sum = sum(range(1, period + 1))
    for i in range(period - 1, len(closes)):
        weighted_sum = sum(closes[i - period + 1 + j] * (j + 1) for j in range(period))
        result.append(weighted_sum / weight_sum)
    return result


def macd(closes, fast_period=12, slow_period=26, signal_period=9):
    if len(closes) < slow_period:
        return {'dif': [], 'dea': [], 'bar': []}
    
    fast_ema = ema(closes, fast_period)
    slow_ema = ema(closes, slow_period)
    
    dif = []
    start_idx = len(fast_ema) - len(slow_ema)
    for i in range(len(slow_ema)):
        dif.append(fast_ema[i + start_idx] - slow_ema[i])
    
    dea = ema(dif, signal_period)
    
    bar = []
    start_idx_dea = len(dif) - len(dea)
    for i in range(len(dea)):
        bar.append(dif[i + start_idx_dea] - dea[i])
    
    return {'dif': dif, 'dea': dea, 'bar': bar}


def kdj(highs, lows, closes, n=9, m1=3, m2=3):
    if len(highs) != len(lows) or len(lows) != len(closes):
        raise ValueError("highs, lows, closes must have same length")
    if len(closes) < n:
        return {'k': [], 'd': [], 'j': []}
    
    k = []
    d = []
    j = []
    prev_k = 50.0
    prev_d = 50.0
    
    for i in range(len(closes)):
        ll = min(lows[max(0, i - n + 1):i + 1])
        hh = max(highs[max(0, i - n + 1):i + 1])
        den = hh - ll
        rsv = 50.0 if den == 0.0 else ((closes[i] - ll) / den * 100.0)
        
        prev_k = (2.0 / m1) * prev_k + (1.0 / m1) * rsv
        prev_d = (2.0 / m2) * prev_d + (1.0 / m2) * prev_k
        j_val = 3 * prev_k - 2 * prev_d
        
        k.append(prev_k)
        d.append(prev_d)
        j.append(j_val)
    
    return {'k': k, 'd': d, 'j': j}


def rsi(closes, period=14):
    if len(closes) < period + 1:
        return []
    
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    
    avg_gain = sum(d for d in deltas[:period] if d > 0) / period
    avg_loss = abs(sum(d for d in deltas[:period] if d < 0)) / period
    
    result = []
    for i in range(period - 1, len(deltas)):
        delta = deltas[i]
        avg_gain = (avg_gain * (period - 1) + max(delta, 0)) / period
        avg_loss = (avg_loss * (period - 1) + abs(min(delta, 0))) / period
        
        rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
        result.append(100 - 100 / (1 + rs))
    
    return result


def boll(highs, lows, closes, period=20, num_std=2):
    if len(highs) != len(lows) or len(lows) != len(closes):
        raise ValueError("highs, lows, closes must have same length")
    if len(closes) < period:
        return {'mid': [], 'upper': [], 'lower': []}
    
    mid = sma(closes, period)
    upper = []
    lower = []
    
    for i in range(len(mid)):
        start = i
        end = start + period
        if end > len(closes):
            break
        prices = closes[start:end]
        mean = mid[i]
        variance = sum((p - mean) ** 2 for p in prices) / period
        std = math.sqrt(variance)
        upper.append(mean + num_std * std)
        lower.append(mean - num_std * std)
    
    return {'mid': mid[:len(upper)], 'upper': upper, 'lower': lower}


def atr(highs, lows, closes, period=14):
    if len(highs) != len(lows) or len(lows) != len(closes):
        raise ValueError("highs, lows, closes must have same length")
    if len(closes) < period:
        return []
    
    tr_values = []
    for i in range(1, len(closes)):
        tr1 = highs[i] - lows[i]
        tr2 = abs(highs[i] - closes[i - 1])
        tr3 = abs(lows[i] - closes[i - 1])
        tr_values.append(max(tr1, tr2, tr3))
    
    atr_values = ema(tr_values, period)
    return atr_values


def vol_ma(volumes, period=5):
    return sma(volumes, period)