"""
Tân Lê: Pipeline Làm sạch & Chuẩn hóa Dữ liệu (Data Cleaning)
============================================================
File: src/tan_le_data_cleaning/data_cleaning.py
Nhiệm vụ: Làm sạch bộ dữ liệu, xử lý missing data.
"""

from pathlib import Path
import pandas as pd
import numpy as np


def load_raw_data(file_path: str | Path) -> pd.DataFrame:
    """
    TODO [Tân Lê]: Đọc dữ liệu bán hàng thô từ data/raw/ (Chế độ Read-only).
    - Hỗ trợ định dạng .csv hoặc .xlsx
    - Không chỉnh sửa file nguồn
    """
    # TODO: Tân Lê viết code tại đây
    pass


def clean_coffee_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO [Tân Lê]: Xử lý và làm sạch dữ liệu thô:
    1. Chuẩn hóa tên cột (lowercase, xóa khoảng trắng thừa).
    2. Loại bỏ bản ghi trùng lặp (duplicates).
    3. Xử lý missing values (xóa hoặc điền theo quy chuẩn trong docs/project_notes.md).
    4. Ép kiểu dữ liệu (Date, Time, Numeric).
    5. Feature engineering:
       - Tách giờ: 'hour'
       - Tách thứ trong tuần: 'day_name'
       - Tách tháng-năm: 'month_year'
       - Tính doanh thu: 'revenue' = quantity * unit_price
    """
    # TODO: Tân Lê viết code tại đây
    pass


def save_clean_data(df: pd.DataFrame, output_path: str | Path) -> None:
    """
    TODO [Tân Lê]: Lưu dữ liệu đã làm sạch vào thư mục data/clean/
    - Định dạng CSV chuẩn utf-8
    """
    # TODO: Tân Lê viết code tại đây
    pass


def main():
    """
    TODO [Tân Lê]: Luồng điều phối chính khi chạy script độc lập:
    python src/tan_le_data_cleaning/data_cleaning.py
    """
    # TODO: Tân Lê viết code kết nối load -> clean -> save tại đây
    pass


if __name__ == "__main__":
    main()

