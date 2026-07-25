import math
from datetime import date, timedelta


TRADING_CALENDAR = set()


def load_trading_calendar(calendar_file=None):
    if calendar_file:
        with open(calendar_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    TRADING_CALENDAR.add(line)


def is_trading_day(d):
    if isinstance(d, date):
        d = d.strftime('%Y-%m-%d')
    return d in TRADING_CALENDAR


def get_trading_days(start_date, end_date):
    if isinstance(start_date, date):
        start_date = start_date.strftime('%Y-%m-%d')
    if isinstance(end_date, date):
        end_date = end_date.strftime('%Y-%m-%d')
    
    result = []
    current = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    
    while current <= end:
        if current.weekday() < 5:
            result.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    
    return result


def zscore(values):
    if len(values) == 0:
        return []
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std = math.sqrt(variance)
    if std == 0:
        return [0.0] * len(values)
    return [(v - mean) / std for v in values]


def normalize(values, method='zscore'):
    if len(values) == 0:
        return []
    
    if method == 'zscore':
        return zscore(values)
    elif method == 'minmax':
        min_val = min(values)
        max_val = max(values)
        if max_val == min_val:
            return [0.0] * len(values)
        return [(v - min_val) / (max_val - min_val) for v in values]
    elif method == 'rank':
        sorted_vals = sorted(values)
        ranks = [sorted_vals.index(v) / (len(sorted_vals) - 1) if len(sorted_vals) > 1 else 0.5 for v in values]
        return ranks
    else:
        return zscore(values)


def median(values):
    if len(values) == 0:
        return 0.0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n % 2 == 0:
        return (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
    else:
        return sorted_vals[n // 2]