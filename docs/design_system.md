# ☕ Coffee Sales Dashboard - Gentelella v4 Dark Mode Design System
*Thiết kế dựa trên phiên bản mới nhất [Colorlib Gentelella v4 Dark Mode](https://preview.colorlib.com/theme/gentelella/production/index.html)*

---

## 🎨 1. Bảng Màu Chuẩn Gentelella v4 (Dark Obsidian & Neon Accents)

| Vai trò thiết kế | Tên mã màu | Mã HEX | Ứng dụng thực tế |
| :--- | :--- | :--- | :--- |
| **Dark Canvas** | Void Navy Black | `#0B0F19` | Nền canvas toàn bộ ứng dụng (chiều sâu cao, chuẩn Dark Theme). |
| **Dark Surface** | Deep Obsidian Slate | `#111827` | Nền Sidebar và Top Header Navigation. |
| **Dark Card** | Dark Navy Panel | `#151D2F` | Nền các thẻ KPI Scorecards và khung biểu đồ. |
| **Border / Divider** | Subtle Slate Border | `#1F293D` | Viền mảnh các thẻ và đường kẻ phân cách. |
| **Neon Green (Primary)** | Emerald Glow | `#10B981` | Điểm nhấn chính: Button "Xuất báo cáo", đường Area Chart, chỉ số doanh thu. |
| **Neon Cyan (Accent)** | Electric Cyan | `#06B6D4` | Biểu đồ cột sản lượng giờ, badge Quốc Thái. |
| **Neon Amber (Warning)** | Golden Crema | `#F59E0B` | Biểu đồ danh mục, badge Ngọc Phước. |
| **Neon Purple** | Royal Violet | `#8B5CF6` | Thẻ phân bổ tỷ trọng, badge Tân Lê. |
| **Text Primary** | Pure White | `#F8FAFC` | Tiêu đề chính, số liệu lớn. |
| **Text Secondary / Muted** | Slate Gray | `#64748B` | Tiêu đề phụ, nhãn trục tọa độ. |

---

## 📐 2. Bố Cục Gentelella v4 Đã Triển Khai Vào Dự Án

1. **Sidebar Trái (`#111827` - 256px cố định):**
   - Brand icon xanh ngọc với ly cà phê + `Gentelella v4`.
   - Danh mục điều hướng với hiệu ứng viền xanh ngọc gradient `sidebar-item-active`.
   - Bộ lọc điều hành tích hợp trực tiếp trong sidebar.
   - Bảng phân công 4 thành viên (Tân Lưu, Tân Lê, Quốc Thái, Ngọc Phước).
   - Thẻ hồ sơ Leader Tân Lưu ở chân Sidebar.
2. **Top Navigation Bar:**
   - Breadcrumb đường dẫn `Home / Dashboard`.
   - Thanh tìm kiếm thông minh `⌘K`.
   - Badge trạng thái trực tiếp `● Hệ Thống Đang Chờ Data`.
   - Notification bell và Avatar người dùng.
3. **Hàng 6 Thẻ KPI Đậm Chất Gentelella v4:**
   - Hàng trên: 3 Thẻ lớn (Tổng Doanh Thu, Tổng Sản Lượng, Tổng Đơn Hàng) với icon bo góc tròn và sparkline phát sáng.
   - Hàng dưới: 3 Thẻ phụ với thanh tiến độ (Progress Bars) màu Neon Green, Cyan và Purple.
4. **Khu Vực Phân Tích Lưới 70% : 30%:**
   - **Cột Trái (Phân hệ Quốc Thái):** Biểu đồ Spline Area Chart phát sáng gradient 2 màu, Biểu đồ cột giờ (0h-23h), Biểu đồ ngày trong tuần và khung Ma trận nhiệt Heatmap.
   - **Cột Phải (Phân hệ Ngọc Phước):** Donut Chart cơ cấu danh mục với tâm rỗng hiện đại, Bảng xếp hạng Top 5 món bán chạy nhất và khung phân tích giá.
5. **Khu Vực Dữ Liệu Sạch (Phân hệ Tân Lê):**
   - Bảng dữ liệu phong cách Dark Table cao cấp với ô tìm kiếm nhanh và nút tải CSV.
