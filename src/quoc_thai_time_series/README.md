# Nhiệm vụ: Quốc Thái - Phân tích Doanh thu & Chuỗi thời gian

## 👤 Thành viên: Quốc Thái
- **Vai trò chính:** Phân tích Doanh thu & Viết Báo cáo
- **Nhiệm vụ (KPI) lõi:** Phân tích chuỗi thời gian. Chịu trách nhiệm tổng hợp và viết báo cáo (Report).

---

## 🎯 Mục tiêu chi tiết (Tuần 1 - Tuần 2)
1. Sử dụng dữ liệu sạch từ thư mục chung `data/clean/` (do Tân Lê cung cấp).
2. Trực quan hóa và trả lời trọn vẹn câu hỏi lớn: **"Thời điểm nào bán chạy?"**
   - Phân tích theo khung giờ trong ngày (nhận diện khung giờ cao điểm).
   - Phân tích theo các ngày trong tuần (so sánh ngày thường vs cuối tuần).
   - Thiết lập bản đồ nhiệt (Heatmap) giao thoa Thứ $\times$ Giờ.
   - Phân tích xu hướng dài hạn theo ngày/tháng (trend, seasonality).
3. Đóng gói các hàm vẽ biểu đồ Plotly vào `time_series_charts.py` để Tân Lưu nhúng vào Tab 1 của Dashboard.
4. Tổng hợp số liệu và cùng Tân Lưu viết Báo cáo tổng kết (Report).

---

## 📋 Checklist công việc

- [ ] **Bước 1:** Khảo sát dữ liệu chuỗi thời gian trên notebook nháp `notebook/EDA_and_Testing.ipynb`.
- [ ] **Bước 2:** Hoàn thiện code các hàm trong `time_series_charts.py`:
  - `plot_hourly_sales(df)`: Biểu đồ doanh thu và lượng ly/đơn theo từng giờ (0h - 23h).
  - `plot_sales_by_day_of_week(df)`: Biểu đồ doanh thu thứ Hai đến Chủ Nhật.
  - `plot_sales_heatmap(df)`: Ma trận nhiệt Ngày trong tuần $\times$ Khung giờ.
  - `plot_trend_over_time(df)`: Biểu đồ diện tích/đường thể hiện xu hướng doanh thu qua thời gian.
- [ ] **Bước 3:** Bàn giao các hàm này cho Tân Lưu để tích hợp lên Dashboard Streamlit.
- [ ] **Bước 4:** Soạn thảo báo cáo kết quả phân tích chuỗi thời gian (Report).

