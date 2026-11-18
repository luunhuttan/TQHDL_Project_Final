# ☕ Trực Quan Hóa Dữ Liệu Bán Hàng Coffee Sales (Executive Dashboard)

> **Môn học:** Trực quan hóa dữ liệu (TQHDL)  
> **Kiến trúc:** Python (Flask Backend) + [Colorlib Gentelella v4 Dark Mode](https://preview.colorlib.com/theme/gentelella/production/index.html) (HTML5/Tailwind/Chart.js)  
> **Mục tiêu:** Trả lời 2 bài toán cốt lõi: *"Thời điểm nào bán chạy?"* & *"Sản phẩm nào mang lại doanh thu cao?"*

---

## 👥 Bảng Phân Công Nhiệm Vụ Thành Viên (Chính Thức)

| STT | Thành viên | Vai trò chính | Nhiệm vụ (KPI) lõi | Không gian làm việc phụ trách |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Tân Lưu (Leader)** | Quản lý dự án, Dashboard & Report | Lên khung Dashboard tổng (Gentelella v4), kết nối dữ liệu và biểu đồ của nhóm, chuẩn bị Slide thuyết trình. | [`src/tan_luu_dashboard/`](src/tan_luu_dashboard/) |
| 2 | **Tân Lê** | Data Cleaning & Tiền xử lý | Làm sạch bộ dữ liệu gốc, xử lý missing data, chuẩn hóa định dạng và xuất file sạch vào `data/clean/`. | [`src/tan_le_data_cleaning/`](src/tan_le_data_cleaning/) |
| 3 | **Quốc Thái** | Phân tích Doanh thu & Viết Báo cáo | Phân tích chuỗi thời gian (*"Thời điểm nào bán chạy?"*). Chịu trách nhiệm tổng hợp số liệu và viết báo cáo (Report). | [`src/quoc_thai_time_series/`](src/quoc_thai_time_series/) |
| 4 | **Ngọc Phước** | Phân tích Sản phẩm & Khách hàng | Trực quan hóa mặt hàng bán chạy, cơ cấu danh mục (*"Sản phẩm nào mang lại doanh thu cao?"*). | [`src/ngoc_phuoc_product_analysis/`](src/ngoc_phuoc_product_analysis/) |

---

## 📁 Cấu Trúc Thư Mục Dự Án Chuẩn (Project Tree)

```text
TQHDL_Project_Final/
├── .env                              # Biến môi trường hệ thống
├── .gitignore                        # Bộ lọc Git loại trừ cache, venv, file rác
├── data/
│   ├── raw/                          # Dữ liệu gốc bán hàng (READ-ONLY, tuyệt đối không chỉnh sửa)
│   └── clean/                        # Dữ liệu sạch do Tân Lê xuất ra cho cả nhóm dùng chung
├── docs/
│   ├── design_system.md              # Bảng màu HEX & thông số Gentelella v4 Dark Mode
│   └── project_notes.md              # Data Dictionary chuẩn & câu hỏi nghiệp vụ
├── notebook/
│   └── EDA_and_Testing.ipynb          # Notebook nháp khám phá dữ liệu (EDA) & test biểu đồ
├── src/                              # Toàn bộ mã nguồn chia theo 4 thành viên:
│   ├── __init__.py
│   ├── tan_le_data_cleaning/         # 👤 TÂN LÊ: DATA CLEANING & TIỀN XỬ LÝ
│   │   ├── README.md                 # Hướng dẫn chi tiết & checklist của Tân Lê
│   │   └── data_cleaning.py          # Script pipeline xử lý missing data & chuẩn hóa
│   ├── quoc_thai_time_series/        # 👤 QUỐC THÁI: PHÂN TÍCH DOANH THU & CHUỖI THỜI GIAN
│   │   ├── README.md                 # Hướng dẫn chi tiết & checklist của Quốc Thái
│   │   └── time_series_charts.py     # Thư viện hàm biểu đồ thời gian (Giờ, Ngày, Heatmap)
│   ├── ngoc_phuoc_product_analysis/  # 👤 NGỌC PHƯỚC: PHÂN TÍCH SẢN PHẨM & KHÁCH HÀNG
│   │   ├── README.md                 # Hướng dẫn chi tiết & checklist của Ngọc Phước
│   │   └── product_charts.py         # Thư viện hàm biểu đồ Top 10 sản phẩm, Donut danh mục
│   └── tan_luu_dashboard/            # 👤 TÂN LƯU (LEADER): DASHBOARD & BÁO CÁO
│       ├── templates/
│       │   └── index.html            # Giao diện Gentelella v4 Dark Mode (HTML5/Tailwind/Chart.js)
│       ├── README.md                 # Hướng dẫn chi tiết & checklist của Tân Lưu
│       └── app.py                    # Web Server Flask điều phối toàn hệ thống
├── Skill.md                          # Bộ tiêu chuẩn kỹ thuật & quy định vai trò Lead DA
├── requirements.txt                  # Danh mục thư viện Python bắt buộc
└── README.md                         # Tài liệu tổng quan & hướng dẫn toàn diện dự án
```

---

## 🚀 Hướng Dẫn Cài Đặt Môi Trường & Khởi Chạy

### 1. Kích hoạt Môi trường ảo Python
Mở Terminal tại thư mục gốc dự án và chạy:
```bash
# Trên macOS / Linux:
source .venv/bin/activate

# Trên Windows (Command Prompt / PowerShell):
# .venv\Scripts\activate
```

### 2. Cài đặt các thư viện cần thiết
Nếu mở dự án trên máy mới:
```bash
pip install -r requirements.txt
```

### 3. Khởi chạy Web Dashboard (Gentelella v4)
```bash
python src/tan_luu_dashboard/app.py
```
👉 Mở trình duyệt web truy cập địa chỉ: **`http://127.0.0.1:5000`**

---

## 📖 Hướng Dẫn Chi Tiết Cho Từng Thành Viên

### 👤 1. Hướng dẫn dành cho Tân Lê (Data Cleaning & Tiền xử lý)
- **Nhiệm vụ:**
  1. Tải file dữ liệu bán hàng gốc (dạng `.csv` hoặc `.xlsx`) và lưu vào thư mục [`data/raw/`](data/raw/).
  2. Tuyệt đối **không chỉnh sửa trực tiếp** vào file gốc.
  3. Mở file [`src/tan_le_data_cleaning/data_cleaning.py`](src/tan_le_data_cleaning/data_cleaning.py) để viết mã:
     - Đọc file thô từ `data/raw/`.
     - Lọc bỏ dòng trùng lặp, xử lý missing values.
     - Chuẩn hóa kiểu dữ liệu datetime, số lượng (`quantity`), đơn giá (`unit_price`).
     - Tạo thêm các cột đặc trưng: `hour` (giờ trong ngày 0-23h), `day_name` (thứ trong tuần), `revenue = quantity * unit_price`.
     - Xuất file kết quả sạch vào thư mục [`data/clean/`](data/clean/).
  4. Chạy script để tạo file sạch:
     ```bash
     python src/tan_le_data_cleaning/data_cleaning.py
     ```
  5. Bàn giao tên file dữ liệu sạch trong `data/clean/` cho Quốc Thái, Ngọc Phước và Tân Lưu.

---

### 👤 2. Hướng dẫn dành cho Quốc Thái (Phân tích Doanh thu & Chuỗi thời gian)
- **Câu hỏi phụ trách:** *"Thời điểm nào bán chạy?"*
- **Nhiệm vụ:**
  1. Đọc dữ liệu sạch từ [`data/clean/`](data/clean/) do Tân Lê cung cấp.
  2. Mở file [`src/quoc_thai_time_series/time_series_charts.py`](src/quoc_thai_time_series/time_series_charts.py) và hoàn thiện 4 hàm biểu đồ:
     - `plot_hourly_sales(df)`: Biểu đồ doanh thu/sản lượng theo khung giờ (0h - 23h), tìm giờ cao điểm.
     - `plot_sales_by_day_of_week(df)`: Biểu đồ doanh số các ngày trong tuần (T2 - CN), so sánh ngày thường vs cuối tuần.
     - `plot_sales_heatmap(df)`: Ma trận nhiệt 2 chiều Ngày trong tuần $\times$ Khung giờ.
     - `plot_trend_over_time(df)`: Biểu đồ đường xu hướng doanh thu theo ngày/tháng.
  3. Có thể dùng notebook [`notebook/EDA_and_Testing.ipynb`](notebook/EDA_and_Testing.ipynb) để nháp ý tưởng trước.
  4. Chịu trách nhiệm tổng hợp số liệu phân tích thời gian và cùng Tân Lưu viết Báo cáo (Report).

---

### 👤 3. Hướng dẫn dành cho Ngọc Phước (Phân tích Sản phẩm & Khách hàng)
- **Câu hỏi phụ trách:** *"Sản phẩm nào mang lại doanh thu cao?"*
- **Nhiệm vụ:**
  1. Đọc dữ liệu sạch từ [`data/clean/`](data/clean/) do Tân Lê cung cấp.
  2. Mở file [`src/ngoc_phuoc_product_analysis/product_charts.py`](src/ngoc_phuoc_product_analysis/product_charts.py) và hoàn thiện các hàm biểu đồ:
     - `plot_top_products_by_revenue(df, top_n=10)`: Biểu đồ thanh ngang xếp hạng Top sản phẩm đạt doanh số cao nhất (Cash cows).
     - `plot_revenue_by_category(df)`: Biểu đồ Donut thể hiện tỷ trọng doanh số giữa Cà phê, Trà, Bánh ngọt,...
     - `plot_price_vs_volume(df)`: Biểu đồ phân tán (Scatter) phân tích mối quan hệ giữa Đơn giá và Số lượng bán ra.
  3. Cung cấp các phát hiện (insights) về mặt hàng bán chạy cho báo cáo chung của nhóm.

---

### 👤 4. Hướng dẫn dành cho Tân Lưu (Leader - Quản lý, Dashboard & Report)
- **Nhiệm vụ:**
  1. Đôn đốc tiến độ của 3 thành viên theo kế hoạch 2 tuần.
  2. Quản lý Web Dashboard tại [`src/tan_luu_dashboard/`](src/tan_luu_dashboard/):
     - Giao diện được dựng bằng Flask và chuẩn Gentelella v4 Dark Mode.
     - Kết nối dữ liệu từ `data/clean/` lên bảng dữ liệu và 6 thẻ KPI tổng quan.
     - Kết nối dữ liệu các biểu đồ từ Quốc Thái và Ngọc Phước vào Dashboard.
  3. Chuẩn bị Slide thuyết trình bảo vệ dự án cuối kỳ.

---

## 🛠️ Xử Lý Lỗi Thường Gặp (Troubleshooting)

- **Lỗi cổng 5000 đã được sử dụng (Port 5000 in use):**
  Trên macOS Monterey/Ventura/Sonoma, cổng 5000 đôi khi bị dịch vụ AirPlay Receiver chiếm giữ.
  - *Cách 1:* Tắt AirPlay Receiver: Vào **System Settings > General > AirDrop & AirPlay > Tắt AirPlay Receiver**.
  - *Cách 2:* Đổi cổng trong `app.py`: sửa `app.run(host="127.0.0.1", port=5000)` thành `port=8080`.
- **Lỗi không tìm thấy module:**
  Đảm bảo đã kích hoạt môi trường ảo: `source .venv/bin/activate` trước khi chạy code.
