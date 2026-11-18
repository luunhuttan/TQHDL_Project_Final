# Skill: Project Architecture & Python Dashboard Collaboration

## Vai trò
**Lead Data Analyst & Quản lý quy chuẩn kỹ thuật** của dự án "Trực quan hóa dữ liệu bán hàng Coffee Sales".
Nhiệm vụ: Thiết lập cấu trúc thư mục, thiết kế luồng công việc (workflow) bằng Python để đảm bảo dữ liệu đầu vào luôn sạch, biểu đồ có thông điệp rõ ràng, và tích hợp mượt mà thành một Web Dashboard tương tác chuyên nghiệp theo chuẩn **Gentelella v4 Dark Mode (Python Flask + Bootstrap/Tailwind & HTML5)** trong thời hạn 2 tuần.

---

## Mục tiêu dự án (Project Aims)

1. **Làm sạch dữ liệu tuyệt đối (Nguyên tắc 1 - Tân Lê phụ trách):**
   - Xử lý triệt để missing values (khuyết thiếu) và outliers phi lý.
   - Chuẩn hóa định dạng dữ liệu (datetime, số thực, chuỗi phân loại) bằng Pandas ngay từ bước đầu.
2. **Trực quan hóa có thông điệp (Nguyên tắc 2):**
   - Mỗi biểu đồ vẽ bằng Python/Chart.js/Plotly phải kể một câu chuyện cụ thể.
   - Trả lời trực tiếp 2 câu hỏi nghiệp vụ cốt lõi:
     - *"Thời điểm nào bán chạy?"* (Quốc Thái phụ trách: Theo giờ, thứ trong tuần, heatmap, mùa vụ).
     - *"Sản phẩm nào mang lại doanh thu cao?"* (Ngọc Phước phụ trách: Top sản phẩm, cơ cấu danh mục, tương quan giá vs sản lượng).
3. **Phân tách không gian xử lý và Giao diện (Separation of Concerns):**
   - Dữ liệu thô (`data/raw/`): Read-only, bất khả xâm phạm.
   - Dữ liệu sạch (`data/clean/`): Nguồn cấp duy nhất cho Dashboard.
   - Logic xử lý dữ liệu (`src/tan_le_data_cleaning/`): Độc lập, chạy batch script tự động.
   - Logic biểu đồ thời gian (`src/quoc_thai_time_series/`): Đóng gói module hóa.
   - Logic biểu đồ sản phẩm (`src/ngoc_phuoc_product_analysis/`): Đóng gói module hóa.
   - Giao diện người dùng (`src/tan_luu_dashboard/`): Nền tảng web Flask + Gentelella v4 Dark Mode (Tân Lưu điều phối).
4. **Chuẩn hóa Báo cáo (Reporting Standard):**
   - Đóng gói ứng dụng web dashboard chạy local ổn định tại `http://127.0.0.1:5000`.
   - Cung cấp URL Dashboard trực quan, ổn định cho người dùng nội bộ và bảo vệ dự án.

---

## Kế hoạch hành động 2 tuần (2-Week Roadmap)

### Tuần 1: Khởi tạo & Làm sạch dữ liệu
- **Giai đoạn 1: Khởi tạo & Thống nhất luồng dữ liệu**
  - Kích hoạt môi trường ảo Python (`venv`), cài đặt thư viện từ `requirements.txt`.
  - Tân Lê tiếp nhận file dữ liệu gốc vào `data/raw/` (tuyệt đối không sửa file gốc).
- **Giai đoạn 2: Khám phá & Làm sạch dữ liệu**
  - Dùng Jupyter Notebook (`notebook/EDA_and_Testing.ipynb`) để EDA, khảo sát phân phối và test biểu đồ mẫu.
  - Tân Lê đóng gói logic làm sạch vào `src/tan_le_data_cleaning/data_cleaning.py`.
  - Xuất dữ liệu đạt chuẩn 100% vào `data/clean/`.

### Tuần 2: Xây dựng Dashboard & Bàn giao
- **Giai đoạn 3: Trực quan hóa & Kết nối Dashboard**
  - Quốc Thái hoàn thiện các hàm chuỗi thời gian tại `src/quoc_thai_time_series/time_series_charts.py`.
  - Ngọc Phước hoàn thiện các hàm phân tích sản phẩm tại `src/ngoc_phuoc_product_analysis/product_charts.py`.
  - Tân Lưu (Leader) kết nối dữ liệu từ `data/clean/` và các hàm biểu đồ lên giao diện Gentelella v4 (`app.py`).
- **Giai đoạn 4: Kiểm duyệt & Bàn giao**
  - Chạy thử Dashboard (`python src/tan_luu_dashboard/app.py`): kiểm tra độ trễ tương tác, tính đúng đắn của số liệu.
  - Bàn giao kèm tài liệu hướng dẫn và Slide thuyết trình.
