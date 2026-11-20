# Nhiệm vụ: Tân Lê - Data Cleaning & Tiền xử lý (ĐÃ HOÀN THÀNH ✅)

## 👤 Thành viên: Tân Lê
- **Vai trò chính:** Data Cleaning & Tiền xử lý
- **Nhiệm vụ (KPI) lõi:** Làm sạch bộ dữ liệu 149,116 dòng, xử lý missing data, trích xuất đặc trưng thời gian & doanh thu.

## 📋 Checklist Hoàn Thành
- [x] **Bước 1:** Khảo sát dữ liệu thô `data/raw/coffee_shop_sales.csv` (149,116 dòng × 11 cột).
- [x] **Bước 2:** Kiểm định chất lượng: 0 missing values, 0 duplicates, 100% giá trị số lượng (1–8) và đơn giá ($0.80–$45.00) hợp lệ.
- [x] **Bước 3:** Hoàn thiện pipeline trong `data_cleaning.py` và trích xuất 9 cột đặc trưng mới (`revenue`, `hour`, `time_slot`, `month`, `month_label`, `day_of_week`, `day_name`, `day_name_vn`, `is_weekend`).
- [x] **Bước 4:** Xuất file sạch `data/clean/coffee_sales_cleaned.csv` cho Quốc Thái, Ngọc Phước và Tân Lưu.
