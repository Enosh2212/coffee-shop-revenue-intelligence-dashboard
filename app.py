from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List, Dict

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype


# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Coffee Shop Revenue Intelligence Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = APP_DIR / "data" / "coffee_shop_sales_raw.csv"

REQUIRED_COLUMNS = {
    "transaction_id",
    "transaction_date",
    "transaction_time",
    "transaction_qty",
    "store_location",
    "product_id",
    "unit_price",
    "product_category",
    "product_type",
    "product_detail",
}

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
TIME_SLOT_ORDER = ["Morning", "Afternoon", "Evening", "Night"]

COLORWAY = ["#C47A3A", "#2F6F73", "#7C3AED", "#2563EB", "#E11D48", "#16A34A", "#F59E0B", "#64748B", "#9333EA", "#0891B2"]

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = COLORWAY


# =============================================================================
# CSS: MNC / CONSULTING DASHBOARD STYLE
# =============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    :root {
        --bg: #F5F1EA;
        --ink: #111827;
        --muted: #6B7280;
        --card: #FFFFFF;
        --line: rgba(17,24,39,.10);
        --coffee: #7A3F25;
        --coffee2: #C47A3A;
        --teal: #2F6F73;
        --blue: #2563EB;
        --green: #16A34A;
        --red: #DC2626;
        --shadow: 0 12px 30px rgba(17,24,39,.075);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(196,122,58,.14), transparent 36%),
            radial-gradient(circle at top right, rgba(47,111,115,.12), transparent 38%),
            linear-gradient(180deg, #FBF8F3 0%, #F5F1EA 100%);
    }

    .main .block-container {
        padding-top: .75rem;
        padding-bottom: 2rem;
        max-width: 1520px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #1F2937 56%, #2B1D16 100%);
        border-right: 1px solid rgba(255,255,255,.08);
    }

    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #F9FAFB !important;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background: rgba(196,122,58,.92) !important;
        color: white !important;
        max-width: 100%;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        background: rgba(255,255,255,.10);
        border: 1px solid rgba(255,255,255,.24);
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] button {
        color: #111827 !important;
        background: #FFFFFF !important;
    }

    /* Professional visual styling for sidebar expanders */
    [data-testid="stSidebar"] [data-testid="stExpander"],
    [data-testid="stSidebar"] details {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderDetails"],
    [data-testid="stSidebar"] details > div {
        background-color: transparent !important;
    }

    /* Professional visual styling for Reset filters button on dark sidebar */
    [data-testid="stSidebar"] div.stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #C47A3A 0%, #7A3F25 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255,255,255,.18) !important;
        border-radius: 14px !important;
        padding: 0.75rem 1rem !important;
        font-weight: 800 !important;
        box-shadow: 0 10px 24px rgba(0,0,0,.22) !important;
        transition: all 0.2s ease-in-out !important;
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        background: linear-gradient(135deg, #D08A48 0%, #8A472A 100%) !important;
        border-color: rgba(255,255,255,.28) !important;
        transform: translateY(-1px) !important;
    }

    [data-testid="stSidebar"] div.stButton > button p,
    [data-testid="stSidebar"] div.stButton > button span {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    .hero {
        border-radius: 22px;
        padding: 22px 26px;
        margin-bottom: 14px;
        background:
            linear-gradient(135deg, rgba(17,24,39,.96), rgba(31,41,55,.94)),
            radial-gradient(circle at 20% 10%, rgba(196,122,58,.35), transparent 35%);
        box-shadow: var(--shadow);
        border: 1px solid rgba(255,255,255,.08);
        color: white;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: 1.55fr .9fr;
        gap: 18px;
        align-items: center;
    }

    .hero h1 {
        margin: 0;
        color: white;
        font-size: 2rem;
        line-height: 1.06;
        letter-spacing: -.05em;
        font-weight: 850;
    }

    .hero p {
        margin: 10px 0 0;
        color: rgba(255,255,255,.72);
        font-size: .94rem;
        max-width: 900px;
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        margin-bottom: 14px;
        border-radius: 999px;
        background: rgba(196,122,58,.16);
        color: #FED7AA;
        border: 1px solid rgba(251,146,60,.22);
        font-weight: 750;
        font-size: .80rem;
        letter-spacing: .04em;
        text-transform: uppercase;
    }

    .hero-panel {
        background: rgba(255,255,255,.08);
        border: 1px solid rgba(255,255,255,.10);
        border-radius: 16px;
        padding: 16px;
    }

    .hero-panel div {
        color: rgba(255,255,255,.74);
        font-size: .82rem;
        margin-bottom: 8px;
    }

    .hero-panel strong {
        color: white;
        font-size: 1.1rem;
    }

    .metric-card {
        border-radius: 16px;
        padding: 15px 16px 14px;
        background: rgba(255,255,255,.92);
        border: 1px solid var(--line);
        box-shadow: var(--shadow);
        min-height: 116px;
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        height: 4px;
        width: 100%;
        background: linear-gradient(90deg, var(--coffee2), var(--teal));
    }

    .metric-label {
        color: var(--muted);
        text-transform: uppercase;
        font-size: .75rem;
        letter-spacing: .08em;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .metric-value {
        color: var(--ink);
        font-weight: 850;
        font-size: 1.82rem;
        letter-spacing: -.045em;
        line-height: .95;
    }

    .metric-note {
        margin-top: 9px;
        color: var(--muted);
        font-size: .80rem;
        font-weight: 650;
    }

    .metric-positive { color: var(--green); }
    .metric-negative { color: var(--red); }
    .metric-neutral { color: var(--muted); }

    .section-title {
        margin: 12px 0 10px;
        color: var(--ink);
        font-size: 1.18rem;
        font-weight: 850;
        letter-spacing: -.03em;
    }

    .panel-card {
        border-radius: 16px;
        background: rgba(255,255,255,.94);
        border: 1px solid var(--line);
        box-shadow: var(--shadow);
        padding: 16px 18px;
        height: 100%;
    }

    .panel-card h3 {
        font-size: 1rem;
        margin: 0 0 10px;
        color: var(--ink);
        letter-spacing: -.02em;
    }

    .panel-card p, .panel-card li {
        color: #374151;
        font-size: .90rem;
        line-height: 1.48;
    }

    .snapshot-card {
        border-radius: 16px;
        background: rgba(255,255,255,.96);
        border: 1px solid var(--line);
        box-shadow: var(--shadow);
        padding: 14px 18px;
        margin: 10px 0 14px;
        color: #374151;
        font-size: .94rem;
        line-height: 1.5;
    }

    .snapshot-card strong {
        color: var(--ink);
    }

    .panel-card ul {
        margin-bottom: 0;
        padding-left: 1.15rem;
    }

    .tag {
        display: inline-flex;
        border-radius: 999px;
        padding: 6px 10px;
        margin: 4px 6px 4px 0;
        background: rgba(196,122,58,.12);
        color: #7C2D12;
        font-weight: 800;
        font-size: .78rem;
    }

    .warning-box {
        border-left: 5px solid #F59E0B;
    }

    .good-box {
        border-left: 5px solid #16A34A;
    }

    .info-box {
        border-left: 5px solid #2563EB;
    }

    .risk-box {
        border-left: 5px solid #DC2626;
    }

    .small-muted {
        color: var(--muted);
        font-size: .85rem;
    }

    div[data-testid="stTabs"] button {
        font-weight: 800;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        padding: 10px 18px;
        background: rgba(255,255,255,.76);
        border: 1px solid rgba(17,24,39,.10);
    }

    .stTabs [aria-selected="true"] {
        background: #111827 !important;
        color: white !important;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid var(--line);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# DATA PIPELINE
# =============================================================================
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def read_file(uploaded_file) -> pd.DataFrame:
    if uploaded_file is None:
        return pd.read_csv(DEFAULT_DATA)

    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)
    raise ValueError("Please upload a CSV or Excel file only.")


def parse_time_column(series: pd.Series) -> pd.Series:
    """Robust time parser for Excel serials, date-time strings, time strings and pandas StringDtype."""
    s = series.copy()

    if is_numeric_dtype(s):
        parsed = pd.to_datetime(s, unit="D", origin="1899-12-30", errors="coerce")
    else:
        # Convert via Python strings to avoid Pandas ExtensionDtype / NumPy dtype issues.
        text = s.astype("string").fillna("").str.strip()
        parsed = pd.to_datetime(text, errors="coerce")

        # Some plain times may parse poorly in strict environments; retry with explicit time format.
        missing = parsed.isna() & text.ne("")
        if missing.any():
            retry = pd.to_datetime(text[missing], format="%H:%M:%S", errors="coerce")
            parsed.loc[missing] = retry

    return parsed


@st.cache_data(show_spinner=False)
def prepare_data(raw: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    warnings: List[str] = []
    df = normalize_columns(raw)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(sorted(missing)) +
            ". Please use the coffee shop sales schema."
        )

    # Safe type conversion
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df["transaction_time"] = parse_time_column(df["transaction_time"])
    invalid_time_count = int(df["transaction_time"].isna().sum())

    qty_numeric = pd.to_numeric(df["transaction_qty"], errors="coerce")
    price_numeric = pd.to_numeric(df["unit_price"], errors="coerce")
    invalid_qty_count = int(qty_numeric.isna().sum())
    invalid_price_count = int(price_numeric.isna().sum())
    df["transaction_qty"] = qty_numeric.fillna(0)
    df["unit_price"] = price_numeric.fillna(0)

    text_cols = ["store_location", "product_category", "product_type", "product_detail"]
    for col in text_cols:
        df[col] = (
            df[col]
            .astype("string")
            .fillna("Unknown")
            .str.strip()
            .replace("", "Unknown")
        )

    df["product_id"] = pd.to_numeric(df["product_id"], errors="coerce")
    df["transaction_id"] = pd.to_numeric(df["transaction_id"], errors="coerce")

    before = len(df)
    df = df.dropna(subset=["transaction_date", "transaction_id"])
    dropped = before - len(df)
    if dropped:
        warnings.append(f"{dropped:,} rows were removed because transaction date or ID was invalid.")

    if invalid_time_count:
        warnings.append(f"{invalid_time_count:,} rows have invalid transaction time and are treated as 00:00 for time-slot analysis.")
    if invalid_qty_count:
        warnings.append(f"{invalid_qty_count:,} rows have invalid quantity and were treated as 0.")
    if invalid_price_count:
        warnings.append(f"{invalid_price_count:,} rows have invalid unit price and were treated as 0.")

    # Business-ready derived fields
    df["total_revenue"] = df["transaction_qty"] * df["unit_price"]
    df["hour"] = df["transaction_time"].dt.hour.fillna(0).astype(int)
    df["month_number"] = df["transaction_date"].dt.month
    df["month_name"] = df["transaction_date"].dt.month_name()
    df["year_month"] = df["transaction_date"].dt.to_period("M").astype(str)
    df["day_number"] = df["transaction_date"].dt.dayofweek + 1
    df["day_name"] = df["transaction_date"].dt.day_name()
    df["week_start"] = df["transaction_date"].dt.to_period("W").apply(lambda p: p.start_time)

    def time_slot(h: int) -> str:
        if 6 <= h < 12:
            return "Morning"
        if 12 <= h < 17:
            return "Afternoon"
        if 17 <= h < 21:
            return "Evening"
        return "Night"

    df["time_slot"] = df["hour"].apply(time_slot)

    if df.duplicated().sum():
        warnings.append(f"{int(df.duplicated().sum()):,} duplicate rows detected. Kept for transparent audit.")

    return df, warnings


def money(value: float) -> str:
    value = float(value or 0)
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value/1_000:.2f}K"
    return f"${value:,.0f}"


def money_precise(value: float) -> str:
    return f"${float(value or 0):,.2f}"


def num(value: float) -> str:
    value = float(value or 0)
    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"{value/1_000:.0f}K"
    return f"{value:,.0f}"


def pct(value: float, decimals: int = 1) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{float(value):.{decimals}f}%"


def signed_pct(value: float) -> str:
    if pd.isna(value):
        return "No prior month"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.1f}%"


def short_label(value: str, max_len: int = 24) -> str:
    text = str(value)
    return text if len(text) <= max_len else text[: max_len - 3] + "..."


def format_rank_fig(fig: go.Figure) -> go.Figure:
    fig.update_xaxes(tickformat="~s")
    fig.update_traces(textposition="outside", cliponaxis=False)
    return fig


def style_fig(fig: go.Figure, height: int = 390) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=14, t=52, b=14),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Inter, Segoe UI, Arial", size=12, color="#374151"),
        title=dict(font=dict(size=17, color="#111827", family="Inter, Segoe UI, Arial")),
        hoverlabel=dict(bgcolor="#111827", font_color="#FFFFFF", font_size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, title_font=dict(size=12), tickfont=dict(size=11))
    fig.update_yaxes(gridcolor="rgba(107,114,128,.18)", zeroline=False, title_font=dict(size=12), tickfont=dict(size=11))
    return fig


