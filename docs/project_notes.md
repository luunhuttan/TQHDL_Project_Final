# Coffee Sales Analysis - Project Notes & Data Dictionary
*Dựa trên tập dữ liệu thực tế: [Coffee Shop Sales - Maven Roasters (Kaggle)](https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales)*

---

## 1. Thông Tin Tổng Quan Bộ Dữ Liệu Gốc

- **Tên tập tin gốc:** `coffee_shop_sales.csv` (được lưu tại `data/raw/coffee_shop_sales.csv`).
- **Quy mô:** **149,116 bản ghi (dòng)** $\times$ **11 trường thông tin (cột)**.
- **Phạm vi thời gian:** Từ `01-01-2023` đến `30-06-2023` (6 tháng kinh doanh).
- **Khung giờ hoạt động:** Từ `06:00:00` đến `20:59:32` (cửa hàng mở cửa từ 6h sáng đến 21h tối).
- **Đơn giá:** Dao động từ `$0.80` đến `$45.00`.
- **Số lượng mua / đơn:** Dao động từ `1` đến `8` sản phẩm.
- **Chi nhánh (Store Locations - 3 điểm bán tại New York):**
  1. `Lower Manhattan`
  2. `Hell's Kitchen`
  3. `Astoria`

---

## 2. Danh Mục Sản Phẩm (9 Danh Mục Lớn)

1. **Coffee:** Các món cà phê pha máy & ủ lạnh (Espresso, Latte, Cappuccino, Americano, Drip Coffee...).
2. **Tea:** Trà thảo mộc, trà đen, trà xanh, trà Chai (Chai tea, Earl Grey, Matcha, Green tea...).
3. **Bakery:** Bánh ngọt, bánh nướng ăn kèm (Scone, Pastry, Croissant, Muffin, Biscotti...).
4. **Drinking Chocolate:** Sô-cô-la nóng & sô-cô-la đá (Hot Chocolate, Cocoa...).
5. **Flavours:** Siro thêm hương vị (Caramel syrup, Hazelnut, Vanilla, Sugar free...).
6. **Coffee beans:** Hạt cà phê rang đóng gói mang về (Organic, Decaf, Espresso roast...).
7. **Loose Tea:** Trà búp khô đóng túi mang về.
8. **Packaged Chocolate:** Hộp kẹo sô-cô-la đóng gói.
9. **Branded:** Đồ dùng thương hiệu lưu niệm (Áo thun, ly sứ, bình giữ nhiệt).

---

## 3. Data Dictionary Chi Tiết (11 Cột Gốc)

| STT | Tên cột gốc | Kiểu dữ liệu | Mô tả ý nghĩa | Giá trị mẫu / Định dạng | Hướng xử lý (Tân Lê) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `transaction_id` | Integer | Khóa chính, mã giao dịch duy nhất | `1, 2, 3, ...` | Kiểm tra tính duy nhất, không null |
| 2 | `transaction_date` | String / Date | Ngày thực hiện giao dịch | `01-01-2023` | Parse sang Datetime `YYYY-MM-DD` |
| 3 | `transaction_time` | String / Time | Giờ thực hiện giao dịch | `07:06:11` | Parse sang Time `HH:MM:SS`, trích xuất cột `hour` (6 - 20) |
| 4 | `transaction_qty` | Integer | Số lượng sản phẩm bán ra | `1, 2, 3, ...` | Kiểm tra `qty > 0`, chuẩn hóa thành `int` |
| 5 | `store_id` | Integer | ID định danh điểm bán | `3, 5, 8` | Ép kiểu `int` |
| 6 | `store_location` | String | Địa điểm chi nhánh | `Lower Manhattan`, `Hell's Kitchen`, `Astoria` | Trim khoảng trắng, chuẩn hóa chuỗi |
| 7 | `product_id` | Integer | ID định danh sản phẩm | `32, 57, ...` | Ép kiểu `int` |
| 8 | `unit_price` | Float | Đơn giá niêm yết của 1 đơn vị sản phẩm | `3.0, 3.1, 4.5, ...` | Kiểm tra `unit_price >= 0` |
| 9 | `product_category` | String | Danh mục lớn của sản phẩm | `Coffee`, `Tea`, `Bakery`... | Chuẩn hóa nhóm phân loại chính |
| 10 | `product_type` | String | Phân loại cụ thể của sản phẩm | `Gourmet brewed coffee`, `Brewed Chai tea`... | Phục vụ phân tích nhóm đồ uống |
| 11 | `product_detail` | String | Tên sản phẩm chi tiết | `Ethiopia Rg`, `Cappuccino`, `Scone`... | Dùng để xếp hạng Top 10 sản phẩm bán chạy |
| *(Tự sinh)* | `revenue` | Float | Doanh thu từng dòng | `= transaction_qty * unit_price` | Tính toán trong pipeline làm sạch |
| *(Tự sinh)* | `day_name` | String | Thứ trong tuần | `Monday`, `Tuesday`, ... | Trích xuất từ `transaction_date` |
| *(Tự sinh)* | `month` | Integer / Str | Tháng giao dịch | `1, 2, 3, 4, 5, 6` | Phục vụ phân tích xu hướng dài hạn |

