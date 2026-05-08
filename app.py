
import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Ditto Influencer Dashboard",
    layout="wide"
)

st.title("Ditto Insurance — Influencer Operating Dashboard")
st.markdown("Founder’s Office | Influencer Growth Engine")

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_data():

    df = pd.read_excel("Influencer_Campaigns.xlsx")
    st.write(df.columns)
    # VIEW COLUMN NAMES
    st.write("Dataset Columns:", df.columns.tolist())

    # CLEAN COLUMN NAMES
    df.columns = [col.strip().replace(" ", "_") for col in df.columns]

    # -----------------------------
    # IMPORTANT:
    # UPDATE THESE COLUMN NAMES
    # IF YOUR EXCEL DIFFERS
    # -----------------------------

    # Example expected columns:
    # Influencer
    # Campaign_ID
    # Start_Date
    # Content_Type
    # Product
    # Cost
    # Leads
    # Quality_Lead_Pct
    # Conversions
    # Premiums
    # ROI

    # CREATE CAC
    df["CAC"] = df["Cost"] / df["Conversions"]

    # HANDLE DIVIDE BY ZERO
    df["CAC"] = df["CAC"].replace([float("inf")], 0)

    return df


df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------

st.sidebar.header("Filters")

product_filter = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

content_filter = st.sidebar.multiselect(
    "Select Content Type",
    options=df["Content_Type"].unique(),
    default=df["Content_Type"].unique()
)

filtered_df = df[
    (df["Product"].isin(product_filter)) &
    (df["Content_Type"].isin(content_filter))
]

# -----------------------------
# KPI SECTION
# -----------------------------

st.subheader("Portfolio Performance")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Spend",
        f"₹{filtered_df['Cost'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Total Premiums",
        f"₹{filtered_df['Premiums'].sum():,.0f}"
    )

with col3:
    portfolio_roi = (
        (filtered_df['Premiums'].sum() - filtered_df['Cost'].sum())
        / filtered_df['Cost'].sum()
    )

    st.metric(
        "Portfolio ROI",
        f"{portfolio_roi:.2f}x"
    )

with col4:
    st.metric(
        "Conversions",
        int(filtered_df['Conversions'].sum())
    )

with col5:
    overall_cac = (
        filtered_df['Cost'].sum()
        / filtered_df['Conversions'].sum()
    )

    st.metric(
        "CAC",
        f"₹{overall_cac:,.0f}"
    )

# -----------------------------
# PRODUCT PERFORMANCE
# -----------------------------

st.subheader("Product Performance")

product_summary = filtered_df.groupby("Product").agg({
    "Cost": "sum",
    "Premiums": "sum",
    "Conversions": "sum"
}).reset_index()

product_summary["ROI"] = (
    (product_summary["Premiums"] - product_summary["Cost"])
    / product_summary["Cost"]
)

product_summary["CAC"] = (
    product_summary["Cost"]
    / product_summary["Conversions"]
)

st.dataframe(product_summary)

fig_product = px.bar(
    product_summary,
    x="Product",
    y="ROI",
    title="ROI by Product"
)

st.plotly_chart(fig_product, use_container_width=True)

# -----------------------------
# TOP INFLUENCERS
# -----------------------------

st.subheader("Top Performing Influencers")

influencer_summary = filtered_df.groupby("Influencer").agg({
    "Cost": "sum",
    "Premiums": "sum",
    "Conversions": "sum"
}).reset_index()

influencer_summary["ROI"] = (
    (influencer_summary["Premiums"] - influencer_summary["Cost"])
    / influencer_summary["Cost"]
)

influencer_summary = influencer_summary.sort_values(
    by="ROI",
    ascending=False
)

st.dataframe(influencer_summary.head(10))

fig_top = px.bar(
    influencer_summary.head(10),
    x="Influencer",
    y="ROI",
    title="Top 10 Influencers by ROI"
)

st.plotly_chart(fig_top, use_container_width=True)

# -----------------------------
# LOWEST PERFORMERS
# -----------------------------

st.subheader("Lowest Performing Influencers")

st.dataframe(influencer_summary.tail(10))

# -----------------------------
# CONTENT TYPE PERFORMANCE
# -----------------------------

st.subheader("Content Type Performance")

content_summary = filtered_df.groupby("Content_Type").agg({
    "Cost": "sum",
    "Premiums": "sum"
}).reset_index()

content_summary["ROI"] = (
    (content_summary["Premiums"] - content_summary["Cost"])
    / content_summary["Cost"]
)

fig_content = px.bar(
    content_summary,
    x="Content_Type",
    y="ROI",
    title="ROI by Content Type"
)

st.plotly_chart(fig_content, use_container_width=True)

# -----------------------------
# COST VS PREMIUMS
# -----------------------------

st.subheader("Cost vs Premium Analysis")

fig_scatter = px.scatter(
    filtered_df,
    x="Cost",
    y="Premiums",
    size="Conversions",
    color="Product",
    hover_name="Influencer",
    title="Campaign Cost vs Premiums"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# REPEAT CREATOR ANALYSIS
# -----------------------------

st.subheader("Repeat Creator Analysis")

repeat_creators = filtered_df.groupby(
    "Influencer"
).size().reset_index(name="Campaign_Count")

fig_repeat = px.histogram(
    repeat_creators,
    x="Campaign_Count",
    title="Repeat Campaign Distribution"
)

st.plotly_chart(fig_repeat, use_container_width=True)

# -----------------------------
# OPERATOR INSIGHTS
# -----------------------------

st.subheader("Founder’s Office Insights")

st.markdown("""
### Key Operational Insights

- Repeat creators outperform one-off creators significantly.
- 'Both (Health & Term)' campaigns generate the strongest ROI.
- High spend does not guarantee high premium generation.
- Mid-sized trust-based creators outperform vanity creators.
- Attribution discipline is critical before scaling budget.
""")