def metric_card(label: str, value: str, note: str, sentiment: str = "neutral") -> None:
    cls = {"positive": "metric-positive", "negative": "metric-negative", "neutral": "metric-neutral"}.get(sentiment, "metric-neutral")
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note {cls}">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def agg(df: pd.DataFrame, group: str) -> pd.DataFrame:
    return (
        df.groupby(group, as_index=False)
        .agg(
            revenue=("total_revenue", "sum"),
            orders=("transaction_id", "nunique"),
            quantity=("transaction_qty", "sum"),
            products=("product_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
    )


def calc_metrics(df: pd.DataFrame) -> Dict[str, float]:
    revenue = float(df["total_revenue"].sum())
    orders = float(df["transaction_id"].nunique())
    qty = float(df["transaction_qty"].sum())
    products = float(df["product_id"].nunique())
    aov = revenue / orders if orders else 0
    items_per_order = qty / orders if orders else 0
    return dict(revenue=revenue, orders=orders, qty=qty, products=products, aov=aov, items_per_order=items_per_order)


# =============================================================================
# SIDEBAR + LOAD
# =============================================================================
with st.sidebar:
    st.markdown("## ☕ Revenue Intelligence")
    st.caption("Sales, product and operations dashboard.")
    
    with st.expander("Upload updated data", expanded=False):
        uploaded = st.file_uploader("Upload newer sales data", type=["csv", "xlsx", "xls"])
        st.caption("Optional: upload a newer CSV/XLSX file with the same schema.")

try:
    raw_df = read_file(uploaded)
    data, warnings = prepare_data(raw_df)
except Exception as e:
    st.error(f"Unable to load data: {e}")
    st.stop()

with st.sidebar:
    min_date, max_date = data["transaction_date"].min().date(), data["transaction_date"].max().date()
    store_options = sorted(data["store_location"].dropna().unique())
    category_options = sorted(data["product_category"].dropna().unique())
    type_options = sorted(data["product_type"].dropna().unique())
    slot_options = [s for s in TIME_SLOT_ORDER if s in set(data["time_slot"])]

    # Safe session state initialization
    if "store_mode" not in st.session_state:
        st.session_state["store_mode"] = "All stores"
    if "category_mode" not in st.session_state:
        st.session_state["category_mode"] = "All categories"
    if "type_mode" not in st.session_state:
        st.session_state["type_mode"] = "All product types"
    if "slot_mode" not in st.session_state:
        st.session_state["slot_mode"] = "All time slots"

    if "selected_stores" not in st.session_state:
        st.session_state["selected_stores"] = store_options
    if "selected_categories" not in st.session_state:
        st.session_state["selected_categories"] = category_options
    if "selected_types" not in st.session_state:
        st.session_state["selected_types"] = type_options
    if "selected_slots" not in st.session_state:
        st.session_state["selected_slots"] = slot_options

    if "date_range" not in st.session_state:
        st.session_state["date_range"] = (min_date, max_date)
    else:
        # Validate that the cached dates are within bounds if file changed
        curr_dates = st.session_state["date_range"]
        if isinstance(curr_dates, tuple) and len(curr_dates) == 2:
            if curr_dates[0] < min_date or curr_dates[1] > max_date:
                st.session_state["date_range"] = (min_date, max_date)

    if "top_n_val" not in st.session_state:
        st.session_state["top_n_val"] = 10

    # 1. Date range
    date_range = st.date_input("Date range", value=st.session_state["date_range"], min_value=min_date, max_value=max_date, key="date_range")

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    # 2. Store Location filter mode
    st.markdown("**Store Location**")
    store_mode = st.radio(
        "Store Location Mode",
        options=["All stores", "Custom"],
        key="store_mode",
        label_visibility="collapsed",
        horizontal=True
    )
    if store_mode == "Custom":
        stores = st.multiselect("Select stores", options=store_options, key="selected_stores", label_visibility="collapsed")
        if not stores:
            stores = store_options
    else:
        stores = store_options

    # 3. Advanced filters expander
    with st.expander("Advanced filters", expanded=False):
        # Product Category
        st.markdown("**Product Category**")
        cat_mode = st.radio(
            "Category Mode",
            options=["All categories", "Custom"],
            key="category_mode",
            label_visibility="collapsed",
            horizontal=True
        )
        if cat_mode == "Custom":
            categories = st.multiselect("Select categories", options=category_options, key="selected_categories", label_visibility="collapsed")
            if not categories:
                categories = category_options
        else:
            categories = category_options

        # Product Type
        st.markdown("**Product Type**")
        type_mode = st.radio(
            "Type Mode",
            options=["All product types", "Custom"],
            key="type_mode",
            label_visibility="collapsed",
            horizontal=True
        )
        if type_mode == "Custom":
            product_types = st.multiselect("Select product types", options=type_options, key="selected_types", label_visibility="collapsed")
            if not product_types:
                product_types = type_options
        else:
            product_types = type_options

        # Time Slot
        st.markdown("**Time Slot**")
        slot_mode = st.radio(
            "Slot Mode",
            options=["All time slots", "Custom"],
            key="slot_mode",
            label_visibility="collapsed",
            horizontal=True
        )
        if slot_mode == "Custom":
            slots = st.multiselect("Select time slots", options=slot_options, key="selected_slots", label_visibility="collapsed")
            if not slots:
                slots = slot_options
        else:
            slots = slot_options

    # 4. Top-N items slider
    top_n = st.slider("Top-N items", 5, 25, key="top_n_val")

    # 5. Reset filters button
    def reset_filters_callback():
        st.session_state["store_mode"] = "All stores"
        st.session_state["category_mode"] = "All categories"
        st.session_state["type_mode"] = "All product types"
        st.session_state["slot_mode"] = "All time slots"
        st.session_state["selected_stores"] = store_options
        st.session_state["selected_categories"] = category_options
        st.session_state["selected_types"] = type_options
        st.session_state["selected_slots"] = slot_options
        st.session_state["date_range"] = (min_date, max_date)
        st.session_state["top_n_val"] = 10

    st.button("Reset filters", on_click=reset_filters_callback, use_container_width=True)

filtered = data[
    (data["transaction_date"].dt.date >= start_date) &
    (data["transaction_date"].dt.date <= end_date) &
    (data["store_location"].isin(stores)) &
    (data["product_category"].isin(categories)) &
    (data["product_type"].isin(product_types)) &
    (data["time_slot"].isin(slots))
].copy()

if filtered.empty:
    st.warning("No rows match the selected filters. Please adjust filters.")
    st.stop()


# =============================================================================
# HERO
# =============================================================================
m = calc_metrics(filtered)
date_text = f"{filtered['transaction_date'].min():%d %b %Y} to {filtered['transaction_date'].max():%d %b %Y}"
store_perf = agg(filtered, "store_location")
category_perf = agg(filtered, "product_category")
top_store = store_perf.iloc[0]["store_location"]
top_store_revenue = float(store_perf.iloc[0]["revenue"])
second_store_revenue = float(store_perf.iloc[1]["revenue"]) if len(store_perf) > 1 else np.nan
top_store_share = top_store_revenue / m["revenue"] * 100 if m["revenue"] else 0
store_gap = top_store_revenue - second_store_revenue if not pd.isna(second_store_revenue) else np.nan
top_category = category_perf.iloc[0]["product_category"]
top_category_revenue = float(category_perf.iloc[0]["revenue"])
top_category_share = top_category_revenue / m["revenue"] * 100 if m["revenue"] else 0

monthly_summary = (
    filtered.groupby("year_month", as_index=False)
    .agg(revenue=("total_revenue", "sum"), orders=("transaction_id", "nunique"), quantity=("transaction_qty", "sum"))
    .sort_values("year_month")
)
monthly_summary["mom_revenue_pct"] = monthly_summary["revenue"].pct_change() * 100
latest_month = monthly_summary.iloc[-1] if not monthly_summary.empty else None
latest_mom_pct = float(latest_month["mom_revenue_pct"]) if latest_month is not None else np.nan
latest_month_label = str(latest_month["year_month"]) if latest_month is not None else "selected period"
best_growth_month = monthly_summary.dropna(subset=["mom_revenue_pct"]).sort_values("mom_revenue_pct", ascending=False)
best_growth_text = (
    f"{best_growth_month.iloc[0]['year_month']} ({signed_pct(float(best_growth_month.iloc[0]['mom_revenue_pct']))})"
    if not best_growth_month.empty else "not available"
)

hour_df = (
    filtered.groupby("hour", as_index=False)
    .agg(orders=("transaction_id", "nunique"), revenue=("total_revenue", "sum"), quantity=("transaction_qty", "sum"))
    .sort_values("hour")
)
hour_orders = hour_df.set_index("hour")["orders"] if not hour_df.empty else pd.Series(dtype=float)
peak_hour = int(hour_orders.idxmax()) if not hour_orders.empty else 0
low_hour = int(hour_orders.idxmin()) if not hour_orders.empty else 0
peak_hour_str = f"{peak_hour:02d}:00"
low_hour_str = f"{low_hour:02d}:00"
peak_orders = int(hour_orders.max()) if not hour_orders.empty else 0
low_orders = int(hour_orders.min()) if not hour_orders.empty else 0
peak_window_start = max(0, peak_hour - 1)
peak_window_end = min(23, peak_hour + 1)
peak_window = f"{peak_window_start:02d}:00-{peak_window_end:02d}:00"

product_perf = (
    filtered.groupby(["product_detail", "product_category"], as_index=False)
    .agg(
        revenue=("total_revenue", "sum"),
        orders=("transaction_id", "nunique"),
        quantity=("transaction_qty", "sum"),
        avg_unit_price=("unit_price", "mean"),
    )
    .sort_values("revenue", ascending=False)
)
product_total_revenue = float(product_perf["revenue"].sum()) if not product_perf.empty else 0
product_perf["revenue_share"] = np.where(product_total_revenue > 0, product_perf["revenue"] / product_total_revenue * 100, 0)
product_perf["cum_share"] = product_perf["revenue_share"].cumsum()
top_product = product_perf.iloc[0] if not product_perf.empty else None
review_product = product_perf.sort_values(["revenue", "quantity"], ascending=True).iloc[0] if not product_perf.empty else None
top_product_share = float(top_product["revenue_share"]) if top_product is not None else 0

business_snapshot = (
    f"For {date_text}, the selected view generated {money(m['revenue'])} from {num(m['orders'])} transactions "
    f"at {money_precise(m['aov'])} AOV. {top_category} contributes {pct(top_category_share)} of revenue, "
    f"{top_store} leads store revenue with {pct(top_store_share)} share, and demand peaks around {peak_window}."
)

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-grid">
            <div>
                <div class="hero-kicker">Client analytics dashboard</div>
                <h1>Coffee Shop Sales & Customer Behavior Intelligence</h1>
                <p>
                    A boardroom-ready dashboard for revenue tracking, product intelligence,
                    demand planning, staffing support and data-driven business recommendations.
                </p>
            </div>
            <div class="hero-panel">
                <div>Analysis window</div>
                <strong>{date_text}</strong>
                <div style="margin-top:14px;">Top store</div>
                <strong>{top_store}</strong>
                <div style="margin-top:14px;">Leading category</div>
                <strong>{top_category}</strong>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if warnings:
    with st.expander("Data quality notes"):
        for w in warnings:
            st.warning(w)


# =============================================================================
# EXECUTIVE SUMMARY
# =============================================================================
st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

# Format dynamic filter summary strictly as requested
if store_mode == "All stores" or len(stores) == len(store_options):
    stores_summary = "All stores"
else:
    stores_summary = f"{len(stores)} stores"

if cat_mode == "All categories" or len(categories) == len(category_options):
    categories_summary = "All categories"
else:
    categories_summary = f"{len(categories)} categories"

if type_mode == "All product types" or len(product_types) == len(type_options):
    types_summary = "All product types"
else:
    types_summary = "Custom product types"

if slot_mode == "All time slots" or len(slots) == len(slot_options):
    slots_summary = "All time slots"
else:
    slots_summary = ", ".join(slots)

date_summary = f"{start_date:%d %b %Y} to {end_date:%d %b %Y}"
filter_summary_str = f"Current view: {stores_summary} • {categories_summary} • {types_summary} • {slots_summary} • {date_summary}"

st.markdown(
    f"""
    <div class="snapshot-card">
        <strong>Business Snapshot:</strong> {business_snapshot}
        <div style="font-size: 0.82rem; color: var(--muted); margin-top: 6px; font-weight: 500;">
            🔍 {filter_summary_str}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
c1, c2, c3, c4 = st.columns(4)
with c1:
    revenue_sentiment = "positive" if pd.isna(latest_mom_pct) or latest_mom_pct >= 0 else "negative"
    metric_card("Total Revenue", money(m["revenue"]), f"{latest_month_label} MoM: {signed_pct(latest_mom_pct)}", revenue_sentiment)
with c2:
    metric_card("Transactions", num(m["orders"]), "Unique customer transactions", "neutral")
with c3:
    metric_card("Average Order Value (AOV)", money_precise(m["aov"]), "Spend per transaction", "neutral")
with c4:
    metric_card("Items Sold", num(m["qty"]), f"{m['items_per_order']:.2f} items/order", "neutral")

c5, c6, c7, c8 = st.columns(4)
with c5:
    metric_card("Distinct Products", num(m["products"]), "Unique product IDs in scope", "neutral")
with c6:
    metric_card("Best Store", top_store, f"{pct(top_store_share)} revenue share", "positive")
with c7:
    metric_card("Top Category", top_category, f"{pct(top_category_share)} revenue share", "positive")
with c8:
    metric_card("Peak Hour", peak_hour_str, f"{num(peak_orders)} transactions", "positive")

# Dynamic business storytelling
st.write("")
story_what, story_why, story_do = st.columns(3)
with story_what:
    st.markdown(
        f"""
        <div class="panel-card info-box">
            <h3>What happened?</h3>
            <p>
                Revenue reached <b>{money(m['revenue'])}</b> from <b>{num(m['orders'])}</b> transactions.
                Latest month revenue movement is <b>{signed_pct(latest_mom_pct)}</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with story_why:
    st.markdown(
        f"""
        <div class="panel-card warning-box">
            <h3>Why it matters</h3>
            <p>
                <b>{top_category}</b> contributes <b>{pct(top_category_share)}</b> of revenue.
                <b>{top_store}</b> leads by <b>{money(store_gap) if not pd.isna(store_gap) else 'n/a'}</b>,
                so small operational changes can shift store rank.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with story_do:
    st.markdown(
        f"""
        <div class="panel-card good-box">
            <h3>What should the client do?</h3>
            <p>
                Staff <b>{peak_window}</b>, protect <b>{top_category}</b> inventory, and review
                <b>{review_product['product_detail'] if review_product is not None else 'low-revenue SKUs'}</b>
                using revenue, quantity and category context.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# =============================================================================
# DASHBOARD TABS
# =============================================================================
overview, product, customer, operations, executive, qa = st.tabs([
    "Boardroom Overview",
    "Product Intelligence",
    "Customer Demand",
    "Operations",
    "Executive Actions",
    "Data QA"
])


with overview:
    st.markdown('<div class="section-title">Boardroom Overview</div>', unsafe_allow_html=True)

    monthly = monthly_summary.copy()

    row1_col1, row1_col2 = st.columns([1.45, 1])
    with row1_col1:
        fig = px.line(
            monthly,
            x="year_month",
            y="revenue",
            markers=True,
            title="Monthly Revenue Trend",
            hover_data={"revenue": ":$,.2f", "orders": ":,", "quantity": ":,", "mom_revenue_pct": ":.1f"},
        )
        fig.update_traces(line=dict(width=4, color="#C47A3A"), marker=dict(size=9))
        fig.update_layout(xaxis_title="Month", yaxis_title="Revenue")
        fig.update_yaxes(tickformat="~s")
        st.plotly_chart(style_fig(fig, 420), use_container_width=True)

    with row1_col2:
        slot_df = agg(filtered, "time_slot").set_index("time_slot").reindex(TIME_SLOT_ORDER[::-1]).dropna().reset_index()
        slot_df["label"] = slot_df["revenue"].apply(money)
        fig = px.bar(
            slot_df,
            x="revenue",
            y="time_slot",
            orientation="h",
            title="Revenue Contribution by Time Slot",
            text="label",
            hover_data={"revenue": ":$,.2f", "orders": ":,", "quantity": ":,"},
        )
        fig.update_traces(marker_color="#2F6F73")
        fig.update_layout(xaxis_title="Revenue", yaxis_title="")
        st.plotly_chart(style_fig(format_rank_fig(fig), 420), use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        store_df = store_perf.copy()
        store_df["share"] = np.where(m["revenue"] > 0, store_df["revenue"] / m["revenue"] * 100, 0)
        store_df["label"] = store_df.apply(lambda r: f"{money(r['revenue'])} | {r['share']:.1f}%", axis=1)
        fig = px.bar(
            store_df.iloc[::-1],
            x="revenue",
            y="store_location",
            orientation="h",
            title="Store Revenue Benchmark",
            text="label",
            hover_data={"revenue": ":$,.2f", "orders": ":,", "quantity": ":,", "share": ":.1f"},
        )
        fig.update_layout(xaxis_title="Revenue", yaxis_title="")
        st.plotly_chart(style_fig(format_rank_fig(fig), 360), use_container_width=True)

    with row2_col2:
        cat_df = category_perf.copy()
        cat_df["share"] = np.where(m["revenue"] > 0, cat_df["revenue"] / m["revenue"] * 100, 0)
        cat_df["label"] = cat_df.apply(lambda r: f"{money(r['revenue'])} | {r['share']:.1f}%", axis=1)
        fig = px.bar(
            cat_df.iloc[::-1],
            x="revenue",
            y="product_category",
            orientation="h",
            title="Revenue by Product Category",
            text="label",
            hover_data={"revenue": ":$,.2f", "orders": ":,", "quantity": ":,", "share": ":.1f"},
        )
        fig.update_layout(xaxis_title="Revenue", yaxis_title="")
        st.plotly_chart(style_fig(format_rank_fig(fig), 360), use_container_width=True)


with product:
    st.markdown('<div class="section-title">Product intelligence</div>', unsafe_allow_html=True)

    top_products = product_perf.head(top_n).copy()
    top_products["product_detail_short"] = top_products["product_detail"].apply(short_label)
    top_products["label"] = top_products["revenue"].apply(money)
    top_products = top_products.iloc[::-1]

    product_types = agg(filtered, "product_type").head(top_n).iloc[::-1]
    cat_df = category_perf.copy()
    cat_df["revenue_share"] = np.where(m["revenue"] > 0, cat_df["revenue"] / m["revenue"] * 100, 0)
    cat_df["label"] = cat_df["revenue_share"].map(lambda x: f"{x:.1f}%")
    
    bottom_products = product_perf.sort_values(["revenue", "quantity"], ascending=True).head(top_n).copy()
    bottom_products["product_detail_short"] = bottom_products["product_detail"].apply(short_label)
    bottom_products["label"] = bottom_products["revenue"].apply(money)
    bottom_products = bottom_products.iloc[::-1]

    pc1, pc2 = st.columns([1.25, 1])
    with pc1:
        fig = px.bar(
            top_products, 
            x="revenue", 
            y="product_detail_short", 
            orientation="h", 
            title="Top Products by Revenue",
            text="label",
            hover_data={
                "product_detail": True,
                "product_category": True,
                "revenue": ":$,.2f",
                "revenue_share": ":.2f",
                "quantity": ":,",
                "orders": ":,",
                "avg_unit_price": ":$,.2f",
                "product_detail_short": False,
                "label": False,
            },
        )
        fig.update_layout(xaxis_title="Revenue", yaxis_title="")
        st.plotly_chart(style_fig(format_rank_fig(fig), 500), use_container_width=True)

    with pc2:
        fig = px.bar(
            cat_df.iloc[::-1],
            x="revenue_share",
            y="product_category",
            orientation="h",
            title="Revenue Share by Category",
            text="label",
            hover_data={"revenue": ":$,.2f", "revenue_share": ":.2f", "orders": ":,", "quantity": ":,"},
        )
        fig.update_traces(marker_color="#2F6F73")
        fig.update_layout(xaxis_title="Revenue Share", yaxis_title="")
        fig.update_xaxes(ticksuffix="%")
        st.plotly_chart(style_fig(fig, 500), use_container_width=True)

    pc3, pc4 = st.columns(2)
    with pc3:
        product_types = product_types.copy()
        product_types["label"] = product_types["revenue"].apply(money)
        fig = px.bar(
            product_types,
            x="revenue",
            y="product_type",
            orientation="h",
            title="Top Product Types",
            text="label",
            hover_data={"revenue": ":$,.2f", "orders": ":,", "quantity": ":,"},
        )
        fig.update_layout(xaxis_title="Revenue", yaxis_title="")
        st.plotly_chart(style_fig(format_rank_fig(fig), 430), use_container_width=True)

    with pc4:
        fig = px.bar(
            bottom_products, 
            x="revenue", 
            y="product_detail_short", 
            orientation="h", 
            title="Products for Review",
            text="label",
            hover_data={
                "product_detail": True,
                "product_category": True,
                "revenue": ":$,.2f",
                "revenue_share": ":.2f",
                "quantity": ":,",
                "orders": ":,",
                "avg_unit_price": ":$,.2f",
                "product_detail_short": False,
                "label": False,
            },
        )
        fig.update_layout(xaxis_title="Revenue", yaxis_title="")
        st.plotly_chart(style_fig(format_rank_fig(fig), 430), use_container_width=True)

    st.markdown(
        f"""
        <div class="panel-card info-box">
            <h3>Product portfolio signal</h3>
            <p>
                <b>{top_product['product_detail'] if top_product is not None else 'Top product'}</b> contributes
                <b>{pct(top_product_share)}</b> of selected revenue. Review low-revenue SKUs with quantity and category context
                before changing pricing, placement, bundling, or discontinuation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown("### Top Product Performance Ledger")
    top_products_table = product_perf.copy()
    top_products_table.insert(0, "rank", np.arange(1, len(top_products_table) + 1))
    top_products_table["abc_class"] = np.select(
        [
            top_products_table["cum_share"] <= 80,
            top_products_table["cum_share"] <= 95,
        ],
        ["A", "B"],
        default="C",
    )
    top_products_table["revenue"] = top_products_table["revenue"].map("${:,.2f}".format)
    top_products_table["orders"] = top_products_table["orders"].map("{:,.0f}".format)
    top_products_table["quantity"] = top_products_table["quantity"].map("{:,.0f}".format)
    top_products_table["avg_unit_price"] = top_products_table["avg_unit_price"].map("${:,.2f}".format)
    top_products_table["revenue_share"] = top_products_table["revenue_share"].map("{:.2f}%".format)
    top_products_table["cum_share"] = top_products_table["cum_share"].map("{:.2f}%".format)
    top_products_table = top_products_table[
        ["rank", "product_detail", "product_category", "revenue", "revenue_share", "cum_share", "abc_class", "orders", "quantity", "avg_unit_price"]
    ]
    top_products_table.columns = [
        "Rank", "Product", "Category", "Revenue", "Revenue Share", "Cumulative Share", "ABC Class", "Orders", "Quantity", "Avg Unit Price"
    ]
    
    st.dataframe(top_products_table, use_container_width=True, height=300)


with customer:
    st.markdown('<div class="section-title">Customer Demand Behavior</div>', unsafe_allow_html=True)
    hour_df = hour_df.copy()
    hour_df["orders_label"] = hour_df["orders"].apply(num)
    hour_df["revenue_label"] = hour_df["revenue"].apply(money)

    dc1, dc2 = st.columns(2)
    with dc1:
        fig = px.bar(
            hour_df,
            x="hour",
            y="orders",
            title="Demand by Hour",
            text="orders_label",
            hover_data={"orders": ":,", "revenue": ":$,.2f", "quantity": ":,", "orders_label": False},
        )
        fig.update_traces(marker_color="#2563EB")
        fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Transactions")
        fig.update_yaxes(tickformat="~s")
        st.plotly_chart(style_fig(fig, 410), use_container_width=True)

    with dc2:
        fig = px.bar(
            hour_df,
            x="hour",
            y="revenue",
            title="Revenue by Hour",
            text="revenue_label",
            hover_data={"orders": ":,", "revenue": ":$,.2f", "quantity": ":,", "revenue_label": False},
        )
        fig.update_traces(marker_color="#C47A3A")
        fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Revenue")
        fig.update_yaxes(tickformat="~s")
        st.plotly_chart(style_fig(fig, 410), use_container_width=True)

    heat = filtered.pivot_table(
        index="day_name",
        columns="hour",
        values="transaction_id",
        aggfunc=pd.Series.nunique,
        fill_value=0,
    )
    heat = heat.reindex([d for d in DAY_ORDER if d in heat.index])
    fig = px.imshow(
        heat,
        labels=dict(x="Hour", y="Day", color="Transactions"),
        title="Day-Hour Demand Heatmap",
        aspect="auto",
        color_continuous_scale="YlOrBr",
    )
    st.plotly_chart(style_fig(fig, 520), use_container_width=True)

    st.markdown(
        f"""
        <div class="panel-card info-box">
            <h3>Demand signal</h3>
            <p>
                Peak demand is concentrated around <b>{peak_window}</b>, with <b>{num(peak_orders)}</b>
                transactions at the highest hour. The lowest observed hour is <b>{low_hour_str}</b>
                with <b>{num(low_orders)}</b> transactions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


with operations:
    st.markdown('<div class="section-title">Operational Performance Planning</div>', unsafe_allow_html=True)

    oc1, oc2 = st.columns(2)
    with oc1:
        day_df = (
            filtered.groupby(["day_number", "day_name"], as_index=False)
            .agg(revenue=("total_revenue", "sum"), orders=("transaction_id", "nunique"))
            .sort_values("day_number")
        )
        fig = px.line(day_df, x="day_name", y="revenue", markers=True, title="Revenue by Day of Week")
        fig.update_traces(line=dict(width=4, color="#2F6F73"), marker=dict(size=9))
        fig.update_layout(xaxis_title="", yaxis_title="Revenue")
        fig.update_yaxes(tickformat="~s")
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with oc2:
        store_slot = filtered.pivot_table(
            index="store_location",
            columns="time_slot",
            values="transaction_id",
            aggfunc=pd.Series.nunique,
            fill_value=0,
        )
        store_slot = store_slot[[c for c in TIME_SLOT_ORDER if c in store_slot.columns]]
        busiest_store_slot = store_slot.stack().sort_values(ascending=False)
        if not busiest_store_slot.empty:
            busiest_store, busiest_slot = busiest_store_slot.index[0]
            busiest_slot_orders = int(busiest_store_slot.iloc[0])
        else:
            busiest_store, busiest_slot, busiest_slot_orders = top_store, "peak", 0
        fig = px.imshow(
            store_slot,
            title="Store Workload Matrix",
            labels=dict(x="Time Slot", y="Store", color="Transactions"),
            color_continuous_scale="Teal",
            aspect="auto",
        )
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.markdown(
            f"""
            <div class="panel-card good-box">
                <h3>Peak staffing window</h3>
                <p>Highest transaction load appears around <b>{peak_window}</b>. Schedule stronger counter and prep support around this period.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with ic2:
        st.markdown(
            f"""
            <div class="panel-card warning-box">
                <h3>Low-demand opportunity</h3>
                <p>Demand is comparatively lower around <b>{low_hour_str}</b>. Use this window for prep work, inventory checks, or targeted offers.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with ic3:
        st.markdown(
            f"""
            <div class="panel-card info-box">
                <h3>Workload focus</h3>
                <p><b>{busiest_store}</b> has the highest slot workload in <b>{busiest_slot}</b> with <b>{num(busiest_slot_orders)}</b> transactions. Align prep and inventory buffers there first.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


with executive:
    st.markdown('<div class="section-title">Executive actions & client-ready recommendations</div>', unsafe_allow_html=True)

    ex1, ex2 = st.columns(2)
    with ex1:
        st.markdown(
            f"""
            <div class="panel-card info-box">
                <h3>Key findings</h3>
                <ul>
                    <li>Total revenue in the selected view is <b>{money(m['revenue'])}</b>.</li>
                    <li>Latest month revenue movement is <b>{signed_pct(latest_mom_pct)}</b>.</li>
                    <li><b>{top_category}</b> leads categories with <b>{pct(top_category_share)}</b> revenue share.</li>
                    <li><b>{top_store}</b> leads stores with <b>{pct(top_store_share)}</b> revenue share.</li>
                    <li>Peak demand window is <b>{peak_window}</b>.</li>
                    <li><b>{top_product['product_detail'] if top_product is not None else 'Top product'}</b> is the top revenue product.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with ex2:
        st.markdown(
            f"""
            <div class="panel-card good-box">
                <h3>Recommended actions</h3>
                <ul>
                    <li>Increase staffing and prep coverage during <b>{peak_window}</b>.</li>
                    <li>Prioritize inventory buffers for <b>{top_category}</b>, which contributes <b>{pct(top_category_share)}</b> of revenue.</li>
                    <li>Use bundles around <b>{top_product['product_detail'] if top_product is not None else 'top products'}</b> to protect AOV.</li>
                    <li>Review <b>{review_product['product_detail'] if review_product is not None else 'low-revenue SKUs'}</b> before pricing or retirement decisions.</li>
                    <li>Use <b>{low_hour_str}</b> as a prep, restock, or targeted-offer window.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="panel-card">
            <h3>Conclusion</h3>
            <p>
                This dashboard converts transaction-level sales data into a decision-ready analytics view. It supports
                ongoing revenue tracking, product portfolio optimization, customer demand analysis and operational planning.
                As new data is added, the dashboard refreshes KPIs, filters, charts and recommendations automatically.
            </p>
            <span class="tag">Revenue intelligence</span>
            <span class="tag">Product analytics</span>
            <span class="tag">Operational planning</span>
            <span class="tag">Client-ready reporting</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


with qa:
    st.markdown('<div class="section-title">Data QA & export center</div>', unsafe_allow_html=True)

    duplicate_rows = int(filtered.duplicated().sum())
    duplicate_transaction_ids = int(filtered["transaction_id"].duplicated().sum())
    missing_cells = int(filtered.isna().sum().sum())
    zero_revenue_rows = int((filtered["total_revenue"] <= 0).sum())
    negative_qty_rows = int((filtered["transaction_qty"] < 0).sum())
    negative_price_rows = int((filtered["unit_price"] < 0).sum())
    filtered_date_range = f"{filtered['transaction_date'].min():%d %b %Y} - {filtered['transaction_date'].max():%d %b %Y}"

    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Total rows", f"{len(data):,}")
    q2.metric("Filtered rows", f"{len(filtered):,}")
    q3.metric("Duplicate rows", f"{duplicate_rows:,}")
    q4.metric("Missing values", f"{missing_cells:,}")

    q5, q6, q7, q8 = st.columns(4)
    q5.metric("Date range", filtered_date_range)
    q6.metric("Stores", f"{filtered['store_location'].nunique():,}")
    q7.metric("Products", f"{filtered['product_id'].nunique():,}")
    q8.metric("Zero/negative revenue rows", f"{zero_revenue_rows:,}")

    qa_flags = []
    if duplicate_transaction_ids:
        qa_flags.append(f"{duplicate_transaction_ids:,} duplicate transaction IDs detected in the filtered data.")
    if negative_qty_rows:
        qa_flags.append(f"{negative_qty_rows:,} rows have negative quantity.")
    if negative_price_rows:
        qa_flags.append(f"{negative_price_rows:,} rows have negative unit price.")
    if zero_revenue_rows:
        qa_flags.append(f"{zero_revenue_rows:,} rows have zero or negative calculated revenue.")
    if qa_flags:
        with st.expander("Data QA flags"):
            for flag in qa_flags:
                st.warning(flag)

    dq1, dq2 = st.columns([.9, 1.1])
    with dq1:
        qa_df = pd.DataFrame({
            "Column": filtered.columns,
            "Missing": [int(filtered[c].isna().sum()) for c in filtered.columns],
            "Unique": [int(filtered[c].nunique(dropna=True)) for c in filtered.columns],
            "Type": [str(filtered[c].dtype) for c in filtered.columns],
        })
        st.dataframe(qa_df, use_container_width=True, height=440)

    with dq2:
        preview_cols = [
            "transaction_id", "transaction_date", "store_location", "product_category",
            "product_type", "product_detail", "transaction_qty", "unit_price", "total_revenue",
        ]
        st.dataframe(filtered[preview_cols].head(700), use_container_width=True, height=440)

        st.download_button(
            "Download filtered dataset",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="coffee_shop_filtered_data.csv",
            mime="text/csv",
            use_container_width=True,
        )
