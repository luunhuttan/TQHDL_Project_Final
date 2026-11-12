# Nhiệm vụ: Tân Lưu (Leader) - Khung Web Dashboard Gentelella Admin

## 👤 Thành viên: Tân Lưu (Leader)
- **Vai trò chính:** Quản lý dự án, Dashboard & Report
- **Nhiệm vụ (KPI) lõi:** Lên khung Dashboard tổng, kết nối dữ liệu và biểu đồ, chuẩn bị Slide.
- **Công nghệ nền tảng:** **Python (Flask)** + **Gentelella Admin (Bootstrap/HTML5/CSS)** từ [ColorlibHQ/gentelella](https://github.com/ColorlibHQ/gentelella).

---

## 🎯 Mục tiêu chi tiết
1. **Khung giao diện Gentelella Admin (`app.py` & `templates/index.html`):**
   - Chạy nền tảng web bằng **Flask**, mang lại giao diện Bootstrap chuẩn 100% của Gentelella.
   - Sidebar cố định tone xanh than `#2A3F54` chứa thương hiệu, thông tin user và bộ lọc điều hành.
   - Hàng Top Stat Tiles (`tile_count`) kinh điển chia 5 chỉ số KPI ngang hàng.
   - Hệ thống Panel chuẩn (`x_panel`) với thanh `x_title`, nút toolbar và vùng nhúng biểu đồ `x_content`.
2. **Kết nối & Tích hợp:**
   - Tab 1: Nhúng biểu đồ chuỗi thời gian của **Quốc Thái**.
   - Tab 2: Nhúng biểu đồ sản phẩm và danh mục của **Ngọc Phước**.
   - Tab 3: Kết nối bảng dữ liệu sạch do **Tân Lê** xuất ra từ `data/clean/`.
3. **Báo cáo & Bàn giao:**
   - Cùng Quốc Thái viết báo cáo tổng kết phân tích (Report).
   - Chuẩn bị Slide thuyết trình.

---

## 🚀 Lệnh Khởi Chạy Dashboard

```bash
# Kích hoạt môi trường ảo
source .venv/bin/activate

# Khởi chạy ứng dụng Web Dashboard
python src/tan_luu_dashboard/app.py
```
> Mở trình duyệt truy cập: **`http://127.0.0.1:5000`**
