# QuantCore

<p align="center">
  <strong>共享算法层 · 技术指标 / 绩效指标 / 资金计算 纯函数库</strong><br/>
  Python ≥3.10 · 无外部依赖 · MIT License
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"/>
  <img src="https://img.shields.io/badge/Version-0.1.0-orange.svg" alt="Version"/>
</p>

---

## 项目定位

QuantCore 是量化交易系统的**共享算法层**，提供纯函数实现的技术指标、绩效指标和资金计算能力。
被 [QuantEngine](https://github.com/wolfjkd/quantengine) 和 [Trader Finance Hub](https://github.com/wolfjkd/trader-finance-hub) 复用，避免算法重复实现。

## 核心模块

| 模块 | 文件 | 功能 |
|------|------|------|
| **技术指标** | `quantcore/indicators.py` | MA/EMA/SMA/WMA/MACD/KDJ/RSI/BOLL/ATR/量比 |
| **绩效指标** | `quantcore/metrics.py` | 夏普/索提诺/卡尔玛/最大回撤/胜率/盈亏比 等 |
| **资金计算** | `quantcore/money.py` | A股交易费用计算（佣金/印花税/过户费/滑点） |
| **工具函数** | `quantcore/utils.py` | Z-Score/MinMax标准化/中位数/交易日历 |

## 安装

```bash
# 本地开发安装
pip install -e .

# 或直接添加到依赖
pip install quantcore>=0.1.0
```

## 快速使用

```python
from quantcore import macd, kdj, sharpe_ratio, max_drawdown, Money

# 1. 技术指标计算
closes = [10.0, 10.5, 11.0, 10.8, 11.2, ...]
result = macd(closes, fast_period=12, slow_period=26, signal_period=9)
print(result['dif'], result['dea'], result['bar'])

# 2. 绩效指标计算
equity_curve = [1000000, 1010000, 1050000, 1030000, 1080000]
sharpe = sharpe_ratio(equity_curve)
mdd = max_drawdown(equity_curve)
print(f'夏普比率: {sharpe:.4f}, 最大回撤: {mdd:.4f}')

# 3. 资金计算
money = Money()
cost = money.buy_cost(price=10.5, qty=1000)
print(f'买入1000股10.5元，总费用: {cost}')
```

## 设计原则

1. **纯函数**：输入参数 → 输出结果，无副作用，无状态
2. **无外部依赖**：仅依赖 Python 标准库（math），不依赖 numpy/pandas
3. **标准算法**：与 Excel/通达信/同花顺 计算结果一致
4. **A股适配**：资金计算含A股特色规则（万2.5佣金、千0.5印花税、最低5元）

## 项目结构

```
quantcore/
├── quantcore/
│   ├── __init__.py          # 包入口
│   ├── __version__.py       # 版本号硬编码
│   ├── indicators.py        # 技术指标（10+函数）
│   ├── metrics.py           # 绩效指标（12+函数）
│   ├── money.py             # 资金计算
│   └── utils.py             # 工具函数
├── tests/
│   ├── test_indicators.py
│   ├── test_metrics.py
│   ├── test_money.py
│   ├── test_performance.py  # 性能基准测试
│   └── test_utils.py
├── docs/
│   └── phase1-report.md     # 阶段1测试报告
├── pyproject.toml
├── requirements.txt
└── LICENSE
```

## 性能基准

| 指标 | 数据量 | 平均耗时 |
|------|--------|---------|
| MA计算 | 10000点 | < 5ms |
| MACD计算 | 10000点 | < 8ms |
| KDJ计算 | 10000点 | < 10ms |
| 夏普比率 | 10000点权益曲线 | < 3ms |

## 版本历史

详见 [CHANGELOG.md](CHANGELOG.md)

| 版本 | 发布日期 | 主要变更 |
|------|---------|---------|
| v0.1.0 | 2026-07-25 | 初始版本：技术指标 + 绩效指标 + 资金计算 |

## License

MIT License © 2026 [wolfjkd](https://github.com/wolfjkd)