---

## 4. Ánh Xạ Câu Hỏi Nghiệp Vụ Với Các Cột Dữ Liệu

### Câu hỏi 1: "Thời điểm nào bán chạy?" (Quốc Thái phụ trách)
- **Theo giờ trong ngày:** Nhóm dữ liệu theo cột `hour` trích xuất từ `transaction_time` (06:00 đến 20:59) $\rightarrow$ tìm đỉnh cao điểm (Peak hours).
- **Theo thứ trong tuần:** Nhóm dữ liệu theo cột `day_name` trích xuất từ `transaction_date` $\rightarrow$ so sánh sức mua thứ Hai đến Chủ Nhật.
- **Ma trận nhiệt (Heatmap):** Pivot table giữa `day_name` $\times$ `hour` với giá trị là `sum(revenue)`.
- **Theo chu kỳ tháng:** Nhóm dữ liệu theo `month` (tháng 1 đến tháng 6/2023) để thấy đà tăng trưởng.

### Câu hỏi 2: "Sản phẩm nào mang lại doanh thu cao?" (Ngọc Phước phụ trách)
- **Top 10 sản phẩm chủ lực:** Nhóm theo cột `product_detail` $\rightarrow$ tính `sum(revenue)` và lấy Top 10 lớn nhất.
- **Cơ cấu danh mục:** Nhóm theo cột `product_category` (9 nhóm) $\rightarrow$ tính tỷ trọng phần trăm doanh thu (Donut Chart).
- **Tương quan giá vs sản lượng:** Phân tích ma trận giữa `unit_price` và `sum(transaction_qty)` theo từng `product_type`.

---

## 5. Mục Tiêu, Ý Nghĩa Trực Quan Hóa & Lý Do Chọn Đề Tài

### 1. Mục tiêu của dự án này là gì?
Mục tiêu cốt lõi của dự án không chỉ là vẽ biểu đồ, mà là **chuyển đổi dữ liệu thô thành thông tin có giá trị kinh doanh**. Cụ thể:
- **Xây dựng một hệ thống theo dõi (Dashboard) toàn diện:** Tích hợp các chỉ số quan trọng về doanh thu, sản phẩm và khách hàng vào một Dashboard duy nhất để người quản lý dễ dàng theo dõi.
- **Phân tích và trả lời các câu hỏi kinh doanh trọng tâm:** Trả lời trực tiếp các câu hỏi như: *"Thời điểm nào bán chạy nhất?"*, *"Danh mục/Sản phẩm nào mang lại doanh thu cao nhất?"*.
- **Kể chuyện qua dữ liệu (Data Storytelling):** Đảm bảo nguyên tắc *"Mỗi biểu đồ kể một câu chuyện"*, giúp người xem hiểu ngay vấn đề mà không cần phải đọc các con số thô ráp.
- **Làm chủ quy trình phân tích dữ liệu:** Áp dụng trọn vẹn quy trình từ thu thập, làm sạch dữ liệu (Data Cleaning), phân tích khám phá (EDA) đến xây dựng Dashboard trực quan bằng các công cụ chuyên dụng (Python Flask / Bootstrap / Plotly / Chart.js).

