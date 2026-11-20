"""
Tân Lê: Pipeline Làm sạch & Chuẩn hóa Dữ liệu (Data Cleaning & Feature Engineering)
===================================================================================
File: src/tan_le_data_cleaning/data_cleaning.py
Nhiệm vụ:
1. Đọc dữ liệu bán hàng gốc từ data/raw/coffee_shop_sales.csv (Read-only, 149,116 dòng).
2. Kiểm tra và xử lý missing values, dữ liệu trùng lặp và giá trị ngoại lai.
3. Chuẩn hóa kiểu dữ liệu (Datetime, Time, Numeric, Categorical).
4. Trích xuất các đặc trưng phục vụ phân tích (Feature Engineering):
   - revenue = transaction_qty * unit_price
   - hour (6 - 20), time_slot (Ca Sáng / Trưa-Chiều / Tối)
   - day_of_week, day_name, day_name_vn, is_weekend
   - month, month_name, month_year
5. Xuất dữ liệu sạch đạt chuẩn ra data/clean/coffee_sales_cleaned.csv.
"""

import logging
import sys
from pathlib import Path
import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Tân Lê - DataCleaning] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_RAW_PATH = PROJECT_ROOT / "data" / "raw" / "coffee_shop_sales.csv"
DEFAULT_CLEAN_PATH = PROJECT_ROOT / "data" / "clean" / "coffee_sales_cleaned.csv"

DAY_VN_MAP = {
    "Monday": "Thứ 2",
    "Tuesday": "Thứ 3",
    "Wednesday": "Thứ 4",
    "Thursday": "Thứ 5",
    "Friday": "Thứ 6",
    "Saturday": "Thứ 7",
    "Sunday": "Chủ Nhật"
}

MONTH_VN_MAP = {
    1: "Tháng 01/2023",
    2: "Tháng 02/2023",
    3: "Tháng 03/2023",
    4: "Tháng 04/2023",
    5: "Tháng 05/2023",
    6: "Tháng 06/2023"
}


def categorize_time_slot(hour: int) -> str:
    """Phân chia khung giờ hoạt động thành 4 ca kinh doanh thực tế."""
    if 6 <= hour <= 10:
        return "Ca Sáng Cao Điểm (06h-10h)"
    elif 11 <= hour <= 13:
        return "Ca Trưa (11h-13h)"
    elif 14 <= hour <= 17:
        return "Ca Chiều (14h-17h)"
    else:
        return "Ca Tối (18h-21h)"


