"""
Ngọc Phước: Phân tích Sản phẩm, Danh mục & Khách hàng (Product & Category Analysis)
===================================================================================
File: src/ngoc_phuoc_product_analysis/product_charts.py
Nhiệm vụ: Trả lời trọn vẹn câu hỏi nghiệp vụ 2: "Sản phẩm nào mang lại doanh thu cao?"
Bao gồm:
1. Cơ cấu doanh thu & tỷ trọng 9 danh mục lớn (product_category)
2. Top 10 sản phẩm chi tiết mang lại doanh thu cao nhất (product_detail) & Top dòng sản phẩm (product_type)
3. Phân tích tương quan Đơn giá (unit_price) vs Sản lượng bán (transaction_qty)
4. So sánh hiệu suất 3 chi nhánh (Hell's Kitchen, Astoria, Lower Manhattan)
Cung cấp cả hàm trả về dữ liệu JSON (cho Web Dashboard Gentelella v4) và đối tượng Plotly Figure (cho Notebook EDA).
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ==============================================================================
# 1. HÀM TỔNG HỢP DỮ LIỆU JSON PHỤC VỤ DASHBOARD GENTELELLA V4
# ==============================================================================

def get_category_share_data(df: pd.DataFrame) -> dict:
    """Tính doanh thu, sản lượng, số đơn và tỷ trọng % của 9 danh mục (product_category)."""
    if df.empty:
        return {"categories": [], "revenue": [], "quantity": [], "orders": [], "share_pct": []}

    total_rev = max(float(df["revenue"].sum()), 1.0)
    cat_df = (
        df.groupby("product_category")
        .agg(
            revenue=("revenue", "sum"),
            quantity=("transaction_qty", "sum"),
            orders=("transaction_id", "count")
        )
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    cat_df["revenue"] = cat_df["revenue"].round(2)
    cat_df["share_pct"] = (cat_df["revenue"] / total_rev * 100).round(2)
    cat_df["cumulative_pct"] = cat_df["share_pct"].cumsum().round(2)

    return {
        "categories": cat_df["product_category"].tolist(),
        "revenue": cat_df["revenue"].tolist(),
        "quantity": cat_df["quantity"].astype(int).tolist(),
        "orders": cat_df["orders"].astype(int).tolist(),
        "share_pct": cat_df["share_pct"].tolist(),
        "cumulative_pct": cat_df["cumulative_pct"].tolist()
    }


def get_top_products_data(df: pd.DataFrame, top_n: int = 10) -> dict:
    """Xếp hạng Top N món chi tiết (product_detail) có tổng doanh thu cao nhất."""
    if df.empty:
        return {"products": [], "categories": [], "revenue": [], "quantity": [], "unit_price": [], "share_pct": []}

    total_rev = max(float(df["revenue"].sum()), 1.0)
    top_df = (
        df.groupby(["product_detail", "product_category"])
        .agg(
            revenue=("revenue", "sum"),
            quantity=("transaction_qty", "sum"),
            unit_price=("unit_price", "mean"),
            orders=("transaction_id", "count")
        )
        .sort_values("revenue", ascending=False)
        .head(top_n)
        .reset_index()
    )
    top_df["revenue"] = top_df["revenue"].round(2)
    top_df["unit_price"] = top_df["unit_price"].round(2)
    top_df["share_pct"] = (top_df["revenue"] / total_rev * 100).round(2)

    return {
        "products": top_df["product_detail"].tolist(),
        "categories": top_df["product_category"].tolist(),
        "revenue": top_df["revenue"].tolist(),
        "quantity": top_df["quantity"].astype(int).tolist(),
        "unit_price": top_df["unit_price"].tolist(),
        "orders": top_df["orders"].astype(int).tolist(),
        "share_pct": top_df["share_pct"].tolist()
    }


def get_top_product_types_data(df: pd.DataFrame, top_n: int = 10) -> dict:
    """Xếp hạng Top N dòng sản phẩm (product_type) có doanh thu cao nhất."""
    if df.empty:
        return {"types": [], "categories": [], "revenue": [], "quantity": []}

    type_df = (
        df.groupby(["product_type", "product_category"])
        .agg(
            revenue=("revenue", "sum"),
            quantity=("transaction_qty", "sum"),
            avg_price=("unit_price", "mean")
        )
        .sort_values("revenue", ascending=False)
        .head(top_n)
        .reset_index()
    )
    return {
        "types": type_df["product_type"].tolist(),
        "categories": type_df["product_category"].tolist(),
        "revenue": type_df["revenue"].round(2).tolist(),
        "quantity": type_df["quantity"].astype(int).tolist(),
        "avg_price": type_df["avg_price"].round(2).tolist()
    }


def get_price_volume_data(df: pd.DataFrame) -> list[dict]:
    """
    Phân tích tương quan Đơn giá trung bình (unit_price) vs Tổng sản lượng bán (quantity)
    theo từng dòng sản phẩm (product_type) phục vụ biểu đồ Scatter Bubble.
    """
    if df.empty:
        return []

    pv_df = (
        df.groupby(["product_type", "product_category"])
        .agg(
            avg_price=("unit_price", "mean"),
            quantity=("transaction_qty", "sum"),
            revenue=("revenue", "sum"),
            orders=("transaction_id", "count")
        )
        .reset_index()
    )
    points = []
    for _, row in pv_df.iterrows():
        points.append({
            "product_type": str(row["product_type"]),
            "category": str(row["product_category"]),
            "x": int(row["quantity"]),
            "y": round(float(row["avg_price"]), 2),
            "revenue": round(float(row["revenue"]), 2),
            "orders": int(row["orders"]),
            "r": max(5, min(22, int(np.sqrt(row["revenue"]) / 14)))
        })
    return points


def get_store_performance_data(df: pd.DataFrame) -> list[dict]:
    """Tổng hợp doanh thu, sản lượng, số đơn và AOV theo 3 chi nhánh (store_location)."""
    if df.empty:
        return []

    total_rev = max(float(df["revenue"].sum()), 1.0)
    store_df = (
        df.groupby("store_location")
        .agg(
            revenue=("revenue", "sum"),
            quantity=("transaction_qty", "sum"),
            orders=("transaction_id", "count")
        )
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    results = []
    for _, row in store_df.iterrows():
        rev = float(row["revenue"])
        tx = int(row["orders"])
        results.append({
            "store_location": str(row["store_location"]),
            "revenue": round(rev, 2),
            "quantity": int(row["quantity"]),
            "orders": tx,
            "aov": round(rev / max(tx, 1), 2),
            "share_pct": round(rev / total_rev * 100, 2)
        })
    return results


# ==============================================================================
# 2. HÀM VẼ BIỂU ĐỒ PLOTLY (PHỤC VỤ NOTEBOOK EDA & BÁO CÁO)
# ==============================================================================

def plot_top_products_by_revenue(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Biểu đồ thanh ngang Top 10 sản phẩm có doanh thu cao nhất."""
    data = get_top_products_data(df, top_n=top_n)
    fig = go.Figure(go.Bar(
        x=data["revenue"][::-1],
        y=data["products"][::-1],
        orientation="h",
        marker_color="#10B981",
        text=[f"${v:,.0f}" for v in data["revenue"][::-1]],
        textposition="outside"
    ))
    fig.update_layout(
        title=f"<b>Top {top_n} Sản Phẩm Chi Tiết Mang Lại Doanh Thu Cao Nhất</b>",
        xaxis_title="Tổng doanh thu ($)",
        yaxis_title="Sản phẩm (product_detail)",
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827"
    )
    return fig


