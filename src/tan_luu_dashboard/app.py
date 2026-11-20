"""
Tân Lưu (Leader): Hệ Thống Web Dashboard Điều Hành Coffee Sales (Flask + Gentelella v4)
=======================================================================================
File: src/tan_luu_dashboard/app.py
Nhiệm vụ:
1. Tải dữ liệu sạch từ data/clean/coffee_sales_cleaned.csv (hoặc tự động kích hoạt pipeline của Tân Lê nếu chưa có).
2. Tích hợp trực tiếp các hàm phân tích chuỗi thời gian của Quốc Thái (time_series_charts.py).
3. Tích hợp trực tiếp các hàm phân tích sản phẩm & danh mục của Ngọc Phước (product_charts.py).
4. Cung cấp REST API lọc đa chiều thời gian thực (Theo Tháng, Chi nhánh, Danh mục, Tìm kiếm từ khóa).
5. Cung cấp tính năng Xuất báo cáo CSV theo điều kiện lọc hiện tại.

Cách chạy:
    source .venv/bin/activate
    python src/tan_luu_dashboard/app.py
Truy cập:
    http://127.0.0.1:5000
"""

import io
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, request, Response
import pandas as pd

# Thiết lập đường dẫn hệ thống tới các module thành viên
CURRENT_DIR = Path(__file__).resolve().parent
SRC_DIR = CURRENT_DIR.parent
PROJECT_ROOT = SRC_DIR.parent

sys.path.insert(0, str(SRC_DIR / "tan_le_data_cleaning"))
sys.path.insert(0, str(SRC_DIR / "quoc_thai_time_series"))
sys.path.insert(0, str(SRC_DIR / "ngoc_phuoc_product_analysis"))

from data_cleaning import (
    DEFAULT_RAW_PATH,
    DEFAULT_CLEAN_PATH,
    load_raw_data,
    clean_coffee_data,
    save_clean_data
)
from time_series_charts import (
    get_monthly_trend_data,
    get_daily_trend_data,
    get_hourly_sales_data,
    get_weekly_sales_data,
    get_heatmap_data
)
from product_charts import (
    get_category_share_data,
    get_top_products_data,
    get_top_product_types_data,
    get_price_volume_data,
    get_store_performance_data
)

app = Flask(__name__, template_folder=str(CURRENT_DIR / "templates"))

# Bộ nhớ đệm DataFrame sạch để tăng tốc độ phản hồi API (< 50ms)
_DF_MASTER: pd.DataFrame | None = None


def get_master_dataframe() -> pd.DataFrame:
    """Đọc dữ liệu sạch từ data/clean/. Tự động chạy pipeline làm sạch của Tân Lê nếu chưa tồn tại."""
    global _DF_MASTER
    if _DF_MASTER is not None:
        return _DF_MASTER

    if DEFAULT_CLEAN_PATH.exists():
        df = pd.read_csv(DEFAULT_CLEAN_PATH)
    else:
        df_raw = load_raw_data(DEFAULT_RAW_PATH)
        df = clean_coffee_data(df_raw)
        save_clean_data(df, DEFAULT_CLEAN_PATH)

    _DF_MASTER = df
    return _DF_MASTER


def filter_dataframe(df: pd.DataFrame, month: str, store: str, category: str, search: str = "") -> pd.DataFrame:
    """Áp dụng bộ lọc đa chiều từ giao diện người dùng."""
    filtered = df

    if month and month != "all":
        try:
            m_int = int(month)
            filtered = filtered[filtered["month"] == m_int]
        except ValueError:
            pass

    if store and store != "all":
        filtered = filtered[filtered["store_location"] == store]

    if category and category != "all":
        filtered = filtered[filtered["product_category"] == category]

    if search and search.strip():
        q = search.strip().lower()
        mask = (
            filtered["transaction_id"].astype(str).str.lower().str.contains(q, na=False)
            | filtered["product_detail"].str.lower().str.contains(q, na=False)
            | filtered["product_type"].str.lower().str.contains(q, na=False)
            | filtered["product_category"].str.lower().str.contains(q, na=False)
            | filtered["store_location"].str.lower().str.contains(q, na=False)
        )
        filtered = filtered[mask]

    return filtered


# ==============================================================================
# 1. ROUTE GIAO DIỆN CHÍNH
# ==============================================================================
@app.route("/")
def index():
    """Render trang chủ Gentelella v4 Dark Mode."""
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return Response(status=204)


