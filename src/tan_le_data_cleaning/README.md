# Nhiệm vụ: Tân Lê - Data Cleaning & Tiền xử lý

## 👤 Thành viên: Tân Lê
- **Vai trò chính:** Data Cleaning & Tiền xử lý
- **Nhiệm vụ (KPI) lõi:** Làm sạch bộ dữ liệu, xử lý missing data

---

## 🎯 Mục tiêu chi tiết (Tuần 1)
1. Tuyệt đối không chỉnh sửa file gốc trong `data/raw/` (Read-only).
2. Xử lý triệt để các bản ghi missing values, dữ liệu ngoại lai/âm vô lý.
3. Chuẩn hóa định dạng thời gian (`datetime`, trích xuất `hour`, `day_name`, `month_year`).
4. Chuẩn hóa số lượng (`quantity`), đơn giá (`unit_price`), và tạo cột doanh thu (`revenue = quantity * unit_price`).
5. Xuất tập dữ liệu sạch đạt chuẩn 100% vào thư mục chung `data/clean/` để các thành viên khác nạp vào phân tích và Dashboard.

---

## 📋 Checklist công việc

- [ ] **Bước 1:** Khảo sát dữ liệu thô trong `data/raw/` (dùng notebook `notebook/EDA_and_Testing.ipynb`).
- [ ] **Bước 2:** Đọc file Data Dictionary trong `docs/project_notes.md` để đảm bảo đặt tên cột chuẩn.
- [ ] **Bước 3:** Hoàn thiện code các hàm trong `data_cleaning.py`:
  - `load_raw_data(file_path)`: Đọc file thô từ `data/raw/`.
  - `clean_coffee_data(df)`: Toàn bộ pipeline làm sạch, xử lý null, ép kiểu và feature engineering.
  - `save_clean_data(df, output_path)`: Lưu dữ liệu sạch ra `data/clean/`.
- [ ] **Bước 4:** Chạy thử script:
  ```bash
  python src/tan_le_data_cleaning/data_cleaning.py
  ```
- [ ] **Bước 5:** Bàn giao file dữ liệu sạch trong `data/clean/` cho Quốc Thái, Ngọc Phước và Tân Lưu.

