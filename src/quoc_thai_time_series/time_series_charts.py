"""
Quốc Thái: Phân tích Doanh thu & Chuỗi thời gian (Time-Series Charts)
=====================================================================
File: src/quoc_thai_time_series/time_series_charts.py
Nhiệm vụ: Trả lời câu hỏi "Thời điểm nào bán chạy?"
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_hourly_sales(df: pd.DataFrame):
    """
    TODO [Quốc Thái]: Biểu đồ doanh thu / sản lượng bán theo khung giờ trong ngày (0h - 23h).
    - Đầu vào: DataFrame sạch từ data/clean/ có cột 'hour', 'revenue', 'quantity'.
    - Đầu ra: Figure Plotly (cột doanh thu, đường sản lượng).
    - Thông điệp: Xác định 'khung giờ vàng' để chuẩn bị nhân viên và pha chế.
    """
    # TODO: Quốc Thái viết code tại đây
    pass


def plot_sales_by_day_of_week(df: pd.DataFrame):
    """
    TODO [Quốc Thái]: Biểu đồ doanh thu theo các ngày trong tuần (Thứ Hai -> Chủ Nhật).
    - Đầu vào: DataFrame sạch có cột 'day_name', 'revenue'.
    - Đầu ra: Figure Plotly.
    - Thông điệp: So sánh sức mua ngày thường vs cuối tuần.
    """
    # TODO: Quốc Thái viết code tại đây
    pass


def plot_sales_heatmap(df: pd.DataFrame):
    """
    TODO [Quốc Thái]: Ma trận nhiệt (Heatmap) giao thoa Ngày trong tuần vs Khung giờ.
    - Đầu vào: DataFrame sạch.
    - Đầu ra: Figure Plotly (px.imshow).
    - Thông điệp: Định vị chính xác tọa độ thời gian cao điểm nhất trong tuần.
    """
    # TODO: Quốc Thái viết code tại đây
    pass


def plot_trend_over_time(df: pd.DataFrame):
    """
    TODO [Quốc Thái]: Biểu đồ xu hướng doanh thu theo dòng thời gian (theo Ngày hoặc Tháng).
    - Đầu vào: DataFrame sạch có 'transaction_date', 'revenue'.
    - Đầu ra: Figure Plotly (Line / Area chart).
    - Thông điệp: Theo dõi đà tăng trưởng và tính chu kỳ/mùa vụ.
    """
    # TODO: Quốc Thái viết code tại đây
    pass