### 2. Trực quan hóa để làm gì và giải quyết vấn đề gì?
Dự án giúp giải quyết các **"bài toán" thực tế của một cửa hàng kinh doanh cà phê**:
- **Giải quyết bài toán nhân sự và vận hành:** Thông qua Heatmap khung giờ/ngày đông khách, cửa hàng có thể biết chính xác thời điểm nào bị quá tải. Từ đó, người quản lý biết cách xếp ca trực cho nhân viên hợp lý, tránh lãng phí vào giờ vắng và thiếu hụt nhân sự vào giờ cao điểm.
- **Giải quyết bài toán chiến lược sản phẩm (Menu Optimization):** Bằng cách dùng biểu đồ Pareto hoặc Treemap, nhóm sẽ chỉ ra được đâu là "nhóm sản phẩm vàng" (thường chiếm 20% mặt hàng nhưng tạo ra 80% doanh thu). Cửa hàng sẽ biết nên tập trung quảng bá, đẩy mạnh nhập nguyên liệu cho món nào, và xem xét loại bỏ các món "ế".
- **Giải quyết bài toán theo dõi hiệu suất (Performance Tracking):** Các biểu đồ Line/Bar chart về xu hướng doanh thu giúp chủ quán nhận diện được sự tăng trưởng hay sụt giảm theo thời gian, từ đó kịp thời đưa ra các chương trình khuyến mãi nếu doanh thu đang đi xuống.
- **Giúp ra quyết định nhanh chóng (Data-driven decision making):** Thay vì đọc một bảng Excel (như file raw từ Kaggle) dài hàng ngàn dòng, người quản lý chỉ cần nhìn vào Dashboard là nắm bắt được sức khỏe của doanh nghiệp ngay lập tức.

### 3. Tại sao nhóm lại chọn đề tài này?
- **Đề tài gần gũi, mang tính ứng dụng thực tế cao:** F&B (ngành dịch vụ ăn uống nói chung và mô hình quán cà phê nói riêng) là một mô hình kinh doanh cực kỳ phổ biến. Mọi sinh viên đều có thể dễ dàng hiểu được ngữ cảnh dữ liệu, từ đó đưa ra các insight (góc nhìn) rất thực tế và hợp logic.
- **Bộ dữ liệu đáp ứng hoàn hảo yêu cầu của môn Trực quan hóa:** Dataset Coffee Sales từ Kaggle có cấu trúc rất đa dạng (có yếu tố chuỗi thời gian datetime, có dữ liệu danh mục - categorical, có dữ liệu định lượng số tiền/số lượng). Nhờ vậy, nhóm có đất diễn để sử dụng rất nhiều loại biểu đồ khác nhau (Line, Bar, Pie/Donut, Heatmap, Treemap).
- **Phù hợp với cơ cấu nhóm 4 người:** Đề tài này cho phép chia task rất rõ ràng và phát huy thế mạnh của từng thành viên. Chẳng hạn: Tân Lê lo phần tiền xử lý data thô; Quốc Thái tập trung vào xu hướng doanh thu và hành vi; Ngọc Phước chuyên sâu về mặt hàng/sản phẩm; và bạn (Tân Lưu - Leader) sẽ là người đứng ra tổng hợp thành một Dashboard thẩm mỹ và có tính kết nối cao.
