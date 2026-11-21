import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Coffee Sales Intelligence",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DESIGN SYSTEM — FONTS, COLORS, GLOBAL STYLES
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --canvas: #1C140D;
    --canvas-deep: #140E09;
    --canvas-soft: #2A1F15;
    --surface: #FBF7F0;
    --ink: #241A11;
    --ink-soft: #7A6A57;
    --paper: #FBF7F0;
    --paper-soft: rgba(251, 247, 240, 0.62);
    --gold: #D9A441;
    --wine: #7C2D3B;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--canvas);
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    max-width: 1440px;
}

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

hr { border-color: rgba(251, 247, 240, 0.12) !important; }
small { color: var(--paper-soft) !important; }

/* ---------- Hero ---------- */
.hero {
    background: linear-gradient(120deg, #241A11 0%, #3B2718 60%, #5C3A1E 100%);
    border-radius: 22px;
    padding: 34px 38px;
    margin-bottom: 26px;
}
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: var(--paper);
    letter-spacing: -0.3px;
    margin: 0;
    line-height: 1.25;
}
.hero-subtitle {
    color: var(--paper-soft);
    font-size: 14px;
    margin-top: 8px;
    max-width: 580px;
    line-height: 1.55;
}

/* ---------- Section headings on the dark canvas ---------- */
.section-title {
    font-family: 'Sora', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--paper);
    margin-top: 6px;
    margin-bottom: 2px;
}
.section-description {
    color: var(--paper-soft);
    font-size: 13px;
    margin-bottom: 16px;
}

/* ---------- KPI cards ---------- */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 14px;
    margin-bottom: 6px;
}
.kpi-card {
    background: var(--surface);
    border-radius: 16px;
    padding: 18px 20px;
    border-left: 4px solid var(--gold);
    display: flex;
    align-items: center;
    gap: 14px;
}
.kpi-icon {
    width: 40px;
    height: 40px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.kpi-label {
    font-size: 12.5px;
    font-weight: 500;
    color: var(--ink-soft);
    margin-bottom: 3px;
}
.kpi-value {
    font-family: 'Sora', sans-serif;
    font-size: 21px;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -0.3px;
}

/* ---------- Plotly chart cards ---------- */
div[data-testid="stPlotlyChart"] {
    background: var(--surface);
    border-radius: 18px;
    padding: 16px 16px 6px 16px;
    border: 1px solid rgba(251, 247, 240, 0.08);
}

/* ---------- Dataframe cards ---------- */
div[data-testid="stDataFrame"] {
    background: var(--surface);
    border-radius: 16px;
    padding: 8px;
    overflow: hidden;
    border: 1px solid rgba(251, 247, 240, 0.08);
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--canvas-deep);
}
.sidebar-brand {
    font-family: 'Sora', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--paper);
    margin-top: 2px;
}
.sidebar-tagline {
    font-size: 12.5px;
    color: var(--paper-soft);
    margin-bottom: 2px;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown {
    color: var(--paper) !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: var(--canvas-soft) !important;
    border-color: rgba(251, 247, 240, 0.15) !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: var(--paper) !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: var(--gold) !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] * {
    color: var(--canvas) !important;
}
section[data-testid="stSidebar"] input {
    background-color: var(--canvas-soft) !important;
    color: var(--paper) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(251, 247, 240, 0.15) !important;
}
section[data-testid="stSidebar"] svg {
    fill: rgba(251, 247, 240, 0.7);
}
div[data-baseweb="popover"] ul,
ul[data-baseweb="menu"] {
    background-color: var(--canvas-soft) !important;
}
li[role="option"] {
    color: var(--paper) !important;
}
li[role="option"]:hover {
    background-color: rgba(217, 164, 65, 0.18) !important;
}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {
    font-weight: 600;
    color: var(--paper-soft) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--gold) !important;
}
div[data-baseweb="tab-highlight"] {
    background-color: var(--gold) !important;
}
div[data-baseweb="tab-border"] {
    background-color: rgba(251, 247, 240, 0.08) !important;
}

/* ---------- Buttons ---------- */
.stDownloadButton button {
    background: var(--gold);
    color: var(--canvas);
    border-radius: 10px;
    border: none;
    font-weight: 700;
    padding: 10px 22px;
}
.stDownloadButton button:hover {
    background: #C69433;
    color: var(--canvas);
}

