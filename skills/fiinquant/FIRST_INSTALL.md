# Hướng dẫn cài đặt FiinQuant Skill

## Agent Self-Install (Tự động)

Agent có thể tự cài đặt bằng cách chạy:

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/refs/heads/main/install_fiinquant.py | python3
```

## Cài đặt thủ công từng bước

### Bước 1: Cài đặt thư viện FiinQuantX

**Chọn nơi cài đặt:**

1. **Global (toàn hệ thống)** - Dùng chung cho mọi project
```bash
pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx
```

2. **Virtual Environment (.venv)** - Cài riêng trong thư mục `.venv`
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --extra-index-url https://fiinquant.github.io/fiinquantx/simple fiinquantx
```

**Kiểm tra signalrcore:**
```bash
pip show signalrcore
```
Nếu >= 1.0.0, gỡ và cài lại:
```bash
pip uninstall signalrcore
pip install signalrcore==0.9.x
```

---

### Bước 2: Cấu hình thông tin đăng nhập

**Bạn đã có tài khoản FiinQuant chưa?**

- **Có** → Có muốn lưu vào file `.env` không?
  ```env
  # Lưu tại ~/.config/opencode/skills/fiinquant/.env
  FIIN_USERNAME=your_username
  FIIN_PASSWORD=your_password
  ```

- **Chưa có** → Đăng ký tại [fiinquant.vn](https://fiinquant.vn)

---

### Bước 3: Cài đặt Skill cho Agent

Chọn cách đăng ký:

1. **Global Skill** - Agent dùng được ở mọi project
   - Thêm vào `~/.config/opencode/opencode.json`:
   ```json
   {
     "skills": [
       {
         "name": "fiinquant",
         "location": "~/.config/opencode/skills/fiinquant"
       }
     ]
   }
   ```

2. **Project-based** - Chỉ dùng trong project hiện tại
   - Thêm vào `.opencode/opencode.json` trong project

---

## Cấu trúc Skill

```
~/.config/opencode/skills/fiinquant/
├── SKILL.md              # Định nghĩa skill
├── FIRST_INSTALL.md      # Hướng dẫn cài đặt
├── install_fiinquant.py  # Script tự cài đặt
├── .env                  # Credentials (nếu lưu)
└── scripts/
    ├── fiinquant_search.py   # Công cụ tìm kiếm tài liệu
    └── first_install.py      # Script cài đặt interactive
```

---

## Kiểm tra cài đặt

```python
from FiinQuantX import FiinSession

client = FiinSession(
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD'
).login()

print("Đăng nhập thành công!")
```

---

## Sử dụng Công cụ tìm kiếm tài liệu

```bash
python scripts/fiinquant_search.py "WebSocket realtime"
```

```python
from scripts.fiinquant_search import search_documents, get_document_outline

results = search_documents("WebSocket realtime", limit=5)
outline = get_document_outline()
```