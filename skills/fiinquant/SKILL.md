---
name: fiinquant
description: >
  Skill điều phối trung tâm — hướng dẫn agent xác định đúng skill cần trigger 
  dựa trên ý định (intent) của người dùng và tra cứu cú pháp từ tài liệu trực tiếp.
---

# 🧭 FiinQuant Skill Steering & Dispatcher Guide

> **MỤC ĐÍCH**: Đây là tài liệu điều phối hành vi cho AI Agent. Khi người dùng hỏi bất kỳ câu hỏi nào liên quan đến FiinQuant, agent PHẢI tuân thủ các quy tắc định tuyến, làm sạch tham số và chạy script tra cứu tài liệu động từ command line để lấy cú pháp hàm chính xác trước khi phản hồi hoặc viết code.

---

## 🔍 Hướng dẫn Tra cứu Tài liệu Động

Không được tự đoán hoặc bịa cú pháp các hàm của thư viện `FiinQuantX`. Bạn phải chạy trực tiếp script tìm kiếm qua Terminal để tra cứu tài liệu:

```bash
# Tìm kiếm các trang tài liệu liên quan đến từ khóa
python3 scripts/fiinquant_search.py "từ khóa tìm kiếm"

# Đọc chi tiết nội dung một trang tài liệu cụ thể
python3 scripts/fiinquant_search.py --read "/ham-va-cong-thuc/2.-du-lieu-giao-dich/2.1.-ham-du-lieu-realtime.md"

# Xem sơ đồ thư mục toàn bộ tài liệu
python3 scripts/fiinquant_search.py --outline

# Xem toàn bộ tài liệu dạng một file phẳng (offline reasoning)
python3 scripts/fiinquant_search.py --corpus
```

---

## 🗺️ Bản đồ điều phối Intent (Routing Map)

Dựa trên câu hỏi của người dùng, hãy xác định **Nhóm Intent** tương ứng để tra cứu đúng tài liệu:

