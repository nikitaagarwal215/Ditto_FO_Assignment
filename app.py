import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Ditto Influencer Operating System",
    page_icon="📈",
    layout="wide"
)

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():

    df = pd.read_excel("Influencer_Campaigns.xlsx")

    df.columns = [c.strip().replace(" ", "_") for c in df.columns]

    # ROI
    df["Calculated_ROI"] = (
        (df["Total_Sales_Premiums_(INR)"] - df["Cost_(INR)"])
        / df["Cost_(INR)"]
    )

    # CAC
    df["CAC"] = (
        df["Cost_(INR)"]
        / df["Total_converts"]
    )

    # Conversion Rate
    df["Conversion_Rate"] = (
        df["Total_converts"]
        / df["Leads"]
    )

    return df

df = load_data()

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("Dashboard Filters")

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

roi_filter = st.sidebar.slider(
    "Minimum ROI",
    min_value=float(df["Calculated_ROI"].min()),
    max_value=float(df["Calculated_ROI"].max()),
    value=float(df["Calculated_ROI"].min())
)

filtered_df = df[
    (df["Product"].isin(product_filter)) &
    (df["Content_type"].isin(content_filter)) &
    (df["Calculated_ROI"] >= roi_filter)
]

# ======================================================
# HEADER
# ======================================================

st.title("Ditto Insurance — Influencer Operating System")
st.caption("Founder’s Office | Growth & Portfolio Intelligence")

# ======================================================
# KPI SECTION
# ======================================================

total_spend = filtered_df["Cost_(INR)"].sum()
total_premium = filtered_df["Total_Sales_Premiums_(INR)"].sum()

portfolio_roi = (
    (total_premium - total_spend)
    / total_spend
)

negative_roi_pct = (
    len(filtered_df[filtered_df["Calculated_ROI"] < 0])
    / len(filtered_df)
) * 100

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Spend",
    f"₹{total_spend:,.0f}"
)

col2.metric(
    "Premiums Generated",
    f"₹{total_premium:,.0f}"
)

col3.metric(
    "Portfolio ROI",
    f"{portfolio_roi:.2f}x"
)

col4.metric(
    "Conversions",
    int(filtered_df["Total_converts"].sum())
)

col5.metric(
    "Negative ROI %",
    f"{negative_roi_pct:.1f}%"
)

st.divider()

# ======================================================
# EXECUTIVE INSIGHTS
# ======================================================

st.subheader("Executive Insights")

best_format = (
    filtered_df
    .groupby("Content_type")["Calculated_ROI"]
    .mean()
    .idxmax()
)

worst_format = (
    filtered_df
    .groupby("Content_type")["Calculated_ROI"]
    .mean()
    .idxmin()
)

best_product = (
    filtered_df
    .groupby("Product")["Calculated_ROI"]
    .mean()
    .idxmax()
)

st.info(f"""
• Best Performing Format: {best_format}

• Weakest Performing Format: {worst_format}

• Highest ROI Product Category: {best_product}

• Portfolio ROI is concentrated among a small set of repeat creators.

• LinkedIn and trust-based creators materially outperform vanity creator formats.
""")

# ======================================================
# ROI BY CONTENT FORMAT
# ======================================================

st.subheader("ROI by Content Format")

content_summary = (
    filtered_df
    .groupby("Content_type")
    .agg({
        "Cost_(INR)": "sum",
        "Total_Sales_Premiums_(INR)": "sum"
    })
    .reset_index()
)

content_summary["ROI"] = (
    (content_summary["Total_Sales_Premiums_(INR)"] -
     content_summary["Cost_(INR)"])
    / content_summary["Cost_(INR)"]
)

fig_content = px.bar(
    content_summary,
    x="Content_type",
    y="ROI",
    text_auto=True
)

st.plotly_chart(fig_content, use_container_width=True)

# ======================================================
# PRODUCT PERFORMANCE
# ======================================================

st.subheader("Product Performance")

