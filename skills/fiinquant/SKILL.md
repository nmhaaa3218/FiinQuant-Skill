# FiinQuantX Skill

Thư viện dữ liệu tài chính Python cho thị trường chứng khoán Việt Nam.

## Cài đặt tự động (Agent Self-Install)

Agent có thể tự cài đặt skill này bằng cách fetch installation script:

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/refs/heads/main/install_fiinquant.py | python3
```

Hoặc đọc và follow hướng dẫn:
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/refs/heads/main/FIRST_INSTALL.md
```

## Cài đặt thư viện (Manual)

```bash
pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx
```

**Lưu ý:** Kiểm tra signalrcore - nếu >= 1.0.0 thì gỡ và cài lại 0.9.x:
```bash
pip show signalrcore
pip uninstall signalrcore
pip install signalrcore==0.9.x
```

## Đăng nhập

```python
from FiinQuantX import FiinSession

client = FiinSession(
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD'
).login()
```

## Điểm nổi bật

- **Dữ liệu realtime** từ HOSE, HNX, UPCOM qua WebSocket
- **Dữ liệu lịch sử** đầy đủ timeframe 1m, 5m, 15m, 1h, 4h, 1D
- **Báo cáo tài chính** theo năm, quý, hợp nhất/riêng lẻ
- **Chỉ báo TA** tích hợp: MA, EMA, RSI, MACD, Bollinger Bands
- **Dòng tiền thông minh**: BU-SD, NĐTNN realtime

## Lỗi thường gặp

| Mã lỗi | Mô tả |
|--------|-------|
| 400 | Tài khoản không tồn tại hoặc mật khẩu không đúng |
| NameError | Chưa đăng nhập trước khi gọi dữ liệu |