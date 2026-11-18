"""
Tân Lê: Pipeline Làm sạch & Chuẩn hóa Dữ liệu (Data Cleaning)
============================================================
File: src/tan_le_data_cleaning/data_cleaning.py
Nhiệm vụ: Làm sạch bộ dữ liệu, xử lý missing data.
"""

from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = {
    "transaction_id",
    "transaction_date",
    "transaction_time",
    "transaction_qty",
    "store_id",
    "store_location",
    "product_id",
    "unit_price",
    "product_category",
    "product_type",
    "product_detail",
}


def _normalize_column_name(column: object) -> str:
    """Convert a source column name to the project's snake_case convention."""
    return "_".join(str(column).strip().lower().replace("-", " ").split())


def load_raw_data(file_path: str | Path) -> pd.DataFrame:
    """
    TODO [Tân Lê]: Đọc dữ liệu bán hàng thô từ data/raw/ (Chế độ Read-only).
    - Hỗ trợ định dạng .csv hoặc .xlsx
    - Không chỉnh sửa file nguồn
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError("Chỉ hỗ trợ file dữ liệu .csv, .xlsx hoặc .xls")


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
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df phải là một pandas DataFrame")

    cleaned = df.copy()
    cleaned.columns = [_normalize_column_name(column) for column in cleaned.columns]

    # Accept the common alternative name used by downstream chart modules.
    cleaned = cleaned.rename(columns={"quantity": "transaction_qty"})
    missing_columns = REQUIRED_COLUMNS - set(cleaned.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Thiếu các cột bắt buộc: {missing}")

    cleaned = cleaned.drop_duplicates()

    numeric_columns = [
        "transaction_id",
        "transaction_qty",
        "store_id",
        "product_id",
        "unit_price",
    ]
    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned["transaction_date"] = pd.to_datetime(
        cleaned["transaction_date"], errors="coerce", dayfirst=True
    )
    parsed_time = pd.to_datetime(
        cleaned["transaction_time"].astype("string"), errors="coerce", format="mixed"
    )

    text_columns = [
        "store_location",
        "product_category",
        "product_type",
        "product_detail",
    ]
    for column in text_columns:
        cleaned[column] = (
            cleaned[column]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

    valid_rows = (
        cleaned[list(REQUIRED_COLUMNS)].notna().all(axis=1)
        & parsed_time.notna()
        & (cleaned["transaction_qty"] > 0)
        & (cleaned["unit_price"] >= 0)
    )
    cleaned = cleaned.loc[valid_rows].copy()
    parsed_time = parsed_time.loc[valid_rows]

    cleaned = cleaned.drop_duplicates(subset="transaction_id", keep="first")
    cleaned["transaction_id"] = cleaned["transaction_id"].astype("int64")
    cleaned["transaction_qty"] = cleaned["transaction_qty"].astype("int64")
    cleaned["store_id"] = cleaned["store_id"].astype("int64")
    cleaned["product_id"] = cleaned["product_id"].astype("int64")
    cleaned["unit_price"] = cleaned["unit_price"].astype(float)
    cleaned["transaction_time"] = parsed_time.dt.strftime("%H:%M:%S")

    cleaned["quantity"] = cleaned["transaction_qty"]
    cleaned["hour"] = parsed_time.dt.hour.astype("int64")
    cleaned["day_name"] = cleaned["transaction_date"].dt.day_name()
    cleaned["month"] = cleaned["transaction_date"].dt.month.astype("int64")
    cleaned["month_year"] = cleaned["transaction_date"].dt.strftime("%Y-%m")
    cleaned["revenue"] = cleaned["quantity"] * cleaned["unit_price"]

    return cleaned.sort_values("transaction_id").reset_index(drop=True)


def save_clean_data(df: pd.DataFrame, output_path: str | Path) -> None:
    """
    TODO [Tân Lê]: Lưu dữ liệu đã làm sạch vào thư mục data/clean/
    - Định dạng CSV chuẩn utf-8
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df phải là một pandas DataFrame")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")


def main():
    """
    TODO [Tân Lê]: Luồng điều phối chính khi chạy script độc lập:
    python src/tan_le_data_cleaning/data_cleaning.py
    """
    project_root = Path(__file__).resolve().parents[2]
    raw_path = project_root / "data" / "raw" / "coffee_shop_sales.csv"
    clean_path = project_root / "data" / "clean" / "coffee_shop_sales_clean.csv"

    raw_data = load_raw_data(raw_path)
    clean_data = clean_coffee_data(raw_data)
    save_clean_data(clean_data, clean_path)
    print(f"Đã làm sạch {len(clean_data):,} dòng dữ liệu: {clean_path}")


if __name__ == "__main__":
    main()

