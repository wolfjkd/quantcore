# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/),

## [0.1.0] - 2026-07-25

### Added - 初始版本
- **技术指标模块** (`quantcore/indicators.py`)
  - `ma` / `sma` / `ema` / `wma` - 移动平均线（4种）
  - `macd` - MACD 指标（DIF/DEA/BAR）
  - `kdj` - KDJ 随机指标（K/D/J）
  - `rsi` - RSI 相对强弱指数（Wilder 平滑法）
  - `boll` - 布林带（上/中/下轨）
  - `atr` - ATR 平均真实波幅
  - `vol_ma` - 量比移动平均

- **绩效指标模块** (`quantcore/metrics.py`)
  - `total_return` / `annualized_return` - 收益率
  - `volatility` / `downside_volatility` - 波动率
  - `max_drawdown` - 最大回撤
  - `sharpe_ratio` / `sortino_ratio` / `calmar_ratio` - 风险调整收益
  - `win_rate` / `profit_factor` / `expected_return` - 交易质量

- **资金计算模块** (`quantcore/money.py`)
  - `Money` 类：A股交易费用计算
  - 佣金（万2.5，最低5元）、印花税（千0.5，仅卖出）
  - 滑点模拟、过户费

- **工具函数模块** (`quantcore/utils.py`)
  - `zscore` / `normalize` / `median` - 数据标准化
  - `is_trading_day` / `get_trading_days` - 交易日历工具

### Tests
- 5个测试文件，覆盖所有模块
- 性能基准测试：10000点数据 < 10ms
- 阶段1测试报告：`docs/phase1-report.md`

### Infrastructure
- `pyproject.toml` 项目配置（setuptools 构建后端）
- `requirements.txt` 依赖清单（无外部依赖）
- MIT License
- `.gitignore` Python 标准模板
