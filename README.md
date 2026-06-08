# FiinQuant Skill for Agents

Thư viện dữ liệu tài chính Python cho thị trường chứng khoán Việt Nam.

## One-Line Agent Install

```bash
curl -fsSL https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/install_fiinquant.py | python3
```

Or read the guide and follow manually:

```bash
curl -fsSL https://raw.githubusercontent.com/nmhaaa3218/FiinQuant-Skill/refs/heads/main/skills/fiinquant/FIRST_INSTALL.md
```

## What is FiinQuantX?

- **Dữ liệu realtime** từ HOSE, HNX, UPCOM qua WebSocket
- **Dữ liệu lịch sử** đầy đủ timeframe 1m, 5m, 15m, 1h, 4h, 1D
- **Báo cáo tài chính** theo năm, quý, hợp nhất/riêng lẻ
- **Chỉ báo TA** tích hợp: MA, EMA, RSI, MACD, Bollinger Bands
- **Dòng tiền thông minh**: BU-SD, NĐTNN realtime

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
