
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
    
    # VIEW COLUMN NAMES
    

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
    # Cost_(INR)
    # Leads
    # Quality_Lead_Pct
    # Total_converts
    # Total_Sales_Premiums_(INR)
    # ROI

    # CREATE CAC
    # df["CAC"] = df["Cost_(INR)"] / df["Total_converts"]

    # HANDLE DIVIDE BY ZERO
    # df["CAC"] = df["CAC"].replace([float("inf")], 0)

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
    options=df["Content_type"].unique(),
    default=df["Content_type"].unique()
)

filtered_df = df[
    (df["Product"].isin(product_filter)) &
    (df["Content_type"].isin(content_filter))
]

# -----------------------------
# KPI SECTION
# -----------------------------

st.subheader("Portfolio Performance")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Spend",
        f"₹{filtered_df['Cost_(INR)'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Total_Sales_Premiums_(INR)",
        f"₹{filtered_df['Total_Sales_Premiums_(INR)'].sum():,.0f}"
    )

with col3:
    portfolio_roi = (
        (filtered_df['Total_Sales_Premiums_(INR)'].sum() - filtered_df['Cost_(INR)'].sum())
       # / filtered_df['Cost_(INR)'].sum()
    )

    st.metric(
        "Portfolio ROI",
        f"{portfolio_roi:.2f}x"
    )

with col4:
    st.metric(
        "Total_converts",
        int(filtered_df['Total_converts'].sum())
    )

with col5:
    overall_cac = (
        filtered_df['Cost_(INR)'].sum()
        / filtered_df['Total_converts'].sum()
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
"Cost_(INR)": "sum",
    "Total_Sales_Premiums_(INR)": "sum",
    "Total_converts": "sum"
}).reset_index()

product_summary["ROI"] = (
    (product_summary["Total_Sales_Premiums_(INR)"] - product_summary["Cost_(INR)"])
    / product_summary["Cost_(INR)"]
)

product_summary["CAC"] = (
    product_summary["Cost_(INR)"]
    / product_summary["Total_converts"]
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

influencer_summary = filtered_df.groupby("Influencer_name").agg({
 "Cost_(INR)": "sum",
    "Total_Sales_Premiums_(INR)": "sum",
    "Total_converts": "sum"
}).reset_index()

influencer_summary["ROI"] = (
    (influencer_summary["Total_Sales_Premiums_(INR)"] - influencer_summary["Cost_(INR)"])
    / influencer_summary["Cost_(INR)"]
)

influencer_summary = influencer_summary.sort_values(
    by="ROI",
    ascending=False
)

st.dataframe(influencer_summary.head(10))

fig_top = px.bar(
    influencer_summary.head(10),
    x="Influencer_name",
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
"Cost_(INR)": "sum",
    "Total_Sales_Premiums_(INR)": "sum"
}).reset_index()

content_summary["ROI"] = (
    (content_summary["Total_Sales_Premiums_(INR)"] - content_summary["Cost_(INR)"])
    / content_summary["Cost_(INR)"]
)

fig_content = px.bar(
    content_summary,
    x="Content_Type",
    y="ROI",
    title="ROI by Content Type"
)

st.plotly_chart(fig_content, use_container_width=True)

# -----------------------------
# Cost_(INR) VS Total_Sales_Premiums_(INR)
# -----------------------------

st.subheader("Cost_(INR) vs Premium Analysis")

fig_scatter = px.scatter(
    filtered_df,
x="Cost_(INR)",
    y="Total_Sales_Premiums_(INR)",
    size="Total_converts",
    color="Product",
    hover_name="Influencer_name",
    title="Campaign Cost_(INR) vs Total_Sales_Premiums_(INR)"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# REPEAT CREATOR ANALYSIS
# -----------------------------

st.subheader("Repeat Creator Analysis")

repeat_creators = filtered_df.groupby(
    "Influencer_name"
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

