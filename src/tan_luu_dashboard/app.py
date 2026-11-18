"""
Coffee Sales Executive Dashboard - Flask & Gentelella Admin Web App
====================================================================
File: src/tan_luu_dashboard/app.py
Nhiệm vụ: Tân Lưu (Leader) - Khung Web Dashboard chuẩn Gentelella (Bootstrap & HTML5)

Cách chạy:
    python src/tan_luu_dashboard/app.py
Truy cập trình duyệt:
    http://127.0.0.1:5000
"""

from pathlib import Path
import sys
from flask import Flask, render_template, jsonify, request, Response
import pandas as pd
import numpy as np

# Thiết lập đường dẫn thư mục gốc và các module thành viên
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
SRC_DIR = CURRENT_DIR.parent

sys.path.append(str(SRC_DIR / "quoc_thai_time_series"))
sys.path.append(str(SRC_DIR / "ngoc_phuoc_product_analysis"))
sys.path.append(str(SRC_DIR / "tan_le_data_cleaning"))

app = Flask(__name__, template_folder=str(CURRENT_DIR / "templates"))


# ==============================================================================
# 1. TRANG CHỦ DASHBOARD GENTELELLA & FAVICON
# ==============================================================================
@app.route("/")
def index():
    """Render giao diện khung sườn Dashboard theo chuẩn Gentelella Admin."""
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    """Trả về 204 No Content để tránh báo lỗi 404 favicon trên terminal."""
    return Response(status=204)


# ==============================================================================
# 2. CÁC API ENDPOINTS PHỤC VỤ DỮ LIỆU CHO CÁC THÀNH VIÊN
# ==============================================================================
@app.route("/api/summary", methods=["GET"])
def get_summary_kpi():
    """
    TODO [Tân Lưu]: Trả về các chỉ số KPI tổng hợp cho hàng Top Stat Tiles.
    Kết nối với dữ liệu sạch trong data/clean/ do Tân Lê cung cấp khi có dữ liệu thật.
    """
    summary = {
        "total_revenue": None,
        "total_volume": None,
        "total_transactions": None,
        "avg_order_value": None,
        "hero_product": None,
        "hero_product_share": None
    }
    return jsonify(summary)


@app.route("/api/time_series", methods=["GET"])
def get_time_series_data():
    """
    TODO [Tân Lưu & Quốc Thái]: API cung cấp dữ liệu chuỗi thời gian cho Tab 1.
    Trả về dữ liệu theo giờ, ngày trong tuần, heatmap và đường xu hướng.
    """
    return jsonify({"status": "pending_data", "assignee": "Quốc Thái", "module": "time_series_charts.py"})


@app.route("/api/products", methods=["GET"])
def get_product_data():
    """
    TODO [Tân Lưu & Ngọc Phước]: API cung cấp dữ liệu sản phẩm cho Tab 2.
    Trả về Top 10 sản phẩm, cơ cấu danh mục và phân tích giá.
    """
    return jsonify({"status": "pending_data", "assignee": "Ngọc Phước", "module": "product_charts.py"})


@app.route("/api/data", methods=["GET"])
def get_clean_data_table():
    """
    TODO [Tân Lưu & Tân Lê]: API trả về danh sách giao dịch sạch từ data/clean/ cho Tab 3.
    """
    return jsonify({"status": "pending_data", "assignee": "Tân Lê", "module": "data_cleaning.py"})


# ==============================================================================
# KHỞI CHẠY SERVER LOCAL
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print(" ☕ GENTELELLA COFFEE SALES EXECUTIVE DASHBOARD ĐANG CHẠY...")
    print(" 👉 Mở trình duyệt web truy cập: http://127.0.0.1:5000")
    print(" 💡 Nhấn Ctrl + C để dừng server.")
    print("=" * 70 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=True)
