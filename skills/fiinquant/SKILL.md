---
name: fiinquant
description: Python financial data library for Vietnamese stock market — realtime WebSocket, historical data, financial reports, and technical analysis indicators.
---

# FiinQuantX Skill

Exposes the FiinQuant Vietnamese financial data library and documentation search as a native skill/toolset to AI agents.

## Installation & Setup

Please follow the step-by-step setup instructions in the root [README.md](../../README.md) to install dependencies, set up credentials, and configure the Model Context Protocol (MCP) server.

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