### Nhóm 0 — Cài đặt & Giới thiệu
* **Ý định (Intent):** Hỏi về cài đặt, import, login, lỗi cài đặt, giới thiệu tổng quan.
* **Từ khóa chính:** `cài đặt`, `install`, `pip`, `setup`, `import`, `đăng nhập`, `login`, `lỗi import`, `NameError`.
* **Tra cứu tài liệu:** Chạy CLI search script hoặc xem hướng dẫn trực tuyến tại [GitHub README](https://github.com/nmhaaa3218/FiinQuant-Skill/blob/main/README.md) và [FIRST_INSTALL Guide](https://github.com/nmhaaa3218/FiinQuant-Skill/blob/main/FIRST_INSTALL.md).

### Nhóm 1 — Danh mục & Thông tin cơ bản
* **Ý định (Intent):** Tra cứu danh sách mã, thông tin doanh nghiệp, vốn hóa, room ngoại, freefloat, giá trần/sàn.
* **Từ khóa chính:** `danh sách mã`, `VN30`, `HNX30`, `rổ chỉ số`, `VNINDEX`, `ngành ICB`, `vốn hóa`, `room ngoại`, `NĐTNN`, `freefloat`, `giá trần sàn`, `tên công ty`, `hồ sơ công ty`.
* **Tra cứu từ khóa:** `Danh mục & Thông tin cơ bản` hoặc `danh sach ma`.

### Nhóm 2 — Dữ liệu giao dịch
* **Ý định (Intent):** Lấy giá realtime, giá lịch sử (OHLCV), sổ lệnh bid/ask, dữ liệu tick-by-tick.
* **Từ khóa chính:** `giá hiện tại`, `giá realtime`, `giá lịch sử`, `quá khứ`, `OHLCV`, `nến`, `timeframe`, `sổ lệnh`, `orderbook`, `bước giá`, `hủy lệnh`, `tick data`.
* **Tra cứu từ khóa:** `Dữ liệu giao dịch` hoặc `du lieu lich su`.

### Nhóm 3 — Phân tích cơ bản & Định giá (FA)
* **Ý định (Intent):** Lọc/đọc Báo cáo tài chính (BCTC), chỉ số tài chính (ROE, ROA, EPS...), định giá P/E, P/B, EV/EBITDA.
* **Từ khóa chính:** `báo cáo tài chính`, `BCTC`, `cân đối kế toán`, `kết quả kinh doanh`, `lưu chuyển tiền tệ`, `ROE`, `ROA`, `EPS`, `P/E`, `P/B`, `định giá`.
* **Tra cứu từ khóa:** `Phân tích cơ bản & Định giá` hoặc `bao cao tai chinh`.

### Nhóm 4 — Thống kê thị trường
* **Ý định (Intent):** Độ rộng thị trường (mã tăng/giảm), seasonality (mùa vụ giá).
* **Từ khóa chính:** `độ rộng thị trường`, `số mã tăng giảm`, `advance decline`, `seasonality`, `biến động theo tháng/quý`.
* **Tra cứu từ khóa:** `Thống kê thị trường`.

### Nhóm 5 — Chiến lược & Công cụ
* **Ý định (Intent):** Rebalance danh mục, tối ưu hóa danh mục (Markowitz), biểu đồ sức mạnh giá RRG.
* **Từ khóa chính:** `rebalance`, `tái cơ cấu`, `phân bổ lại`, `tối ưu danh mục`, `RRG`, `sức mạnh giá`.
* **Tra cứu từ khóa:** `Chiến lược & công cụ`.

### Nhóm 6 — Đặt lệnh giao dịch
* **Ý định (Intent):** Đăng nhập công ty chứng khoán, kiểm tra số dư tài khoản, sức mua, đặt/sửa/hủy lệnh mua/bán, xem vị thế đang giữ.
* **Từ khóa chính:** `kết nối DNSE`, `số dư tài khoản`, `margin`, `sức mua`, `đặt lệnh mua`, `đặt lệnh bán`, `sửa lệnh`, `hủy lệnh`, `vị thế`, `đóng deal`.
* **Tra cứu từ khóa:** `Hàm Đặt Lệnh` hoặc `dat lenh`.

### Nhóm 7 — Chỉ báo kỹ thuật (TA)
* **Ý định (Intent):** Chỉ báo xu hướng (MA, EMA...), động lượng (RSI, MACD...), biến động (Bollinger Bands, ATR...), khối lượng (OBV, VWAP...), hỗ trợ/kháng cự, Fibonacci, Smart Money Concepts (SMC, FVG, BOS, CHoCH).
* **Từ khóa chính:** `MA`, `EMA`, `RSI`, `MACD`, `Bollinger Bands`, `OBV`, `chỉ báo dòng tiền`, `hỗ trợ kháng cự`, `fibonacci`, `fibo`, `SMC`, `order block`, `FVG`.
* **Tra cứu từ khóa:** `Danh sách chỉ số TA`.

### Nhóm 8 — Mô hình biểu đồ (Chart Patterns)
* **Ý định (Intent):** Nhận dạng mô hình nến đảo chiều/tiếp diễn, cốc tay cầm, vai đầu vai...
* **Từ khóa chính:** `mô hình nến`, `candlestick`, `vai đầu vai`, `cốc tay cầm`, `hai đỉnh`, `hai đáy`, `engulfing`.
* **Tra cứu từ khóa:** `Danh sách mô hình Pattern`.

### Nhóm 9 — Bộ lọc cổ phiếu (Stock Screening)
* **Ý định (Intent):** Tìm các cổ phiếu thỏa mãn tiêu chí tài chính/kỹ thuật.
* **Từ khóa chính:** `lọc cổ phiếu`, `tìm cổ phiếu`, `screen`, `screener`, `CP có PE <`.
* **Tra cứu từ khóa:** `Bộ lọc cổ phiếu`.

---

## 🛠️ Quy tắc xử lý đa kỹ năng (Cross-Skill Orchestration)

Khi câu hỏi của người dùng yêu cầu nhiều bước phức tạp:
1. **Phân tách yêu cầu:** Tách câu hỏi thành các bước tuần tự (ví dụ: Lấy dữ liệu trước -> Tính toán chỉ báo sau -> Đưa ra khuyến nghị cuối cùng).
2. **Thứ tự ưu tiên:** 
   - *Dữ liệu trước, phân tích sau:* Luôn lấy giá lịch sử trước khi gọi hàm tính chỉ báo kỹ thuật.
   - *Đăng nhập trước, thao tác sau:* Để thực hiện lệnh (Nhóm 6), phải gọi hàm đăng nhập kết nối broker trước.
   - *Lọc trước, phân tích sau:* Lọc cổ phiếu từ bộ lọc trước rồi mới chạy phân tích chi tiết.

---

## ⚠️ Quy tắc xử lý Edge Cases & Bẫy nhập nhằng

### 1. Dữ liệu đầu vào mơ hồ (Thiếu thông tin)
Không được tự suy đoán tham số khi thiếu thông tin quan trọng. Hãy hỏi lại để làm rõ:
* *Thiếu mã cổ phiếu:* Hỏi "Bạn muốn xem mã cổ phiếu nào?"
* *Thiếu timeframe:* Hỏi rõ timeframe muốn lấy (1min, 5min, 15min, 1h, 4h, 1D).
* *Thiếu khoảng thời gian:* Hỏi rõ ngày bắt đầu và kết thúc.
* *Thiếu loại báo cáo tài chính:* Hỏi "Bạn muốn xem Cân đối kế toán, Kết quả kinh doanh, hay Lưu chuyển tiền tệ?"

### 2. Tự động sửa và Chuẩn hóa Format
* **Mã chứng khoán:** Tự động chuyển thành chữ hoa (ví dụ: `vnm` -> `VNM`). Sửa các định dạng sai (ví dụ: `VN-30` -> `VN30`).
* **Định dạng ngày:** Chuyển đổi mọi định dạng ngày của người dùng thành `YYYY-MM-DD` (ví dụ: `1-1-2024` -> `2024-01-01`).
* **Từ viết tắt tiếng Việt:** Tự động nhận diện các từ viết tắt tài chính phổ biến:
  - `CP` -> `cổ phiếu`
  - `BCTC` -> `báo cáo tài chính`
  - `KQKD` -> `kết quả kinh doanh`
  - `CĐKT` -> `bảng cân đối kế toán`
  - `LCTT` -> `lưu chuyển tiền tệ`
  - `NĐTNN` -> `nhà đầu tư nước ngoài`
  - `CTCK` -> `công ty chứng khoán`

### 3. ĐẶT LỆNH AN TOÀN (Bắt buộc Xác nhận Kép)
* Đối với mọi thao tác ở **Nhóm 6 (Đặt/Sửa/Hủy lệnh)**, Agent **PHẢI** yêu cầu xác nhận xác thực từ người dùng trước khi thực thi code.
* Hỏi lại đầy đủ các thông tin: Mã cổ phiếu, Số lượng, Giá, Loại lệnh (LO, MP...) nếu thiếu.
* Nếu số lượng giao dịch lớn bất thường (>100,000 cổ phiếu), hãy hiển thị cảnh báo rủi ro nổi bật và yêu cầu xác nhận lần thứ 2.
* Tuyệt đối không tự ý đặt lệnh ngầm.