# Kế Hoạch & Định Hướng Dự Án: Trực Quan Hóa Dữ Liệu Bán Hàng Coffee Sales

> **Môn học:** Trực Quan Hóa Dữ Liệu (TQHDL)  
> **Dataset:** Maven Roasters Coffee Sales (Kaggle - 149,116 bản ghi)  
> **Ban dự án:** Tân Lưu (Leader) • Tân Lê • Quốc Thái • Ngọc Phước  
> **Tệp tin Word (.docx):** [`docs/Muc_Tieu_Va_Dinh_Huong_De_Tai.docx`](Muc_Tieu_Va_Dinh_Huong_De_Tai.docx)

---

## 1. Mục tiêu của dự án này là gì?

Mục tiêu cốt lõi của dự án không chỉ là vẽ biểu đồ, mà là **chuyển đổi dữ liệu thô thành thông tin có giá trị kinh doanh**. Cụ thể:

- **Xây dựng một hệ thống theo dõi (Dashboard) toàn diện:** Tích hợp các chỉ số quan trọng về doanh thu, sản phẩm và khách hàng vào một Dashboard duy nhất để người quản lý dễ dàng theo dõi.
- **Phân tích và trả lời các câu hỏi kinh doanh trọng tâm:** Trả lời trực tiếp các câu hỏi như: *"Thời điểm nào bán chạy nhất?"*, *"Danh mục/Sản phẩm nào mang lại doanh thu cao nhất?"*.
- **Kể chuyện qua dữ liệu (Data Storytelling):** Đảm bảo nguyên tắc *"Mỗi biểu đồ kể một câu chuyện"*, giúp người xem hiểu ngay vấn đề mà không cần phải đọc các con số thô ráp.
- **Làm chủ quy trình phân tích dữ liệu:** Áp dụng trọn vẹn quy trình từ thu thập, làm sạch dữ liệu (Data Cleaning), phân tích khám phá (EDA) đến xây dựng Dashboard trực quan bằng các công cụ chuyên dụng (Python Flask / Bootstrap / Plotly / Chart.js).

---

## 2. Trực quan hóa để làm gì và giải quyết vấn đề gì?

Dự án giúp giải quyết các **"bài toán" thực tế của một cửa hàng kinh doanh cà phê**:

- **Giải quyết bài toán nhân sự và vận hành:** Thông qua Heatmap khung giờ/ngày đông khách, cửa hàng có thể biết chính xác thời điểm nào bị quá tải. Từ đó, người quản lý biết cách xếp ca trực cho nhân viên hợp lý, tránh lãng phí vào giờ vắng và thiếu hụt nhân sự vào giờ cao điểm.
- **Giải quyết bài toán chiến lược sản phẩm (Menu Optimization):** Bằng cách dùng biểu đồ Pareto hoặc Treemap, nhóm sẽ chỉ ra được đâu là "nhóm sản phẩm vàng" (thường chiếm 20% mặt hàng nhưng tạo ra 80% doanh thu). Cửa hàng sẽ biết nên tập trung quảng bá, đẩy mạnh nhập nguyên liệu cho món nào, và xem xét loại bỏ các món "ế".
- **Giải quyết bài toán theo dõi hiệu suất (Performance Tracking):** Các biểu đồ Line/Bar chart về xu hướng doanh thu giúp chủ quán nhận diện được sự tăng trưởng hay sụt giảm theo thời gian, từ đó kịp thời đưa ra các chương trình khuyến mãi nếu doanh thu đang đi xuống.
- **Giúp ra quyết định nhanh chóng (Data-driven decision making):** Thay vì đọc một bảng Excel (như file raw từ Kaggle) dài hàng ngàn dòng, người quản lý chỉ cần nhìn vào Dashboard là nắm bắt được sức khỏe của doanh nghiệp ngay lập tức.

---

## 3. Tại sao nhóm lại chọn đề tài này?

Đây là câu hỏi rất hay bị giảng viên hỏi để xem nhóm có hiểu ý nghĩa của data mình chọn hay không. Bạn có thể trả lời dựa trên các ý sau:

- **Đề tài gần gũi, mang tính ứng dụng thực tế cao:** F&B (ngành dịch vụ ăn uống nói chung và mô hình quán cà phê nói riêng) là một mô hình kinh doanh cực kỳ phổ biến. Mọi sinh viên đều có thể dễ dàng hiểu được ngữ cảnh dữ liệu, từ đó đưa ra các insight (góc nhìn) rất thực tế và hợp logic.
- **Bộ dữ liệu đáp ứng hoàn hảo yêu cầu của môn Trực quan hóa:** Dataset Coffee Sales từ Kaggle có cấu trúc rất đa dạng (có yếu tố chuỗi thời gian datetime, có dữ liệu danh mục - categorical, có dữ liệu định lượng số tiền/số lượng). Nhờ vậy, nhóm có đất diễn để sử dụng rất nhiều loại biểu đồ khác nhau (Line, Bar, Pie/Donut, Heatmap, Treemap).
- **Phù hợp với cơ cấu nhóm 4 người:** Đề tài này cho phép chia task rất rõ ràng và phát huy thế mạnh của từng thành viên. Chẳng hạn: Tân Lê lo phần tiền xử lý data thô; Quốc Thái tập trung vào xu hướng doanh thu và hành vi; Ngọc Phước chuyên sâu về mặt hàng/sản phẩm; và bạn (Tân Lưu - Leader) sẽ là người đứng ra tổng hợp thành một Dashboard thẩm mỹ và có tính kết nối cao.