/* ---------- Alerts ---------- */
div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* ---------- Footer ---------- */
.footer-note {
    color: var(--paper-soft);
    font-size: 12.5px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DESIGN HELPERS
# ============================================================

GOLD = "#D9A441"
WINE = "#7C2D3B"

CHART_COLORS = [
    "#D9A441", "#7C2D3B", "#B3773A", "#4A3323",
    "#E8C27A", "#9C4F5A", "#6B5C4C", "#C98A4B"
]

ROAST_SCALE = ["#F1DDB0", "#D9A441", "#7C2D3B"]


def style_fig(fig, height=420):
    """Apply the dashboard's shared Plotly look to any figure."""

    fig.update_layout(
        height=height,
        template="plotly_white",
        font=dict(family="Inter, sans-serif", color="#241A11", size=12),
        title_font=dict(family="Sora, sans-serif", size=15, color="#241A11"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(
            font=dict(family="Inter, sans-serif", size=11, color="#7A6A57"),
            bgcolor="rgba(0,0,0,0)"
        ),
        hoverlabel=dict(
            bgcolor="#241A11",
            font=dict(family="Inter, sans-serif", color="#FBF7F0")
        )
    )

    axis_style = dict(
        showgrid=True,
        gridcolor="rgba(36,26,17,0.08)",
        zeroline=False,
        color="#7A6A57",
        title_font=dict(family="Inter, sans-serif", size=12, color="#7A6A57"),
        tickfont=dict(family="Inter, sans-serif", color="#7A6A57")
    )

    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)

    return fig


def kpi_card(icon, label, value, accent):
    """Build one KPI card as an HTML snippet."""

    icon_bg = f"{accent}22"

    return f"""
    <div class="kpi-card" style="border-left-color:{accent};">
        <div class="kpi-icon" style="background:{icon_bg}; color:{accent};">{icon}</div>
        <div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    </div>
    """


def render_html(html):
    """
    Render a block of custom HTML through st.markdown.

    Streamlit's Markdown parser treats any line starting with 4+ spaces as a
    preformatted code block, even with unsafe_allow_html=True — so a nicely
    indented multi-line HTML string (like the ones above) silently stops
    being parsed as HTML partway through. Collapsing all whitespace to single
    spaces keeps the source readable while guaranteeing it always renders as
    HTML rather than falling back to a visible code block.
    """

    st.markdown(" ".join(html.split()), unsafe_allow_html=True)


# ============================================================
# MYSQL CONNECTION + LOAD DATA
# ============================================================

def connect_db():
    """Connect to the local MySQL database."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="coffee_sales_db",
            port=3306
        )
    except mysql.connector.Error as error:
        st.error(f"MySQL connection failed: {error}")
        return None


def get_mysql_tables():
    """Return the table names available in coffee_sales_db."""
    connection = connect_db()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables
    except mysql.connector.Error as error:
        st.error(f"Could not read database tables: {error}")
        return []
    finally:
        connection.close()


@st.cache_data(ttl=300)
def load_data(table_name):
    """Load the selected MySQL table into a Pandas DataFrame."""
    connection = connect_db()
    if connection is None:
        return pd.DataFrame()

    try:
        # Table name comes from SHOW TABLES, then is escaped as a MySQL identifier.
        safe_table_name = table_name.replace("`", "``")
        query = f"SELECT * FROM `{safe_table_name}`"
        df = pd.read_sql(query, connection)
    except Exception as error:
        st.error(f"Could not load table '{table_name}': {error}")
        return pd.DataFrame()
    finally:
        connection.close()

    required_columns = [
        "transaction_date",
        "sales_value",
        "transaction_qty",
        "unit_price",
        "product_category",
        "product_type",
        "store_id",
        "transaction_id",
        "product_detail"
    ]
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        st.error(
            "The selected MySQL table is missing dashboard columns: "
            + ", ".join(missing_columns)
        )
        st.info(
            "The dashboard expects the same column names as your "
            "coffee_sales_clean.csv file. Rename/map the SQL columns or select "
            "the correct table."
        )
        return pd.DataFrame()

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"], errors="coerce"
    )
    for column in ["sales_value", "transaction_qty", "unit_price"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


# ------------------------------------------------------------
# ============================================================
# GENERIC MYSQL CRUD OPERATIONS FOR ALL TABLES
# ============================================================

from decimal import Decimal
from datetime import time as datetime_time
import json


def quote_identifier(name):
    """Safely quote a MySQL table or column identifier."""
    return "`" + str(name).replace("`", "``") + "`"


def get_table_schema(table_name):
    """Return column metadata and primary-key columns for a table."""
    connection = connect_db()
    if connection is None:
        return [], []

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            f"SHOW COLUMNS FROM {quote_identifier(table_name)}"
        )
        columns = cursor.fetchall()

        cursor.execute(
            f"SHOW KEYS FROM {quote_identifier(table_name)} "
            "WHERE Key_name = 'PRIMARY'"
        )
        key_rows = cursor.fetchall()

        primary_keys = [
            row["Column_name"]
            for row in sorted(
                key_rows,
                key=lambda row: row["Seq_in_index"]
            )
        ]
        return columns, primary_keys

    except mysql.connector.Error as error:
        st.error(f"Could not read table structure: {error}")
        return [], []

    finally:
        cursor.close()
        connection.close()


def read_table(table_name):
    """Read the latest records directly from the selected MySQL table."""
    connection = connect_db()
    if connection is None:
        return pd.DataFrame()

    try:
        query = f"SELECT * FROM {quote_identifier(table_name)}"
        return pd.read_sql(query, connection)

    except Exception as error:
        st.error(f"Could not read '{table_name}': {error}")
        return pd.DataFrame()

    finally:
        connection.close()


class _OmitValue:
    """Sentinel meaning that MySQL should use a column's default."""
    pass


OMIT_VALUE = _OmitValue()


def normalize_sql_value(value):
    """Convert Pandas/NumPy scalar values into MySQL-friendly values."""
    if value is None:
        return None

    if hasattr(value, "item"):
        try:
            value = value.item()
        except Exception:
            pass

    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    if isinstance(value, pd.Timedelta):
        return str(value)

    return value


def convert_input(value, column):
    """Convert a text-input value according to its MySQL column type."""
    field = column["Field"]
    mysql_type = column["Type"].lower()
    base_type = mysql_type.split("(")[0].split()[0]
    extra = str(column.get("Extra", "")).lower()

    if value is None or str(value).strip() == "":
        if "auto_increment" in extra or "generated" in extra:
            return OMIT_VALUE

        if column.get("Default") is not None:
            return OMIT_VALUE

        if column.get("Null") == "YES":
            return None

        raise ValueError(f"'{field}' is required.")

    value = str(value).strip()

    if base_type in {
        "tinyint", "smallint", "mediumint",
        "int", "integer", "bigint", "year"
    }:
        return int(value)

    if base_type in {"decimal", "numeric"}:
        return Decimal(value)

    if base_type in {"float", "double", "real"}:
        return float(value)

    if base_type == "date":
        return pd.to_datetime(value).date()

    if base_type in {"datetime", "timestamp"}:
        return pd.to_datetime(value).to_pydatetime()

    if base_type == "time":
        try:
            return datetime_time.fromisoformat(value)
        except ValueError:
            # Also accept Pandas timedelta-style TIME values.
            return str(pd.to_timedelta(value))

    if base_type == "json":
        json.loads(value)
        return value

    if base_type in {"bit"}:
        return int(value, 0)

    # VARCHAR, CHAR, TEXT, ENUM, SET and other string-compatible types.
    return value


def insert_generic(table_name, columns, values):
    """Insert a row into any selected table and commit it to MySQL."""
    connection = connect_db()
    if connection is None:
        return False, "Could not connect to MySQL."

    cursor = connection.cursor()
    try:
        included = [
            (column, value)
            for column, value in zip(columns, values)
            if value is not OMIT_VALUE
        ]

        if not included:
            cursor.execute(
                f"INSERT INTO {quote_identifier(table_name)} () VALUES ()"
            )
        else:
            column_names = ", ".join(
                quote_identifier(column["Field"])
                for column, _ in included
            )
            placeholders = ", ".join(["%s"] * len(included))
            params = tuple(
                normalize_sql_value(value)
                for _, value in included
            )

            query = (
                f"INSERT INTO {quote_identifier(table_name)} "
                f"({column_names}) VALUES ({placeholders})"
            )
            cursor.execute(query, params)

        connection.commit()
        return True, (
            f"Record inserted successfully into '{table_name}'."
        )

    except (mysql.connector.Error, ValueError) as error:
        connection.rollback()
        return False, f"Insert failed: {error}"

    finally:
        cursor.close()
        connection.close()


def update_generic(
    table_name,
    columns,
    primary_keys,
    original_key_values,
    values
):
    """Update a row using its primary key (supports composite keys)."""
    editable = [
        (column, value)
        for column, value in zip(columns, values)
        if column["Field"] not in primary_keys
        and value is not OMIT_VALUE
    ]

    if not editable:
        return False, "No editable column values were supplied."

    connection = connect_db()
    if connection is None:
        return False, "Could not connect to MySQL."

    cursor = connection.cursor()
    try:
        set_clause = ", ".join(
            f"{quote_identifier(column['Field'])} = %s"
            for column, _ in editable
        )
        where_clause = " AND ".join(
            f"{quote_identifier(key)} = %s"
            for key in primary_keys
        )

        params = (
            tuple(
                normalize_sql_value(value)
                for _, value in editable
            )
            + tuple(
                normalize_sql_value(value)
                for value in original_key_values
            )
        )

        query = (
            f"UPDATE {quote_identifier(table_name)} "
            f"SET {set_clause} WHERE {where_clause}"
        )
        cursor.execute(query, params)

        if cursor.rowcount == 0:
            # MySQL reports zero when the supplied values are unchanged.
            cursor.execute(
                f"SELECT 1 FROM {quote_identifier(table_name)} "
                f"WHERE {where_clause} LIMIT 1",
                tuple(
                    normalize_sql_value(value)
                    for value in original_key_values
                )
            )
            if cursor.fetchone() is None:
                connection.rollback()
                return False, "Record not found."

        connection.commit()
        return True, f"Record in '{table_name}' updated successfully."

    except mysql.connector.Error as error:
        connection.rollback()
        return False, f"Update failed: {error}"

    finally:
        cursor.close()
        connection.close()


def delete_generic(table_name, primary_keys, key_values):
    """Delete a row using its primary key (supports composite keys)."""
    connection = connect_db()
    if connection is None:
        return False, "Could not connect to MySQL."

    cursor = connection.cursor()
    try:
        where_clause = " AND ".join(
            f"{quote_identifier(key)} = %s"
            for key in primary_keys
        )
        query = (
            f"DELETE FROM {quote_identifier(table_name)} "
            f"WHERE {where_clause}"
        )

        cursor.execute(
            query,
            tuple(normalize_sql_value(value) for value in key_values)
        )

        if cursor.rowcount == 0:
            connection.rollback()
            return False, "No matching record was deleted."

        connection.commit()
        return True, f"Record deleted successfully from '{table_name}'."

    except mysql.connector.Error as error:
        connection.rollback()
        return False, f"Delete failed: {error}"

    finally:
        cursor.close()
        connection.close()


def display_field_value(value):
    """Format existing database values for the generic text inputs."""
    if value is None:
        return ""

    if isinstance(value, pd.Timestamp):
        return value.isoformat(sep=" ")

    if isinstance(value, pd.Timedelta):
        return str(value)

    if hasattr(value, "isoformat"):
        return value.isoformat()

    if pd.isna(value):
        return ""

    return str(value)


def show_generic_field(column, current_value=None, key_prefix="field"):
    """Render one input for a database column."""
    field = column["Field"]
    extra = str(column.get("Extra", "")).lower()

    if "auto_increment" in extra or "generated" in extra:
        st.text_input(
            f"{field} (generated by MySQL)",
            value="Automatically generated",
            disabled=True,
            key=f"{key_prefix}_{field}_generated"
        )
        return OMIT_VALUE

    help_text = (
        f"MySQL type: {column['Type']} | "
        f"{'Nullable' if column.get('Null') == 'YES' else 'Required'}"
    )

    return st.text_input(
        field,
        value=display_field_value(current_value),
        help=help_text,
        key=f"{key_prefix}_{field}"
    )




# ============================================================
# MYSQL TABLE SELECTION
# ============================================================

mysql_tables = get_mysql_tables()

if not mysql_tables:
    st.error(
        "No tables were found in coffee_sales_db, or the database "
        "connection failed. Check MySQL Server and your database."
    )
    st.stop()

if "sales_transactions" not in mysql_tables:
    st.error(
        "The sales_transactions table is required for the existing "
        "sales analytics dashboard."
    )
    st.stop()

# This selector controls the generic CRUD section.
default_index = (
    mysql_tables.index("sales_transactions")
    if "sales_transactions" in mysql_tables
    else 0
)

crud_table = st.sidebar.selectbox(
    "Select table for CRUD",
    options=mysql_tables,
    index=default_index
)

st.sidebar.caption("Connected database: coffee_sales_db")

# Existing analytics and charts continue to use sales_transactions.
df = load_data("sales_transactions")

if df.empty:
    st.warning(
        "The sales_transactions table has no usable rows for analytics."
    )
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    '<div class="sidebar-brand">☕ Coffee Analytics</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="sidebar-tagline">Interactive Sales Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

st.sidebar.divider()

st.sidebar.subheader("Filters")


# DATE FILTER

min_date = df["transaction_date"].min().date()
max_date = df["transaction_date"].max().date()

date_range = st.sidebar.date_input(
    "Transaction Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:

    start_date = date_range[0]
    end_date = date_range[1]

else:

    start_date = min_date
    end_date = max_date


# CATEGORY FILTER

categories = sorted(
    df["product_category"]
    .dropna()
    .unique()
)

selected_categories = st.sidebar.multiselect(
    "Product Category",
    categories,
    default=categories
)


# PRODUCT TYPE FILTER

product_types = sorted(
    df["product_type"]
    .dropna()
    .unique()
)

selected_types = st.sidebar.multiselect(
    "Product Type",
    product_types,
    default=product_types
)


# STORE FILTER

stores = sorted(
    df["store_id"]
    .dropna()
    .unique()
)

selected_stores = st.sidebar.multiselect(
    "Store ID",
    stores,
    default=stores
)


# ============================================================
# FILTER DATA
# ============================================================

filtered = df[
    (df["transaction_date"].dt.date >= start_date)
    &
    (df["transaction_date"].dt.date <= end_date)
    &
    (df["product_category"].isin(selected_categories))
    &
    (df["product_type"].isin(selected_types))
    &
    (df["store_id"].isin(selected_stores))
].copy()


if filtered.empty:

    st.warning(
        "No data available for the selected filters."
    )

    st.stop()


# ============================================================
# HERO
# ============================================================

render_html(
    """
    <div class="hero">
        <div class="hero-title">Coffee Sales Intelligence Dashboard</div>
        <div class="hero-subtitle">
            A business analytics view of revenue, product performance and transaction
            behaviour across the selected stores and date range.
        </div>
    </div>
    """
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_records = len(filtered)

distinct_transactions = (
    filtered["transaction_id"].nunique()
)

total_units_sold = (
    filtered["transaction_qty"].sum()
)

total_sales = (
    filtered["sales_value"].sum()
)

average_transaction_value = (
    filtered["sales_value"].mean()
)

average_unit_price = (
    filtered["unit_price"].mean()
)


# ============================================================
# KPI SECTION
# ============================================================

render_html('<div class="section-title">Executive Performance</div>')

render_html(
    '<div class="section-description">'
    'Key performance indicators from the selected data'
    '</div>'
)

kpi_html = '<div class="kpi-grid">'
kpi_html += kpi_card("💰", "Total sales", f"₹{total_sales:,.2f}", GOLD)
kpi_html += kpi_card("🧾", "Distinct transactions", f"{distinct_transactions:,}", WINE)
kpi_html += kpi_card("📦", "Total units sold", f"{total_units_sold:,.0f}", WINE)
kpi_html += kpi_card("📈", "Average transaction value", f"₹{average_transaction_value:,.2f}", GOLD)
kpi_html += kpi_card("🏷️", "Average unit price", f"₹{average_unit_price:,.2f}", GOLD)
kpi_html += kpi_card("📊", "Total records", f"{total_records:,}", WINE)
kpi_html += '</div>'

render_html(kpi_html)

st.divider()


# ============================================================
# DATA PREPARATION
# ============================================================

category_summary = (
    filtered
    .groupby("product_category")
    .agg(
        units_sold=("transaction_qty", "sum"),
        total_sales=("sales_value", "sum"),
        transaction_records=("transaction_id", "count"),
        average_sale=("sales_value", "mean")
    )
    .reset_index()
    .sort_values(
        "total_sales",
        ascending=False
    )
)


product_summary = (
    filtered
    .groupby("product_type")
    .agg(
        units_sold=("transaction_qty", "sum"),
        total_sales=("sales_value", "sum"),
        average_price=("unit_price", "mean")
    )
    .reset_index()
    .sort_values(
        "total_sales",
        ascending=False
    )
)


top_products = (
    filtered
    .groupby("product_detail")
    .agg(
        units_sold=("transaction_qty", "sum"),
        total_sales=("sales_value", "sum")
    )
    .reset_index()
    .sort_values(
        "total_sales",
        ascending=False
    )
    .head(10)
)


daily_sales = (
    filtered
    .groupby("transaction_date")
    .agg(
        units_sold=("transaction_qty", "sum"),
        daily_sales=("sales_value", "sum")
    )
    .reset_index()
    .sort_values("transaction_date")
)


# ============================================================
# DASHBOARD TABS
# ============================================================

overview, products, sql_analysis, manage = st.tabs(
    [
        "Overview",
        "Product Analytics",
        "SQL Analysis",
        "Manage Records"
    ]
)


# ============================================================
# ============================================================
# MANAGE RECORDS — CRUD FOR ALL MYSQL TABLES
# ============================================================

with manage:

    render_html('<div class="section-title">Manage Records</div>')
    render_html(
        '<div class="section-description">'
        'Create, view, update and delete records in any table '
        'inside the connected MySQL database.'
        '</div>'
    )

    if "flash" in st.session_state:
        st.success(st.session_state.pop("flash"))

    st.subheader(f"Selected table: {crud_table}")

    schema_columns, primary_keys = get_table_schema(crud_table)
    table_df = read_table(crud_table)

    if not schema_columns:
        st.error("Could not retrieve the selected table's columns.")

    else:
        action = st.radio(
            "Operation",
            ["View", "Add", "Update", "Delete"],
            horizontal=True,
            key="generic_crud_action"
        )

        # ---------------- READ ----------------
        if action == "View":
            search_text = st.text_input(
                "Search records",
                placeholder="Search across all columns"
            )

            view_df = table_df.copy()

            if search_text and not view_df.empty:
                mask = view_df.astype(str).apply(
                    lambda column: column.str.contains(
                        search_text,
                        case=False,
                        na=False,
                        regex=False
                    )
                ).any(axis=1)
                view_df = view_df[mask]

            st.caption(f"Records found: {len(view_df):,}")
            st.dataframe(
                view_df,
                use_container_width=True,
                hide_index=True
            )

        # ---------------- CREATE ----------------
        elif action == "Add":
            st.write("Enter values for the new record.")

            with st.form(f"add_form_{crud_table}"):
                add_values = []

                for column in schema_columns:
                    value = show_generic_field(
                        column,
                        key_prefix=f"add_{crud_table}"
                    )
                    add_values.append(value)

                add_submit = st.form_submit_button(
                    "Add record",
                    type="primary"
                )

            if add_submit:
                try:
                    converted_values = [
                        convert_input(value, column)
                        for column, value in zip(
                            schema_columns, add_values
                        )
                    ]

                    success, message = insert_generic(
                        crud_table,
                        schema_columns,
                        converted_values
                    )

                    if success:
                        st.session_state["flash"] = message
                        st.rerun()
                    else:
                        st.error(message)

                except (ValueError, TypeError) as error:
                    st.error(str(error))

        # ---------------- UPDATE ----------------
        elif action == "Update":
            if not primary_keys:
                st.warning(
                    "This table has no primary key. "
                    "Update is disabled to avoid changing the wrong row."
                )

            elif table_df.empty:
                st.info("There are no records to update.")

            else:
                key_records = table_df[primary_keys].to_dict("records")

                key_labels = [
                    " | ".join(
                        f"{key}={display_field_value(record[key])}"
                        for key in primary_keys
                    )
                    for record in key_records
                ]

                selected_label = st.selectbox(
                    "Select record to update",
                    key_labels,
                    key=f"update_select_{crud_table}"
                )
                selected_index = key_labels.index(selected_label)
                original_row = table_df.iloc[selected_index]

                original_key_values = [
                    original_row[key] for key in primary_keys
                ]

                st.caption(
                    "Primary-key columns are protected and cannot be edited here."
                )

                with st.form(f"update_form_{crud_table}"):
                    update_values = []

                    for column in schema_columns:
                        field = column["Field"]

                        if field in primary_keys:
                            st.text_input(
                                f"{field} (PRIMARY KEY)",
                                value=display_field_value(original_row[field]),
                                disabled=True,
                                key=f"update_pk_{crud_table}_{field}"
                            )
                            update_values.append(OMIT_VALUE)
                        else:
                            value = show_generic_field(
                                column,
                                original_row[field],
                                key_prefix=f"update_{crud_table}"
                            )
                            update_values.append(value)

                    update_submit = st.form_submit_button(
                        "Save changes",
                        type="primary"
                    )

                if update_submit:
                    try:
                        converted_values = []

                        for column, value in zip(
                            schema_columns, update_values
                        ):
                            if value is OMIT_VALUE:
                                converted_values.append(OMIT_VALUE)
                            else:
                                converted_values.append(
                                    convert_input(value, column)
                                )

                        success, message = update_generic(
                            crud_table,
                            schema_columns,
                            primary_keys,
                            original_key_values,
                            converted_values
                        )

                        if success:
                            st.session_state["flash"] = message
                            st.rerun()
                        else:
                            st.error(message)

                    except (ValueError, TypeError) as error:
                        st.error(str(error))

        # ---------------- DELETE ----------------
        elif action == "Delete":
            if not primary_keys:
                st.warning(
                    "This table has no primary key. "
                    "Delete is disabled to avoid deleting the wrong row."
                )

            elif table_df.empty:
                st.info("There are no records to delete.")

            else:
                key_records = table_df[primary_keys].to_dict("records")

                key_labels = [
                    " | ".join(
                        f"{key}={display_field_value(record[key])}"
                        for key in primary_keys
                    )
                    for record in key_records
                ]

                selected_label = st.selectbox(
                    "Select record to delete",
                    key_labels,
                    key=f"delete_select_{crud_table}"
                )
                selected_index = key_labels.index(selected_label)
                selected_row = table_df.iloc[selected_index]

                key_values = [
                    selected_row[key] for key in primary_keys
                ]

                st.write("Selected record:")
                st.dataframe(
                    table_df.iloc[[selected_index]],
                    use_container_width=True,
                    hide_index=True
                )

                confirm = st.checkbox(
                    "I confirm that I want to permanently delete this record.",
                    key=f"confirm_delete_{crud_table}"
                )

                if st.button(
                    "Delete record",
                    type="primary",
                    disabled=not confirm,
                    key=f"delete_button_{crud_table}"
                ):
                    success, message = delete_generic(
                        crud_table,
                        primary_keys,
                        key_values
                    )

                    if success:
                        st.session_state["flash"] = message
                        st.rerun()
                    else:
                        st.error(message)




# OVERVIEW
# ============================================================

with overview:

    render_html('<div class="section-title">Revenue Performance</div>')

    render_html(
        '<div class="section-description">'
        'Daily sales trend and category contribution'
        '</div>'
    )


    col1, col2 = st.columns(
        [1.6, 1]
    )


    # --------------------------------------------------------
    # DAILY SALES
    # --------------------------------------------------------

    with col1:

        fig = px.line(
            daily_sales,
            x="transaction_date",
            y="daily_sales",
            markers=True,
            title="Daily Sales Trend"
        )

        fig.update_traces(
            line=dict(
                width=3,
                color=GOLD
            ),
            marker=dict(
                size=5,
                color=GOLD
            ),
            fill="tozeroy",
            fillcolor="rgba(217,164,65,0.12)"
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Sales (₹)",
            hovermode="x unified"
        )

        fig = style_fig(fig)

        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False}
        )


    # --------------------------------------------------------
    # CATEGORY DONUT
    # --------------------------------------------------------

    with col2:

        fig = px.pie(
            category_summary,
            names="product_category",
            values="total_sales",
            hole=0.55,
            title="Sales by Category",
            color_discrete_sequence=CHART_COLORS
        )

        fig.update_traces(
            textinfo="percent+label",
            textfont=dict(family="Inter, sans-serif", size=11)
        )

        fig = style_fig(fig)

        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False}
        )


    # --------------------------------------------------------
    # CATEGORY PERFORMANCE
    # --------------------------------------------------------

    render_html('<div class="section-title">Category Performance</div>')

    fig = px.bar(
        category_summary.sort_values(
            "total_sales"
        ),
        x="total_sales",
        y="product_category",
        orientation="h",
        text_auto=".2s",
        title="Total Sales by Product Category",
        color="total_sales",
        color_continuous_scale=ROAST_SCALE
    )

    fig.update_layout(
        xaxis_title="Sales (₹)",
        yaxis_title="",
        coloraxis_showscale=False
    )

    fig.update_traces(
        textfont=dict(family="Inter, sans-serif", color="#241A11")
    )

    fig = style_fig(fig, height=450)

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False}
    )


    # --------------------------------------------------------
    # CATEGORY TABLE
    # --------------------------------------------------------

    render_html('<div class="section-title">Category Summary</div>')

    category_display = category_summary.copy()

    category_display["sales_percentage"] = (
        category_display["total_sales"]
        /
        total_sales
        *
        100
    )

    st.dataframe(
        category_display.style.format({
            "total_sales": "₹{:,.2f}",
            "average_sale": "₹{:,.2f}",
            "sales_percentage": "{:.2f}%"
        }),
        width="stretch",
        hide_index=True
    )


