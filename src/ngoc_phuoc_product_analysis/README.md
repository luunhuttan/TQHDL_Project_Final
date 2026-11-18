# Nhiệm vụ: Ngọc Phước - Phân tích Sản phẩm & Khách hàng

## 👤 Thành viên: Ngọc Phước
- **Vai trò chính:** Phân tích Sản phẩm & Khách hàng
- **Nhiệm vụ (KPI) lõi:** Trực quan mặt hàng bán chạy, danh mục.

---

## 🎯 Mục tiêu chi tiết (Tuần 1 - Tuần 2)
1. Sử dụng dữ liệu sạch từ thư mục chung `data/clean/` (do Tân Lê cung cấp).
2. Trực quan hóa và trả lời trọn vẹn câu hỏi lớn: **"Sản phẩm nào mang lại doanh thu cao?"**
   - Xây dựng bảng xếp hạng Top 10 sản phẩm đạt doanh số cao nhất (Cash cows).
   - Phân tích cơ cấu và tỷ trọng doanh thu theo từng Danh mục sản phẩm (Coffee, Tea, Bakery,...).
   - Phân tích tương quan giữa Đơn giá (Price) và Khối lượng bán (Volume/Quantity) để phân loại sản phẩm bán lẻ số lượng lớn vs sản phẩm cao cấp.
3. Đóng gói các hàm vẽ biểu đồ Plotly vào `product_charts.py` để Tân Lưu nhúng vào Tab 2 của Dashboard.

---

## 📋 Checklist công việc

- [ ] **Bước 1:** Khảo sát dữ liệu sản phẩm và danh mục trên notebook nháp `notebook/EDA_and_Testing.ipynb`.
- [ ] **Bước 2:** Hoàn thiện code các hàm trong `product_charts.py`:
  - `plot_top_products_by_revenue(df, top_n=10)`: Biểu đồ thanh ngang Top 10 sản phẩm doanh thu cao nhất.
  - `plot_revenue_by_category(df)`: Biểu đồ Donut/Pie phân tích tỷ trọng danh mục.
  - `plot_price_vs_volume(df)`: Biểu đồ phân tán (Scatter plot) giữa Đơn giá và Sản lượng bán.
- [ ] **Bước 3:** Bàn giao các hàm này cho Tân Lưu để tích hợp lên Dashboard Streamlit.
- [ ] **Bước 4:** Cung cấp thông tin insight về sản phẩm cho báo cáo chung.