product_summary = (
    filtered_df
    .groupby("Product")
    .agg({
        "Cost_(INR)": "sum",
        "Total_Sales_Premiums_(INR)": "sum",
        "Total_converts": "sum"
    })
    .reset_index()
)

product_summary["ROI"] = (
    (product_summary["Total_Sales_Premiums_(INR)"] -
     product_summary["Cost_(INR)"])
    / product_summary["Cost_(INR)"]
)

st.dataframe(product_summary, use_container_width=True)

# ======================================================
# CREATOR INTELLIGENCE
# ======================================================

st.subheader("Creator Intelligence")

creator_summary = (
    filtered_df
    .groupby("Influencer_name")
    .agg({
        "Cost_(INR)": "sum",
        "Total_Sales_Premiums_(INR)": "sum",
        "Total_converts": "sum",
        "Campaign_ID": "count"
    })
    .reset_index()
)

creator_summary["ROI"] = (
    (creator_summary["Total_Sales_Premiums_(INR)"] -
     creator_summary["Cost_(INR)"])
    / creator_summary["Cost_(INR)"]
)

creator_summary["Recommendation"] = creator_summary["ROI"].apply(
    lambda x:
    "SCALE" if x >= 3 else
    "CUT" if x < 1 else
    "HOLD / TEST"
)

creator_summary = creator_summary.sort_values(
    by="ROI",
    ascending=False
)

st.dataframe(
    creator_summary,
    use_container_width=True
)

# ======================================================
# TOP & LOW PERFORMERS
# ======================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Top Creators")

    top_5 = creator_summary.head(5)

    fig_top = px.bar(
        top_5,
        x="Influencer_name",
        y="ROI",
        color="Recommendation",
        text_auto=True
    )

    st.plotly_chart(fig_top, use_container_width=True)

with col2:

    st.subheader("Underperforming Creators")

    low_5 = creator_summary.tail(5)

    fig_low = px.bar(
        low_5,
        x="Influencer_name",
        y="ROI",
        color="Recommendation",
        text_auto=True
    )

    st.plotly_chart(fig_low, use_container_width=True)

# ======================================================
# CAMPAIGN SCATTER
# ======================================================

st.subheader("Campaign Cost vs Premium Analysis")

fig_scatter = px.scatter(
    filtered_df,
    x="Cost_(INR)",
    y="Total_Sales_Premiums_(INR)",
    size="Total_converts",
    color="Product",
    hover_name="Influencer_name"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# ======================================================
# REPEAT CREATOR ANALYSIS
# ======================================================

st.subheader("Repeat Creator Analysis")

repeat_creators = (
    filtered_df
    .groupby("Influencer_name")
    .size()
    .reset_index(name="Campaign_Count")
)

fig_repeat = px.histogram(
    repeat_creators,
    x="Campaign_Count"
)

st.plotly_chart(fig_repeat, use_container_width=True)

# ======================================================
# WEEKLY DECISION ENGINE
# ======================================================

st.subheader("Recommended Actions")

scale_creators = creator_summary[
    creator_summary["Recommendation"] == "SCALE"
]["Influencer_name"].head(5).tolist()

cut_creators = creator_summary[
    creator_summary["Recommendation"] == "CUT"
]["Influencer_name"].head(5).tolist()

st.success(f"""
Scale Budget Allocation:
{', '.join(scale_creators)}
""")

st.error(f"""
Review / Pause Spend:
{', '.join(cut_creators)}
""")

# ======================================================
# OPERATOR NOTES
# ======================================================

st.subheader("Founder’s Office Notes")

st.markdown("""
### Key Strategic Learnings

• LinkedIn creators continue to deliver the strongest blended ROI.

• Bundled Health + Term positioning materially outperforms standalone Term campaigns.

• Dedicated YouTube should be treated selectively as strategic awareness inventory rather than default acquisition spend.

• Portfolio performance is heavily concentrated among repeat creators, making creator relationship management a critical operational capability.

• Attribution consistency and follow-up discipline remain the biggest operational bottlenecks before scaling budget aggressively.
""")