# ============================================================
# PRODUCT ANALYTICS
# ============================================================

with products:

    render_html('<div class="section-title">Product Analytics</div>')

    render_html(
        '<div class="section-description">'
        'Top-performing products and product types'
        '</div>'
    )


    col1, col2 = st.columns(
        [1.5, 1]
    )


    # TOP PRODUCTS

    with col1:

        fig = px.bar(
            top_products.sort_values(
                "total_sales"
            ),
            x="total_sales",
            y="product_detail",
            orientation="h",
            text_auto=".2s",
            title="Top 10 Products by Sales",
            color="total_sales",
            color_continuous_scale=ROAST_SCALE
        )

        fig.update_layout(
            xaxis_title="Sales (₹)",
            yaxis_title="",
            coloraxis_showscale=False
        )

        fig.update_traces(
            textfont=dict(family="Inter, sans-serif", color="#241A11")
        )

        fig = style_fig(fig, height=500)

        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False}
        )


    # PRODUCT TYPES

    with col2:

        fig = px.bar(
            product_summary.head(10).sort_values(
                "total_sales"
            ),
            x="total_sales",
            y="product_type",
            orientation="h",
            text_auto=".2s",
            title="Top Product Types",
            color="total_sales",
            color_continuous_scale=ROAST_SCALE
        )

        fig.update_layout(
            xaxis_title="Sales (₹)",
            yaxis_title="",
            coloraxis_showscale=False
        )

        fig.update_traces(
            textfont=dict(family="Inter, sans-serif", color="#241A11")
        )

        fig = style_fig(fig, height=500)

        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False}
        )


    # PRODUCT TABLE

    render_html('<div class="section-title">Product Type Details</div>')

    st.dataframe(
        product_summary.style.format({
            "total_sales": "₹{:,.2f}",
            "average_price": "₹{:,.2f}"
        }),
        width="stretch",
        hide_index=True
    )


