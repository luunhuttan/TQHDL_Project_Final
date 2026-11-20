"""
Quốc Thái: Phân tích Doanh thu & Chuỗi thời gian (Time-Series Charts)
=====================================================================
File: src/quoc_thai_time_series/time_series_charts.py
Nhiệm vụ: Trả lời câu hỏi "Thời điểm nào bán chạy?"
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Bảng màu chuẩn theo doc
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


def _apply_gentelella_layout(
    fig: go.Figure,
    title_text: str = "",
    subtitle_text: str = "",
) -> go.Figure:
    """
    Helper nội bộ: Áp dụng theme Dark Mode chuẩn Gentelella v4 cho mọi biểu đồ.
    Gọi hàm này ở cuối mỗi hàm plot_* trước khi return fig.

    Tham số:
        fig           – Figure Plotly cần áp dụng style.
        title_text    – Tiêu đề chính (in đậm, trắng).
        subtitle_text – Tiêu đề phụ (nhỏ hơn, màu xám muted).

    Trả về:
        fig đã được cập nhật layout.
    """
    # --- Ghép tiêu đề chính + phụ thành 1 chuỗi HTML Plotly ---
    full_title = f"<b>{title_text}</b>"
    if subtitle_text:
        full_title += (
            f"<br><span style='font-size:12px;"
            f"color:{COLORS['text_secondary']}'>{subtitle_text}</span>"
        )

    fig.update_layout(
        # Tiêu đề
        title={
            "text": full_title,
            "font": {"size": 16, "color": COLORS["text_primary"]},
            "x": 0.02,
            "xanchor": "left",
        },
        # Màu nền chuẩn Gentelella v4 Dark Mode
        paper_bgcolor=COLORS["card"],    # #151D2F – nền khung biểu đồ
        plot_bgcolor=COLORS["canvas"],   # #0B0F19 – nền vùng vẽ bên trong
        # Font chữ toàn bộ
        font={"color": COLORS["text_primary"], "family": "Inter, sans-serif"},
        # Chú thích (legend)
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "font": {"color": COLORS["text_secondary"], "size": 11},
            "bgcolor": "rgba(0,0,0,0)",
        },
        # Margin thoáng
        margin={"l": 50, "r": 30, "t": 70, "b": 50},
        # Hover tooltip style
        hoverlabel={
            "bgcolor": COLORS["card"],
            "bordercolor": COLORS["grid"],
            "font_color": COLORS["text_primary"],
        },
    )

    # Trục X & Y: lưới mảnh màu grid
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

    #Pre-attentive color: chỉ tô màu xanh ngọc cho khung giờ vàn 8h-10h
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
            name="Sản lượng (món/ly)",
            mode="lines+markers",
            line={"color": COLORS["cyan"], "width": 2.5},
            marker={"size": 6, "color": COLORS["cyan"]},
            hovertemplate="Sản lượng: %{y:,} món<extra></extra>",
        ),
        secondary_y=True,
    )

    _apply_gentelella_layout(
        fig,
        title_text=f"Khung giờ vàng 08h-10h đó góp {peak_share:.1f}% tổng doanh thu",
        subtitle_text="Đỉnh cao điểm rơi vào 10h sáng ($88.7k); doanh thu giảm gần 50% từ sau 11h trưa",
    )
    fig.update_yaxes(
        title_text="Doanh thu ($)",
        tickprefix="$",
        tickfont={"color":COLORS["green"]},
        secondary_y=False
    )
    fig.update_yaxes(
        title_text="Sản lượng (món/ly)",
        showgrid=False, # tắt lưới trục phụ để tránh rối
        secondary_y=True
    )
    return fig


def plot_sales_by_day_of_week(df: pd.DataFrame):
    """
    Biểu đồ cột so sánh doanh thu theo Thứ trong tuần (Monday -> Sunday).
    """
    dow = (
        df.groupby("day_name",as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            active_days=("transaction_date", "nunique"),
        )
    )
    #Cố định trục X theo thứ tự từ thứ 2 đến CN
    dow["day_name"] = pd.Categorical(dow["day_name"], categories=DAY_ORDER, ordered=True)
    dow = dow.sort_values("day_name").reset_index(drop=True)
    dow["avg_daily"] = dow["revenue"] / dow["active_days"]

    max_rev = dow["revenue"].max()
    #Tô điểm nhấn Amber cho ngày cao nhất, Cyan cho ngày thường, xám xanh cho cuối tuần
    bar_colors=[
        COLORS["amber"] if rev == max_rev
        else ("#334155" if day in {"Saturday", "Sunday"} else COLORS["cyan"])
        for day, rev in zip(dow["day_name"], dow["revenue"])
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=dow["day_name"],
                y=dow["revenue"],
                marker_color=bar_colors,
                text=[f"${r/1000:.1f}k" for r in dow["revenue"]],
                textposition="outside",
                textfont={"color": COLORS["text_primary"], "size": 11},
                customdata=dow[["active_days", "avg_daily"]],
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Tổng doanh thu: $%{y:,.2f}<br>"
                    "Số ngày mở cửa: %{customdata[0]} ngày<br>"
                    "TB mỗi ngày: $%{customdata[1]:,.2f}<extra></extra>"
                ),
            )
        ]
    )
    _apply_gentelella_layout(
        fig,
        title_text="Sức mua duy trì ổn định quanh $97k–$102k xuyên suốt cả tuần",
        subtitle_text="Thứ 2 dẫn đầu ($101.7k); Thứ 7 thấp hơn về tổng ($96.9k) do ít hơn 1 ngày mở cửa",
    )
    fig.update_yaxes(title_text="Tổng doanh thu ($)", tickprefix="$")
    return fig


def plot_sales_heatmap(df: pd.DataFrame):
    """
    [Quốc Thái] Tuần 2: Ma trận nhiệt (Heatmap) giao thoa Ngày trong tuần × Khung giờ.

    - Đầu vào : DataFrame sạch có cột 'day_name', 'hour', 'revenue', 'quantity'.
    - Đầu ra  : Figure Plotly (go.Heatmap).
    - Thông điệp: Định vị chính xác tọa độ thời gian cao điểm nhất trong tuần —
                  trả lời "Khung giờ nào trong ngày nào đông khách nhất?".

    Insight được mã hoá trực quan:
      · Màu càng sáng (Emerald Glow) = doanh thu/sản lượng càng cao.
      · Tooltip hiển thị đầy đủ: Thứ, Giờ, Doanh thu, Sản lượng.
    """
    # --- 1. Tổng hợp pivot: hàng = Ngày trong tuần, cột = Giờ ---
    agg = (
        df.groupby(["day_name", "hour"], as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"))
    )

    # Pivot thành ma trận 2 chiều
    pivot_rev = agg.pivot(index="day_name", columns="hour", values="revenue").fillna(0)
    pivot_qty = agg.pivot(index="day_name", columns="hour", values="quantity").fillna(0)

    # Sắp xếp hàng theo thứ tự đúng (Mon → Sun)
    pivot_rev = pivot_rev.reindex([d for d in DAY_ORDER if d in pivot_rev.index])
    pivot_qty = pivot_qty.reindex([d for d in DAY_ORDER if d in pivot_qty.index])

    # Nhãn trục X (giờ: "07h", "08h", ...)
    hour_labels = [f"{int(h):02d}h" for h in pivot_rev.columns]

    # --- 2. Vẽ Heatmap ---
    # customdata: nhúng sản lượng vào từng ô để hiện trong hover
    fig = go.Figure(
        go.Heatmap(
            z=pivot_rev.values,
            x=hour_labels,
            y=list(pivot_rev.index),
            customdata=pivot_qty.values,
            colorscale=[
                [0.0,  COLORS["canvas"]],    # thấp nhất = nền tối
                [0.4,  COLORS["muted_bar"]], # trung bình = xanh đậm
                [0.75, COLORS["cyan"]],      # khá cao = cyan
                [1.0,  COLORS["green"]],     # cao nhất = emerald glow
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
        # Đảo ngược trục Y để Thứ 2 nằm trên cùng (đọc từ trên xuống tự nhiên hơn)
        yaxis={"autorange": "reversed"},
    )
    return fig


def plot_trend_over_time(df: pd.DataFrame):
    """
    [Quốc Thái] Biểu đồ xu hướng doanh thu theo dòng thời gian (Ngày & Tháng).

    - Đầu vào : DataFrame sạch có 'transaction_date', 'month_year', 'revenue'.
    - Đầu ra  : Figure Plotly (Area chart theo Tháng + Line chart theo Ngày làm nền).
    - Thông điệp: Theo dõi đà tăng trưởng và tính chu kỳ/mùa vụ của quán cà phê —
                  trả lời "Doanh thu có xu hướng tăng/giảm theo thời gian không?".

    Thiết kế 2 lớp:
      · Lớp nền (mờ): đường theo ngày → thấy biến động ngắn hạn.
      · Lớp nổi (đậm): area chart theo tháng → thấy xu hướng dài hạn rõ ràng.
    """
    # --- 1. Tổng hợp theo Ngày ---
    daily = (
        df.groupby("transaction_date", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values("transaction_date")
    )
    daily["transaction_date"] = pd.to_datetime(daily["transaction_date"])

    # --- 2. Tổng hợp theo Tháng ---
    monthly = (
        df.groupby("month_year", as_index=False)
        .agg(revenue=("revenue", "sum"))
    )
    # Chuyển "2023-01" → datetime để sort đúng thứ tự
    monthly["month_dt"] = pd.to_datetime(monthly["month_year"] + "-01")
    monthly = monthly.sort_values("month_dt")

    # --- 3. Vẽ biểu đồ ---
    fig = go.Figure()

    # Lớp 1: Đường doanh thu ngày (mờ, làm nền để thấy dao động)
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

    # Lớp 2: Area chart doanh thu tháng (nổi bật, là insight chính)
    fig.add_trace(
        go.Scatter(
            x=monthly["month_dt"],
            y=monthly["revenue"],
            name="Doanh thu mỗi tháng",
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(16, 185, 129, 0.15)",   # green với opacity thấp
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
        # Hiện 2 legend để phân biệt lớp ngày vs tháng
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02,
                "xanchor": "right", "x": 1},
    )
    return fig

