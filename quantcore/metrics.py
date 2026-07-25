import math


def total_return(equity_curve):
    if len(equity_curve) < 2:
        return 0.0
    return (equity_curve[-1] - equity_curve[0]) / equity_curve[0]


def annualized_return(equity_curve, trading_days=252):
    if len(equity_curve) < 2:
        return 0.0
    total_ret = total_return(equity_curve)
    days = len(equity_curve)
    if days <= 0:
        return 0.0
    return (1 + total_ret) ** (trading_days / days) - 1


def volatility(equity_curve):
    if len(equity_curve) < 2:
        return 0.0
    returns = [equity_curve[i] / equity_curve[i - 1] - 1 for i in range(1, len(equity_curve))]
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    std = math.sqrt(variance)
    return std * math.sqrt(252)


def downside_volatility(equity_curve):
    if len(equity_curve) < 2:
        return 0.0
    returns = [equity_curve[i] / equity_curve[i - 1] - 1 for i in range(1, len(equity_curve))]
    downside_returns = [r for r in returns if r < 0]
    if len(downside_returns) == 0:
        return 0.0
    mean = sum(downside_returns) / len(downside_returns)
    variance = sum((r - mean) ** 2 for r in downside_returns) / (len(downside_returns) - 1)
    std = math.sqrt(variance)
    return std * math.sqrt(252)


def sharpe_ratio(equity_curve, risk_free_rate=0.03):
    ann_return = annualized_return(equity_curve)
    vol = volatility(equity_curve)
    if vol == 0:
        return 0.0
    return (ann_return - risk_free_rate) / vol


def sortino_ratio(equity_curve, risk_free_rate=0.03):
    ann_return = annualized_return(equity_curve)
    downside_vol = downside_volatility(equity_curve)
    if downside_vol == 0:
        return 0.0
    return (ann_return - risk_free_rate) / downside_vol


def max_drawdown(equity_curve):
    if len(equity_curve) < 2:
        return 0.0
    max_equity = equity_curve[0]
    max_dd = 0.0
    for eq in equity_curve:
        if eq > max_equity:
            max_equity = eq
        dd = (max_equity - eq) / max_equity
        if dd > max_dd:
            max_dd = dd
    return max_dd


def calmar_ratio(equity_curve):
    ann_return = annualized_return(equity_curve)
    max_dd = max_drawdown(equity_curve)
    if max_dd == 0:
        return float('inf') if ann_return > 0 else 0.0
    return ann_return / max_dd


def win_rate(trades):
    if len(trades) == 0:
        return 0.0
    win_count = sum(1 for t in trades if t.get('profit', 0) > 0)
    return win_count / len(trades)


def profit_factor(trades):
    gross_profit = sum(t.get('profit', 0) for t in trades if t.get('profit', 0) > 0)
    gross_loss = abs(sum(t.get('profit', 0) for t in trades if t.get('profit', 0) < 0))
    if gross_loss == 0:
        return float('inf') if gross_profit > 0 else 0.0
    return gross_profit / gross_loss


def expected_return(trades):
    if len(trades) == 0:
        return 0.0
    total_profit = sum(t.get('profit', 0) for t in trades)
    return total_profit / len(trades)