# ============================================================
# SQL ANALYSIS
# ============================================================

with sql_analysis:

    render_html('<div class="section-title">SQL-Based Analysis</div>')

    render_html(
        '<div class="section-description">'
        'Interactive versions of the SQL queries from your project'
        '</div>'
    )


    # --------------------------------------------------------
    # HIGH VALUE SALES
    # --------------------------------------------------------

    high_value = (
        filtered[
            filtered["sales_value"] > 1000
        ]
        [
            [
                "transaction_id",
                "transaction_date",
                "product_category",
                "product_type",
                "product_detail",
                "sales_value"
            ]
        ]
        .sort_values(
            "sales_value",
            ascending=False
        )
    )


    render_html(
        '<div class="section-title">'
        'High-Value Transactions'
        '</div>'
    )

    st.caption(
        "Transactions where sales_value > ₹1,000"
    )

    st.dataframe(
        high_value.style.format({
            "sales_value": "₹{:,.2f}"
        }),
        width="stretch",
        hide_index=True
    )


    # --------------------------------------------------------
    # ABOVE ₹10,000
    # --------------------------------------------------------

    above_10k = product_summary[
        product_summary["total_sales"] > 10000
    ]


    render_html(
        '<div class="section-title">'
        'Product Types Above ₹10,000'
        '</div>'
    )

    st.caption(
        "Product types with total sales above ₹10,000"
    )

    st.dataframe(
        above_10k.style.format({
            "total_sales": "₹{:,.2f}",
            "average_price": "₹{:,.2f}"
        }),
        width="stretch",
        hide_index=True
    )


    # --------------------------------------------------------
    # ABOVE AVERAGE
    # --------------------------------------------------------

    above_average = (
        filtered[
            filtered["sales_value"]
            >
            average_transaction_value
        ]
        [
            [
                "transaction_id",
                "transaction_date",
                "product_detail",
                "sales_value"
            ]
        ]
        .sort_values(
            "sales_value",
            ascending=False
        )
    )


    render_html(
        '<div class="section-title">'
        'Above-Average Transactions'
        '</div>'
    )

    st.caption(
        f"Transactions above average value "
        f"₹{average_transaction_value:,.2f}"
    )

    st.dataframe(
        above_average.style.format({
            "sales_value": "₹{:,.2f}"
        }),
        width="stretch",
        hide_index=True
    )


# ============================================================
# DOWNLOAD
# ============================================================

st.divider()

render_html('<div class="section-title">Export Data</div>')

st.download_button(
    "Download Filtered Dataset",
    data=filtered.to_csv(
        index=False
    ).encode("utf-8"),
    file_name="coffee_sales_filtered.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

render_html(
    '<div class="footer-note">Coffee Sales Intelligence Dashboard — built with Python, Pandas, '
    'Plotly and Streamlit</div>'
)