def load_raw_data(file_path: str | Path = DEFAULT_RAW_PATH) -> pd.DataFrame:
    """Đọc dữ liệu bán hàng thô từ data/raw/ ở chế độ Read-only."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu gốc tại: {path}")

    logger.info(f"Đang tải dữ liệu gốc từ: {path}")
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path, encoding="utf-8")
    elif path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Định dạng file không hỗ trợ: {path.suffix}")

    logger.info(f"Đã tải thành công {len(df):,} dòng x {len(df.columns)} cột.")
    return df


def clean_coffee_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Thực hiện làm sạch tuyệt đối và tạo biến mới (Feature Engineering):
    1. Chuẩn hóa tên cột
    2. Kiểm tra & xử lý duplicates, missing values
    3. Ép kiểu ngày giờ & số thực
    4. Tạo các cột phục vụ phân tích của Quốc Thái và Ngọc Phước
    """
    df_clean = df.copy()
    initial_count = len(df_clean)

    # 1. Chuẩn hóa tên cột
    df_clean.columns = [col.strip().lower().replace(" ", "_") for col in df_clean.columns]

    # 2. Xóa các bản ghi trùng lặp (nếu có)
    dup_count = df_clean.duplicated().sum()
    if dup_count > 0:
        df_clean = df_clean.drop_duplicates()
        logger.info(f"Đã loại bỏ {dup_count:,} dòng trùng lặp.")
    else:
        logger.info("Kiểm tra trùng lặp: 0 dòng trùng lặp.")

    # 3. Kiểm tra và xử lý missing values
    null_counts = df_clean.isnull().sum()
    total_nulls = null_counts.sum()
    if total_nulls > 0:
        logger.warning(f"Phát hiện {total_nulls:,} giá trị thiếu. Đang xử lý...")
        # Bỏ dòng thiếu khóa chính hoặc ngày/giá/số lượng
        critical_cols = ["transaction_id", "transaction_date", "transaction_time", "transaction_qty", "unit_price"]
        df_clean = df_clean.dropna(subset=[c for c in critical_cols if c in df_clean.columns])
        # Điền 'Unknown' cho các cột phân loại còn lại
        for str_col in ["store_location", "product_category", "product_type", "product_detail"]:
            if str_col in df_clean.columns:
                df_clean[str_col] = df_clean[str_col].fillna("Unknown")
    else:
        logger.info("Kiểm tra Missing Values: 0 giá trị khuyết thiếu (Dữ liệu đầy đủ 100%).")

    # 4. Chuẩn hóa chuỗi văn bản
    for col in ["store_location", "product_category", "product_type", "product_detail"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()

    # 5. Chuẩn hóa kiểu số & lọc bỏ giá trị âm/bằng 0 bất hợp lệ
    df_clean["transaction_qty"] = pd.to_numeric(df_clean["transaction_qty"], errors="coerce").fillna(0).astype(int)
    df_clean["unit_price"] = pd.to_numeric(df_clean["unit_price"], errors="coerce").fillna(0.0).astype(float)
    df_clean = df_clean[(df_clean["transaction_qty"] > 0) & (df_clean["unit_price"] > 0)]

    # 6. Chuẩn hóa định dạng Ngày & Giờ
    df_clean["transaction_date"] = pd.to_datetime(
        df_clean["transaction_date"], format="%d-%m-%Y", errors="coerce"
    )
    df_clean = df_clean.dropna(subset=["transaction_date"])

    time_series = pd.to_datetime(df_clean["transaction_time"], format="%H:%M:%S", errors="coerce")
    df_clean["hour"] = time_series.dt.hour.astype(int)

    # 7. Feature Engineering
    df_clean["revenue"] = (df_clean["transaction_qty"] * df_clean["unit_price"]).round(2)
    df_clean["year"] = df_clean["transaction_date"].dt.year
    df_clean["month"] = df_clean["transaction_date"].dt.month
    df_clean["month_year"] = df_clean["transaction_date"].dt.strftime("%Y-%m")
    df_clean["month_label"] = df_clean["month"].map(MONTH_VN_MAP)
    df_clean["day_of_week"] = df_clean["transaction_date"].dt.day_of_week  # 0=Mon .. 6=Sun
    df_clean["day_name"] = df_clean["transaction_date"].dt.day_name()
    df_clean["day_name_vn"] = df_clean["day_name"].map(DAY_VN_MAP)
    df_clean["is_weekend"] = df_clean["day_of_week"].isin([5, 6])
    df_clean["time_slot"] = df_clean["hour"].apply(categorize_time_slot)
    df_clean["transaction_date"] = df_clean["transaction_date"].dt.strftime("%Y-%m-%d")

    logger.info(
        f"Hoàn tất làm sạch: Giữ lại {len(df_clean):,}/{initial_count:,} bản ghi hợp lệ. "
        f"Tổng doanh thu: ${df_clean['revenue'].sum():,.2f}"
    )
    return df_clean


def save_clean_data(df: pd.DataFrame, output_path: str | Path = DEFAULT_CLEAN_PATH) -> Path:
    """Lưu dữ liệu đã làm sạch vào thư mục data/clean/."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False, encoding="utf-8")
    logger.info(f"Đã xuất file dữ liệu sạch tại: {out} ({len(df):,} dòng)")
    return out


def get_cleaning_audit_report(df_clean: pd.DataFrame) -> dict:
    """Trả về báo cáo kiểm toán chất lượng dữ liệu sau khi làm sạch."""
    return {
        "total_rows": int(len(df_clean)),
        "total_columns": int(len(df_clean.columns)),
        "missing_values": int(df_clean.isnull().sum().sum()),
        "date_min": str(df_clean["transaction_date"].min()),
        "date_max": str(df_clean["transaction_date"].max()),
        "total_revenue": round(float(df_clean["revenue"].sum()), 2),
        "total_quantity": int(df_clean["transaction_qty"].sum()),
        "stores": sorted(df_clean["store_location"].unique().tolist()),
        "categories_count": int(df_clean["product_category"].nunique())
    }


def main():
    """Chạy toàn bộ pipeline làm sạch dữ liệu."""
    df_raw = load_raw_data(DEFAULT_RAW_PATH)
    df_clean = clean_coffee_data(df_raw)
    save_clean_data(df_clean, DEFAULT_CLEAN_PATH)
    report = get_cleaning_audit_report(df_clean)
    logger.info(f"Báo cáo kiểm định dữ liệu sạch: {report}")


if __name__ == "__main__":
    main()
