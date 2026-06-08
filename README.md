# FiinQuant Skill

Python financial data library for Vietnamese stock market.

## One-Line Agent Install

```bash
curl -fsSL https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/install_fiinquant.py | python3
```

Agent can also read the guide manually:

```bash
curl -fsSL https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/skills/fiinquant/FIRST_INSTALL.md
```

## What is FiinQuantX?

- **Realtime data** from HOSE, HNX, UPCOM via WebSocket
- **Historical data** full timeframe 1m, 5m, 15m, 1h, 4h, 1D
- **Financial reports** by year, quarter, consolidated/separate
- **Technical indicators**: MA, EMA, RSI, MACD, Bollinger Bands
- **Smart money flow**: BU-SD, Foreign investor (NĐTNN) realtime

## Quick Start

```python
from FiinQuantX import FiinSession

client = FiinSession(
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD'
).login()
```

## Documentation

See [skills/fiinquant/FIRST_INSTALL.md](./skills/fiinquant/FIRST_INSTALL.md) for detailed setup instructions.

## License

MIT