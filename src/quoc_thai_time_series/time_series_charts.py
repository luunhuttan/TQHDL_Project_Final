"""
Quốc Thái: Phân tích Doanh thu & Chuỗi thời gian (Time-Series Charts)
=====================================================================
File: src/quoc_thai_time_series/time_series_charts.py
Nhiệm vụ: Trả lời câu hỏi "Thời điểm nào bán chạy?"
- Cung cấp các hàm vẽ biểu đồ Plotly (EDA & Notebook & Báo cáo)
- Cung cấp các hàm trích xuất dữ liệu JSON (cho Flask Dashboard)
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Bảng màu chuẩn theo thiết kế Gentelella v4 Dark Mode
COLORS = {
    "canvas": "#0B0F19",
    "card": "#151D2F",
    "grid": "#1F293D",
    "green": "#10B981",
    "cyan": "#06B6D4",
    "amber": "#F59E0B",
    "muted_bar": "#1E3A5F",
    "text_primary": "#F8FAFC",
    "text_secondary": "#94A3B8",
}

DAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]
ORDER_DAYS_VN = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
ORDER_DAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ==============================================================================
# 1. HÀM TRÍCH XUẤT DỮ LIỆU JSON (PHỤC VỤ FLASK REST API CHO DASHBOARD)
# ==============================================================================

def get_hourly_sales_data(df: pd.DataFrame) -> dict:
    """Tổng hợp doanh thu & sản lượng theo 24 khung giờ."""
    if df.empty:
        return {"labels": [f"{h:02d}h" for h in range(6, 21)], "revenue": [0] * 15, "quantity": [0] * 15}

    hours = list(range(6, 21))
    hourly = (
        df.groupby("hour", as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"))
    )
    hourly_indexed = hourly.set_index("hour").reindex(hours, fill_value=0).reset_index()

    return {
        "labels": [f"{h:02d}h" for h in hourly_indexed["hour"]],
        "revenue": [round(float(v), 2) for v in hourly_indexed["revenue"]],
        "quantity": [int(v) for v in hourly_indexed["quantity"]]
    }


def get_weekly_sales_data(df: pd.DataFrame) -> dict:
    """Tổng hợp doanh thu & sản lượng theo thứ trong tuần (Thứ 2 -> Chủ Nhật)."""
    if df.empty:
        return {"labels": ORDER_DAYS_VN, "revenue": [0] * 7, "quantity": [0] * 7}

    weekly = (
        df.groupby("day_name", as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"))
    )
    weekly_indexed = weekly.set_index("day_name").reindex(ORDER_DAYS_EN, fill_value=0).reset_index()

    return {
        "labels": ORDER_DAYS_VN,
        "revenue": [round(float(v), 2) for v in weekly_indexed["revenue"]],
        "quantity": [int(v) for v in weekly_indexed["quantity"]]
    }


def get_heatmap_data(df: pd.DataFrame) -> dict:
    """Tạo ma trận nhiệt 2 chiều: 7 Thứ trong tuần x 15 Khung giờ (6h - 20h)."""
    hours = list(range(6, 21))
    if df.empty:
        return {
            "days": ORDER_DAYS_VN,
            "hours": [f"{h:02d}h" for h in hours],
            "matrix": [[0.0 for _ in hours] for _ in ORDER_DAYS_VN],
            "max_value": 0.0
        }

    pivot = df.pivot_table(
        index="day_name",
        columns="hour",
        values="revenue",
        aggfunc="sum",
        fill_value=0.0
    )
    pivot = pivot.reindex(index=ORDER_DAYS_EN, columns=hours, fill_value=0.0)
    matrix = np.round(pivot.values, 2).tolist()
    max_val = float(np.max(pivot.values)) if pivot.values.size > 0 else 0.0

    return {
        "days": ORDER_DAYS_VN,
        "hours": [f"{h:02d}h" for h in hours],
        "matrix": matrix,
        "max_value": round(max_val, 2)
    }


def get_monthly_trend_data(df: pd.DataFrame) -> dict:
    """Tổng hợp xu hướng doanh thu theo tháng."""
    if df.empty:
        return {"labels": [], "revenue": [], "quantity": []}

    monthly = (
        df.groupby("month_year", as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"))
        .sort_values("month_year")
    )
    return {
        "labels": [f"Tháng {m[5:]}/{m[:4]}" for m in monthly["month_year"]],
        "revenue": [round(float(v), 2) for v in monthly["revenue"]],
        "quantity": [int(v) for v in monthly["quantity"]]
    }


def get_daily_trend_data(df: pd.DataFrame) -> dict:
    """Tổng hợp xu hướng doanh thu theo từng ngày giao dịch."""
    if df.empty:
        return {"labels": [], "revenue": [], "quantity": []}

    daily = (
        df.groupby("transaction_date", as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"))
        .sort_values("transaction_date")
    )
    return {
        "labels": [str(d) for d in daily["transaction_date"]],
        "revenue": [round(float(v), 2) for v in daily["revenue"]],
        "quantity": [int(v) for v in daily["quantity"]]
    }


# ==============================================================================
# 2. HÀM VẼ BIỂU ĐỒ PLOTLY CHUẨN GENTELELLA V4 DARK MODE
# ==============================================================================

def _apply_gentelella_layout(
    fig: go.Figure,
    title_text: str = "",
    subtitle_text: str = "",
) -> go.Figure:
    """
    Helper nội bộ: Áp dụng theme Dark Mode chuẩn Gentelella v4 cho mọi biểu đồ.
    Gọi hàm này ở cuối mỗi hàm plot_* trước khi return fig.
    """
    full_title = f"<b>{title_text}</b>"
    if subtitle_text:
        full_title += (
            f"<br><span style='font-size:12px;"
            f"color:{COLORS['text_secondary']}'>{subtitle_text}</span>"
        )

    fig.update_layout(
        title={
            "text": full_title,
            "font": {"size": 16, "color": COLORS["text_primary"]},
            "x": 0.02,
            "xanchor": "left",
        },
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["canvas"],
        font={"color": COLORS["text_primary"], "family": "Inter, sans-serif"},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "font": {"color": COLORS["text_secondary"], "size": 11},
            "bgcolor": "rgba(0,0,0,0)",
        },
        margin={"l": 50, "r": 30, "t": 70, "b": 50},
        hoverlabel={
            "bgcolor": COLORS["card"],
            "bordercolor": COLORS["grid"],
            "font_color": COLORS["text_primary"],
        },
    )

    fig.update_xaxes(
        gridcolor=COLORS["grid"],
        linecolor=COLORS["grid"],
        tickfont={"color": COLORS["text_secondary"]},
        title_font={"color": COLORS["text_secondary"]},
        zeroline=False,
    )
    fig.update_yaxes(
        gridcolor=COLORS["grid"],
        linecolor=COLORS["grid"],
        tickfont={"color": COLORS["text_secondary"]},
        title_font={"color": COLORS["text_secondary"]},
        zeroline=False,
    )

    return fig


def plot_hourly_sales(df: pd.DataFrame):
    """
    Biểu đồ kết hợp Doanh thu (Cột) & Sản lượng (Đường) theo khung giờ (06-20h).
    """
    hourly = (
        df.groupby("hour", as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"))
        .sort_values("hour")
    )

    total_rev = hourly["revenue"].sum()
    peak_hours = {8, 9, 10}
    peak_share = hourly.loc[hourly["hour"].isin(peak_hours), "revenue"].sum() / total_rev * 100

    bar_colors = [
        COLORS["green"] if h in peak_hours else COLORS["muted_bar"]
        for h in hourly["hour"]
    ]
    hour_labels = [f"{int(h):02d}h" for h in hourly["hour"]]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=hour_labels,
            y=hourly["revenue"],
            name="Doanh thu ($)",
            marker_color=bar_colors,
            hovertemplate="Doanh thu: $%{y:,.2f}<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=hour_labels,
            y=hourly["quantity"],
            name="Sản lượng (ly)",
            mode="lines+markers",
            line={"color": COLORS["cyan"], "width": 2.5},
            marker={"size": 6, "color": COLORS["cyan"]},
            hovertemplate="Sản lượng: %{y:,} ly<extra></extra>",
        ),
        secondary_y=True,
    )

    fig.add_annotation(
        x="09h",
        y=hourly.loc[hourly["hour"] == 9, "revenue"].values[0],
        text=f"Khung giờ vàng 8h-10h<br><b>{peak_share:.1f}%</b> tổng doanh thu",
        showarrow=True,
        arrowhead=2,
        arrowcolor=COLORS["green"],
        arrowsize=1,
        arrowwidth=1.5,
        ax=40,
        ay=-50,
        font={"color": COLORS["green"], "size": 11},
        bgcolor=COLORS["card"],
        bordercolor=COLORS["green"],
        borderwidth=1,
        borderpad=4,
    )

    _apply_gentelella_layout(
        fig,
        title_text="Doanh thu & Sản lượng theo Khung giờ",
        subtitle_text="Đỉnh điểm 8h–10h sáng chiếm gần 1/3 doanh thu cả ngày",
    )
    fig.update_layout(
        xaxis_title="Khung giờ trong ngày",
        yaxis_title="Doanh thu ($)",
        yaxis={"tickprefix": "$"},
        yaxis2={
            "title": "Sản lượng (ly)",
            "overlaying": "y",
            "side": "right",
            "showgrid": False,
            "tickfont": {"color": COLORS["cyan"]},
            "title_font": {"color": COLORS["cyan"]},
        },
    )
    return fig


def plot_sales_by_day_of_week(df: pd.DataFrame):
    """
    Biểu đồ cột so sánh Doanh thu theo Thứ trong tuần (Monday -> Sunday).
    """
    weekly = (
        df.groupby("day_name", as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"))
    )

    weekly["day_name"] = pd.Categorical(weekly["day_name"], categories=DAY_ORDER, ordered=True)
    weekly = weekly.sort_values("day_name").reset_index(drop=True)

    avg_revenue = weekly["revenue"].mean()
    max_day = weekly.loc[weekly["revenue"].idxmax(), "day_name"]

    bar_colors = [
        COLORS["green"] if d == max_day else COLORS["muted_bar"]
        for d in weekly["day_name"]
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=weekly["day_name"],
            y=weekly["revenue"],
            name="Doanh thu ngày",
            marker_color=bar_colors,
            text=weekly["revenue"].apply(lambda v: f"${v:,.0f}"),
            textposition="outside",
            textfont={"color": COLORS["text_secondary"], "size": 11},
            hovertemplate="<b>%{x}</b><br>Doanh thu: $%{y:,.2f}<extra></extra>",
        )
    )

    fig.add_hline(
        y=avg_revenue,
        line_dash="dash",
        line_color=COLORS["amber"],
        line_width=1.5,
        annotation_text=f"Trung bình: ${avg_revenue:,.0f}/ngày",
        annotation_position="top right",
        annotation_font={"color": COLORS["amber"], "size": 11},
    )

    _apply_gentelella_layout(
        fig,
        title_text="Doanh thu theo Thứ trong tuần",
        subtitle_text=f"Doanh thu phân bổ đồng đều các ngày trong tuần; {max_day} đạt cao nhất",
    )
    fig.update_layout(
        xaxis_title="Thứ trong tuần",
        yaxis_title="Doanh thu ($)",
        yaxis={"tickprefix": "$", "range": [0, weekly["revenue"].max() * 1.18]},
        showlegend=False,
    )
    return fig


def plot_sales_heatmap(df: pd.DataFrame):
    """
    Biểu đồ Heatmap giao thoa giữa Thứ trong tuần (Y) và Khung giờ (X).
    """
    hours_range = list(range(6, 21))
    pivot_rev = (
        df.pivot_table(
            index="day_name",
            columns="hour",
            values="revenue",
            aggfunc="sum",
            fill_value=0,
        )
        .reindex(index=DAY_ORDER, columns=hours_range, fill_value=0)
    )

    pivot_qty = (
        df.pivot_table(
            index="day_name",
            columns="hour",
            values="quantity",
            aggfunc="sum",
            fill_value=0,
        )
        .reindex(index=DAY_ORDER, columns=hours_range, fill_value=0)
    )

    hour_labels = [f"{int(h):02d}h" for h in hours_range]

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_rev.values,
            x=hour_labels,
            y=pivot_rev.index.tolist(),
            customdata=pivot_qty.values,
            colorscale=[
                [0.0,  COLORS["canvas"]],
                [0.15, COLORS["card"]],
                [0.4,  COLORS["muted_bar"]],
                [0.75, COLORS["cyan"]],
                [1.0,  COLORS["green"]],
            ],
            hovertemplate=(
                "<b>%{y} · %{x}</b><br>"
                "Doanh thu: $%{z:,.0f}<br>"
                "Sản lượng: %{customdata:,} món"
                "<extra></extra>"
            ),
            showscale=True,
            colorbar={
                "title": {"text": "Doanh thu ($)", "side": "right"},
                "tickprefix": "$",
                "tickfont": {"color": COLORS["text_secondary"]},
                "title_font": {"color": COLORS["text_secondary"]},
                "bgcolor": COLORS["card"],
                "bordercolor": COLORS["grid"],
            },
        )
    )

    _apply_gentelella_layout(
        fig,
        title_text="Bản đồ nhiệt: Doanh thu theo Thứ × Khung giờ",
        subtitle_text=(
            "Màu càng sáng = doanh thu càng cao · "
            "Cao điểm tập trung 8h–11h các ngày Thứ 2–Thứ 6"
        ),
    )
    fig.update_layout(
        xaxis_title="Khung giờ trong ngày",
        yaxis_title="Ngày trong tuần",
        yaxis={"autorange": "reversed"},
    )
    return fig


def plot_trend_over_time(df: pd.DataFrame):
    """
    Biểu đồ xu hướng doanh thu theo dòng thời gian (Ngày & Tháng).
    """
    daily = (
        df.groupby("transaction_date", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values("transaction_date")
    )
    daily["transaction_date"] = pd.to_datetime(daily["transaction_date"])

    monthly = (
        df.groupby("month_year", as_index=False)
        .agg(revenue=("revenue", "sum"))
    )
    monthly["month_dt"] = pd.to_datetime(monthly["month_year"] + "-01")
    monthly = monthly.sort_values("month_dt")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=daily["transaction_date"],
            y=daily["revenue"],
            name="Doanh thu mỗi ngày",
            mode="lines",
            line={"color": COLORS["muted_bar"], "width": 1},
            opacity=0.6,
            hovertemplate="Ngày %{x|%d/%m/%Y}: $%{y:,.0f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=monthly["month_dt"],
            y=monthly["revenue"],
            name="Doanh thu mỗi tháng",
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(16, 185, 129, 0.15)",
            line={"color": COLORS["green"], "width": 2.5},
            marker={"size": 8, "color": COLORS["green"],
                    "line": {"width": 1.5, "color": COLORS["canvas"]}},
            hovertemplate=(
                "<b>Tháng %{x|%m/%Y}</b><br>"
                "Tổng doanh thu: $%{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    _apply_gentelella_layout(
        fig,
        title_text="Xu hướng Doanh thu: Tăng trưởng mạnh từ T1 → T6/2023",
        subtitle_text=(
            "Đường nền = biến động hằng ngày · "
            "Vùng xanh = tổng tháng · Trend tăng đều ~15–20% mỗi tháng"
        ),
    )
    fig.update_layout(
        xaxis_title="Thời gian",
        yaxis_title="Doanh thu ($)",
        yaxis={"tickprefix": "$"},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02,
                "xanchor": "right", "x": 1},
    )
    return fig
