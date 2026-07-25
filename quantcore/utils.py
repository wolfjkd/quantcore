import math
from datetime import date, timedelta


TRADING_CALENDAR = set()


# A 股 2024-2026 主要节假日休市日（不含周末，仅法定假日）
# 来源：上交所/深交所公告
_HOLIDAYS = {
    # 2024
    '2024-01-01',                         # 元旦
    '2024-02-09', '2024-02-10', '2024-02-11', '2024-02-12', '2024-02-13',
    '2024-02-14', '2024-02-15', '2024-02-16', '2024-02-17',  # 春节
    '2024-04-04', '2024-04-05', '2024-04-06',  # 清明
    '2024-05-01', '2024-05-02', '2024-05-03', '2024-05-04', '2024-05-05',  # 劳动
    '2024-06-08', '2024-06-09', '2024-06-10',  # 端午
    '2024-09-15', '2024-09-16', '2024-09-17',  # 中秋
    '2024-10-01', '2024-10-02', '2024-10-03', '2024-10-04', '2024-10-05',
    '2024-10-06', '2024-10-07',            # 国庆
    # 2025
    '2025-01-01',                         # 元旦
    '2025-01-28', '2025-01-29', '2025-01-30', '2025-01-31',
    '2025-02-01', '2025-02-02', '2025-02-03', '2025-02-04',  # 春节
    '2025-04-04', '2025-04-05', '2025-04-06',  # 清明
    '2025-05-01', '2025-05-02', '2025-05-03', '2025-05-04', '2025-05-05',  # 劳动
    '2025-05-31', '2025-06-01', '2025-06-02',  # 端午
    '2025-10-01', '2025-10-02', '2025-10-03', '2025-10-04', '2025-10-05',
    '2025-10-06', '2025-10-07', '2025-10-08',  # 中秋+国庆连休
    # 2026
    '2026-01-01', '2026-01-02', '2026-01-03',  # 元旦
    '2026-02-15', '2026-02-16', '2026-02-17', '2026-02-18', '2026-02-19',
    '2026-02-20', '2026-02-21', '2026-02-22',  # 春节
    '2026-04-04', '2026-04-05', '2026-04-06',  # 清明
    '2026-05-01', '2026-05-02', '2026-05-03', '2026-05-04', '2026-05-05',  # 劳动
    '2026-06-19', '2026-06-20', '2026-06-21',  # 端午
    '2026-09-25', '2026-09-26', '2026-09-27',  # 中秋
    '2026-10-01', '2026-10-02', '2026-10-03', '2026-10-04', '2026-10-05',
    '2026-10-06', '2026-10-07',            # 国庆
}


def load_trading_calendar(calendar_file=None):
    """加载交易日历文件（每行一个 YYYY-MM-DD 日期）。

    若调用，则该日历优先级高于内置节假日判断（用于接入权威交易日历）。
    """
    if calendar_file:
        with open(calendar_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    TRADING_CALENDAR.add(line)


def is_trading_day(d):
    """判断是否为 A 股交易日。

    优先级：
    1. 若已通过 load_trading_calendar 加载日历文件，则仅按该日历判断
    2. 否则按 内置节假日 + 周末 判断
    """
    if isinstance(d, date):
        d = d.strftime('%Y-%m-%d')
    if TRADING_CALENDAR:
        return d in TRADING_CALENDAR
    # 无外部日历文件时，使用内置节假日 + 周末判断
    try:
        d_obj = date.fromisoformat(d)
    except (ValueError, TypeError):
        return False
    if d_obj.weekday() >= 5:  # 周六、周日
        return False
    if d in _HOLIDAYS:
        return False
    return True


def get_trading_days(start_date, end_date):
    """返回 [start_date, end_date] 区间内的交易日列表（YYYY-MM-DD 字符串）。"""
    if isinstance(start_date, date):
        start_date = start_date.strftime('%Y-%m-%d')
    if isinstance(end_date, date):
        end_date = end_date.strftime('%Y-%m-%d')

    result = []
    current = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)

    while current <= end:
        if is_trading_day(current):
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