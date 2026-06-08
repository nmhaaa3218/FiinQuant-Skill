---
name: fiinquant
description: Python financial data library for Vietnamese stock market — realtime WebSocket, historical data, financial reports, and technical analysis indicators.
---

# FiinQuantX Skill

## Agent Self-Install

```bash
curl -fsSL https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/install_fiinquant.py | python3
```

Or read the guide manually:
```bash
curl -fsSL https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/skills/fiinquant/FIRST_INSTALL.md
```

## Install Library (Manual)

```bash
pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx
```

**Note:** Check signalrcore - if >= 1.0.0, uninstall and reinstall 0.9.x:
```bash
pip show signalrcore
pip uninstall signalrcore
pip install signalrcore==0.9.x
```

## Login

```python
from FiinQuantX import FiinSession

client = FiinSession(
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD'
).login()
```

## Features

- **Realtime data** from HOSE, HNX, UPCOM via WebSocket
- **Historical data** full timeframe 1m, 5m, 15m, 1h, 4h, 1D
- **Financial reports** by year, quarter, consolidated/separate
- **Technical indicators**: MA, EMA, RSI, MACD, Bollinger Bands
- **Smart money flow**: BU-SD, Foreign investor (NĐTNN) realtime

## Common Errors

| Error Code | Description |
|------------|-------------|
| 400 | Account does not exist or incorrect password |
| NameError | Not logged in before calling data |