def plot_revenue_by_category(df: pd.DataFrame) -> go.Figure:
    """Biểu đồ Donut cơ cấu tỷ trọng doanh thu theo 9 danh mục sản phẩm."""
    data = get_category_share_data(df)
    fig = px.pie(
        names=data["categories"],
        values=data["revenue"],
        hole=0.55,
        title="<b>Tỷ Trọng Doanh Thu Theo 9 Danh Mục Sản Phẩm</b>",
        color_discrete_sequence=["#10B981", "#06B6D4", "#F59E0B", "#8B5CF6", "#3B82F6", "#EC4899", "#14B8A6", "#F97316", "#64748B"]
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827"
    )
    return fig


def plot_price_vs_volume(df: pd.DataFrame) -> go.Figure:
    """Biểu đồ phân tán (Scatter Bubble) giữa Đơn giá trung bình và Sản lượng bán ra."""
    points = get_price_volume_data(df)
    pv_df = pd.DataFrame(points)
    if pv_df.empty:
        return go.Figure()

    fig = px.scatter(
        pv_df,
        x="x",
        y="y",
        size="revenue",
        color="category",
        hover_name="product_type",
        labels={"x": "Tổng sản lượng bán (Ly/Món)", "y": "Đơn giá trung bình ($)", "category": "Danh mục"},
        title="<b>Tương Quan Đơn Giá & Sản Lượng Bán Theo Dòng Sản Phẩm (Kích thước: Doanh thu)</b>"
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827"
    )
    return fig