# ==============================================================================
# 2. API TỔNG HỢP TOÀN BỘ DASHBOARD (KPIs + QUỐC THÁI + NGỌC PHƯỚC + TÂN LÊ)
# ==============================================================================
@app.route("/api/dashboard", methods=["GET"])
def api_dashboard():
    """
    Endpoint chính trả về toàn bộ chỉ số KPIs, dữ liệu biểu đồ chuỗi thời gian,
    dữ liệu biểu đồ sản phẩm và bảng giao dịch theo bộ lọc hiện hành.
    """
    df_master = get_master_dataframe()
    month = request.args.get("month", "all")
    store = request.args.get("store", "all")
    category = request.args.get("category", "all")
    search = request.args.get("search", "")

    df = filter_dataframe(df_master, month, store, category, search)

    total_rev = float(df["revenue"].sum()) if not df.empty else 0.0
    total_qty = int(df["transaction_qty"].sum()) if not df.empty else 0
    total_tx = int(len(df))
    aov = round(total_rev / max(total_tx, 1), 2) if total_tx > 0 else 0.0
    unique_days = max(int(df["transaction_date"].nunique()), 1) if not df.empty else 1
    avg_daily_cups = int(round(total_qty / unique_days)) if not df.empty else 0

    # Mặt hàng chủ lực Top 1
    if not df.empty:
        prod_rev = df.groupby("product_detail")["revenue"].sum()
        hero_product = str(prod_rev.idxmax())
        hero_product_rev = float(prod_rev.max())
        hero_product_share = round(hero_product_rev / max(total_rev, 1.0) * 100, 2)

        store_rev = df.groupby("store_location")["revenue"].sum()
        top_store = str(store_rev.idxmax())
        top_store_rev = float(store_rev.max())
        top_store_share = round(top_store_rev / max(total_rev, 1.0) * 100, 2)
    else:
        hero_product, hero_product_rev, hero_product_share = "N/A", 0.0, 0.0
        top_store, top_store_rev, top_store_share = "N/A", 0.0, 0.0

    # Dữ liệu mẫu 50 dòng giao dịch hiển thị trên bảng
    sample_records = []
    if not df.empty:
        sample_df = df.head(50)
        for _, r in sample_df.iterrows():
            sample_records.append({
                "transaction_id": int(r["transaction_id"]),
                "transaction_date": str(r["transaction_date"]),
                "transaction_time": str(r["transaction_time"]),
                "store_location": str(r["store_location"]),
                "product_category": str(r["product_category"]),
                "product_type": str(r["product_type"]),
                "product_detail": str(r["product_detail"]),
                "unit_price": round(float(r["unit_price"]), 2),
                "transaction_qty": int(r["transaction_qty"]),
                "revenue": round(float(r["revenue"]), 2)
            })

    response_payload = {
        "kpis": {
            "total_revenue": round(total_rev, 2),
            "total_quantity": total_qty,
            "total_transactions": total_tx,
            "aov": aov,
            "avg_daily_cups": avg_daily_cups,
            "unique_days": unique_days,
            "hero_product": hero_product,
            "hero_product_revenue": round(hero_product_rev, 2),
            "hero_product_share": hero_product_share,
            "top_store": top_store,
            "top_store_revenue": round(top_store_rev, 2),
            "top_store_share": top_store_share
        },
        "time_series": {
            "monthly": get_monthly_trend_data(df),
            "daily": get_daily_trend_data(df),
            "hourly": get_hourly_sales_data(df),
            "weekly": get_weekly_sales_data(df),
            "heatmap": get_heatmap_data(df)
        },
        "products": {
            "categories": get_category_share_data(df),
            "top_products": get_top_products_data(df, top_n=10),
            "top_types": get_top_product_types_data(df, top_n=10),
            "price_volume": get_price_volume_data(df),
            "stores": get_store_performance_data(df)
        },
        "table": {
            "total_filtered": total_tx,
            "records": sample_records
        }
    }
    return jsonify(response_payload)


@app.route("/api/export_csv", methods=["GET"])
def api_export_csv():
    """Xuất file CSV theo đúng bộ lọc người dùng đang chọn."""
    df_master = get_master_dataframe()
    month = request.args.get("month", "all")
    store = request.args.get("store", "all")
    category = request.args.get("category", "all")
    search = request.args.get("search", "")

    df = filter_dataframe(df_master, month, store, category, search)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8")
    csv_bytes = csv_buffer.getvalue().encode("utf-8")

    return Response(
        csv_bytes,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=coffee_sales_filtered_report.csv"}
    )


if __name__ == "__main__":
    print("\n" + "=" * 72)
    print(" ☕ GENTELELLA V4 - COFFEE SALES EXECUTIVE DASHBOARD ĐANG CHẠY...")
    print(" 👉 Mở trình duyệt web truy cập: http://127.0.0.1:5000")
    print(" 💡 Nhấn Ctrl + C để dừng server.")
    print("=" * 72 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=True)
