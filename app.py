import pandas as pd
import streamlit as st
import plotly.express as px

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
# SIDEBAR FILTERS
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

selected_creator = st.sidebar.selectbox(
    "Creator Drilldown",
    options=sorted(df["Influencer_name"].unique())
)

# ======================================================
# FILTER DATA
# ======================================================

filtered_df = df[
    (df["Product"].isin(product_filter)) &
    (df["Content_type"].isin(content_filter)) &
    (df["Calculated_ROI"] >= roi_filter)
]

creator_df = df[
    df["Influencer_name"] == selected_creator
]

# ======================================================
# HEADER
# ======================================================

st.title("Ditto Insurance — Influencer Operating System")

st.caption(
    "Founder’s Office | Growth & Portfolio Intelligence"
)

st.caption(
    "Last Updated: 10-May-2026"
)

# ======================================================
# KPI SECTION
# ======================================================

total_spend = filtered_df["Cost_(INR)"].sum()

total_premium = filtered_df[
    "Total_Sales_Premiums_(INR)"
].sum()

portfolio_roi = (
    (total_premium - total_spend)
    / total_spend
)

negative_roi_pct = (
    len(df[df["Calculated_ROI"] < 0])
    / len(df)
) * 100

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Spend",
    f"₹{total_spend/10000000:.2f} Cr"
)

col2.metric(
    "Premiums Generated",
    f"₹{total_premium/10000000:.2f} Cr"
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

• Portfolio ROI remains concentrated among repeat creators with trust-led audiences.

• LinkedIn and bundled insurance campaigns continue to materially outperform blended portfolio averages.
""")

st.divider()

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

content_summary["ROI"] = (
    content_summary["ROI"].round(2)
)

fig_content = px.bar(
    content_summary,
    x="Content_type",
    y="ROI",
    text="ROI",
    hover_data=[
        "Cost_(INR)",
        "Total_Sales_Premiums_(INR)"
    ]
)

st.plotly_chart(
    fig_content,
    use_container_width=True
)

st.divider()

# ======================================================
# PRODUCT PERFORMANCE
# ======================================================

st.subheader("Product Portfolio Performance")

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

product_summary["ROI"] = (
    product_summary["ROI"].round(2)
)

st.dataframe(
    product_summary,
    use_container_width=True
)

st.divider()

# ======================================================
# CREATOR PORTFOLIO REVIEW
# ======================================================

st.subheader("Creator Portfolio Review")

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

creator_summary["ROI"] = (
    creator_summary["ROI"].round(2)
)

creator_summary["Recommendation"] = (
    creator_summary["ROI"]
    .apply(
        lambda x:
        "SCALE" if x >= 3 else
        "CUT" if x < 1 else
        "HOLD / TEST"
    )
)

creator_summary = creator_summary.sort_values(
    by="ROI",
    ascending=False
)

with st.expander("View Full Creator Performance Table"):

    st.dataframe(
        creator_summary,
        use_container_width=True
    )

st.divider()

# ======================================================
# TOP & LOW PERFORMERS
# ======================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Top Performing Creators")

    top_5 = creator_summary.head(5)

    fig_top = px.bar(
        top_5,
        x="Influencer_name",
        y="ROI",
        color="Recommendation",
        text="ROI"
    )

    st.plotly_chart(
        fig_top,
        use_container_width=True
    )

with col2:

    st.subheader("Underperforming Creators")

    low_5 = creator_summary[
        creator_summary["Recommendation"] == "CUT"
    ].head(5)

    fig_low = px.bar(
        low_5,
        x="Influencer_name",
        y="ROI",
        color="Recommendation",
        text="ROI"
    )

    st.plotly_chart(
        fig_low,
        use_container_width=True
    )

st.divider()

# ======================================================
# CREATOR DRILLDOWN
# ======================================================

st.subheader("Creator Drilldown")

creator_spend = creator_df["Cost_(INR)"].sum()

creator_premium = creator_df[
    "Total_Sales_Premiums_(INR)"
].sum()

creator_roi = (
    (creator_premium - creator_spend)
    / creator_spend
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Creator Spend",
    f"₹{creator_spend:,.0f}"
)

c2.metric(
    "Premiums Generated",
    f"₹{creator_premium:,.0f}"
)

c3.metric(
    "Creator ROI",
    f"{creator_roi:.2f}x"
)

st.dataframe(
    creator_df,
    use_container_width=True
)

st.divider()

# ======================================================
# CAMPAIGN ANALYSIS
# ======================================================

st.subheader("Campaign Cost vs Premium Analysis")

fig_scatter = px.scatter(
    filtered_df,
    x="Cost_(INR)",
    y="Total_Sales_Premiums_(INR)",
    size="Total_converts",
    color="Product",
    hover_name="Influencer_name",
    hover_data=[
        "Calculated_ROI",
        "Content_type"
    ]
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

st.divider()

# ======================================================
# REPEAT CREATOR ANALYSIS
# ======================================================

st.subheader(
    "Creator Retention & Repeat Activation Trends"
)

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

st.plotly_chart(
    fig_repeat,
    use_container_width=True
)

st.divider()

# ======================================================
# FOUNDER ACTION PANEL
# ======================================================

st.warning("""
### Immediate Leadership Decisions Needed

• Reduce dedicated YouTube allocation by 25% next cycle.

• Increase LinkedIn creator partnerships for bundled insurance campaigns.

• Re-negotiate pricing with underperforming repeat creators.

• Tighten follow-up SLA enforcement before scaling outreach volume.
""")

# ======================================================
# RECOMMENDED ACTIONS
# ======================================================

st.subheader("Recommended Actions")

scale_creators = creator_summary[
    creator_summary["Recommendation"] == "SCALE"
]["Influencer_name"].head(5).tolist()

cut_creators = creator_summary[
    creator_summary["Recommendation"] == "CUT"
]["Influencer_name"].head(5).tolist()

st.success(f"""
### Scale Budget Allocation

Recommended creators for higher budget allocation:

{', '.join(scale_creators)}

Primary rationale:
Strong blended ROI, repeat campaign consistency, and superior premium generation efficiency.
""")

st.error(f"""
### Review / Pause Spend

Creators requiring budget review or pause:

{', '.join(cut_creators)}

Primary rationale:
Weak ROI efficiency, inconsistent conversions, or elevated CAC.
""")

st.divider()

# ======================================================
# FOUNDER’S OFFICE NOTES
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
