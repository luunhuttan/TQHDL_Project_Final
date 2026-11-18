"""
Ngọc Phước: Phân tích Sản phẩm & Khách hàng (Product Charts)
=============================================================
File: src/ngoc_phuoc_product_analysis/product_charts.py
Nhiệm vụ: Trả lời câu hỏi "Sản phẩm nào mang lại doanh thu cao?"
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_top_products_by_revenue(df: pd.DataFrame, top_n: int = 10):
    """
    TODO [Ngọc Phước]: Biểu đồ thanh ngang: Top N sản phẩm có tổng doanh thu cao nhất.
    - Đầu vào: DataFrame sạch có cột 'product_name' (hoặc 'product_detail') và 'revenue'.
    - Đầu ra: Figure Plotly (Horizontal Bar).
    - Thông điệp: Xác định các sản phẩm 'ngôi sao' đóng góp doanh thu nhiều nhất.
    """
    # TODO: Ngọc Phước viết code tại đây
    pass


def plot_revenue_by_category(df: pd.DataFrame):
    """
    TODO [Ngọc Phước]: Biểu đồ Donut / Pie: Tỷ trọng doanh thu theo từng Danh mục (Category).
    - Đầu vào: DataFrame sạch có cột 'product_category' và 'revenue'.
    - Đầu ra: Figure Plotly (Pie / Donut chart).
    - Thông điệp: Nhận diện cơ cấu doanh số đến từ nhóm đồ uống hay bánh ngọt/quà lưu niệm.
    """
    # TODO: Ngọc Phước viết code tại đây
    pass


def plot_price_vs_volume(df: pd.DataFrame):
    """
    TODO [Ngọc Phước]: Scatter plot: Mối tương quan giữa Đơn giá (Price) và Khối lượng bán (Quantity).
    - Đầu vào: DataFrame sạch.
    - Đầu ra: Figure Plotly (Scatter plot, kích thước điểm là doanh thu).
    - Thông điệp: Phân loại mặt hàng bán chạy số lượng lớn vs mặt hàng cao cấp giá trị lớn.
    """
    # TODO: Ngọc Phước viết code tại đây
    pass

