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
# DITTO STYLE THEME
# ======================================================

st.markdown("""
<style>

.stApp {
    background-color: #FFFFFF;
    color: #1E293B;
}

section[data-testid="stSidebar"] {
    background-color: #F8FAFC;
}

h1, h2, h3 {
    color: #1E293B !important;
}

[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
}

.stButton>button {
    background-color: #FF6B6B;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #F45B5B;
    color: white;
}

</style>
""", unsafe_allow_html=True)

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

st.sidebar.title("Ditto Operating System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "CRM Pipeline",
        "Campaign Operations",
        "Creator Intelligence",
        "Founder Decision Center"
    ]
)

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

selected_creator = st.sidebar.selectbox(
    "Creator Drilldown",
    options=sorted(df["Influencer_name"].unique())
)

# ======================================================
# FILTER DATA
# ======================================================

filtered_df = df[
    (df["Product"].isin(product_filter)) &
    (df["Content_type"].isin(content_filter))
]

creator_df = df[
    df["Influencer_name"] == selected_creator
]

# ======================================================
# HEADER
# ======================================================

st.title("Ditto Insurance — Influencer Operating System")

st.caption("Founder’s Office | Growth & Portfolio Intelligence")

st.markdown("""
<div style='padding:16px;
background-color:#FFF1F2;
border-radius:12px;
margin-bottom:20px;'>

<b>Objective:</b> Build a lightweight influencer operating system that improves attribution visibility, workflow accountability, campaign execution, and portfolio-level decision making while reducing founder dependency.

</div>
""", unsafe_allow_html=True)

# ======================================================
# EXECUTIVE DASHBOARD
# ======================================================

if page == "Executive Dashboard":

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
        text_auto=True,
        color_discrete_sequence=["#FF6B6B"]
    )

    st.plotly_chart(fig_content, use_container_width=True)

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

    st.dataframe(product_summary, use_container_width=True)

    st.divider()

    # ======================================================
    # RISK ALERTS
    # ======================================================

    st.subheader("Portfolio Risk Alerts")

    st.error("""
    • Dedicated YouTube campaigns continue underperforming blended portfolio ROI.

    • Portfolio ROI remains concentrated among repeat creators.

    • Standalone Term campaigns continue showing weaker conversion efficiency.
    """)

# ======================================================
# CRM PIPELINE
# ======================================================

elif page == "CRM Pipeline":

    st.subheader("CRM Pipeline Management")

    crm_df = pd.DataFrame({
        "Influencer": [
            "AdityaGuidePune",
            "MeeraFitChennai",
            "OmStudioIndia"
        ],
        "Stage": [
            "Negotiation",
            "Live",
            "Escalation"
        ],
        "Owner": [
            "Riya",
            "Aman",
            "Karan"
        ],
        "Next Follow Up": [
            "2026-05-12",
            "2026-05-14",
            "2026-05-10"
        ],
        "Status": [
            "Awaiting revised pricing",
            "Campaign live",
            "Weak ROI performance"
        ]
    })

    edited_df = st.data_editor(
        crm_df,
        num_rows="dynamic",
        use_container_width=True
    )

    st.divider()

    st.warning("""
    SLA Alerts

    • 4 creators pending follow-up beyond 7 days.

    • 2 campaigns awaiting creative approval.

    • 1 creator has duplicate outreach risk.
    """)

# ======================================================
# CAMPAIGN OPERATIONS
# ======================================================

elif page == "Campaign Operations":

    st.subheader("Campaign Operations")

    st.dataframe(filtered_df, use_container_width=True)

    fig_scatter = px.scatter(
        filtered_df,
        x="Cost_(INR)",
        y="Total_Sales_Premiums_(INR)",
        size="Total_converts",
        color="Product",
        hover_name="Influencer_name",
        color_discrete_sequence=[
            "#FF6B6B",
            "#1D4ED8",
            "#16A34A"
        ]
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

# ======================================================
# CREATOR INTELLIGENCE
# ======================================================

elif page == "Creator Intelligence":

    st.subheader("Creator Performance Intelligence")

    creator_summary = (
        filtered_df
        .groupby("Influencer_name")
        .agg({
            "Cost_(INR)": "sum",
            "Total_Sales_Premiums_(INR)": "sum",
            "Campaign_ID": "count"
        })
        .reset_index()
    )

    creator_summary["ROI"] = (
        (creator_summary["Total_Sales_Premiums_(INR)"] -
         creator_summary["Cost_(INR)"])
        / creator_summary["Cost_(INR)"]
    )

    creator_summary["Recommendation"] = creator_summary[
        "ROI"
    ].apply(
        lambda x:
        "SCALE" if x >= 3 else
        "CUT" if x < 1 else
        "HOLD / TEST"
    )

    st.dataframe(
        creator_summary,
        use_container_width=True
    )

    st.divider()

    st.subheader("Creator Drilldown")

    st.dataframe(
        creator_df,
        use_container_width=True
    )

# ======================================================
# FOUNDER DECISION CENTER
# ======================================================

elif page == "Founder Decision Center":

    st.subheader("Founder Decision Center")

    st.warning("""
    Immediate Leadership Decisions Needed

    • Reduce Dedicated YouTube allocation by 25%

    • Increase LinkedIn creator partnerships

    • Tighten attribution discipline

    • Scale bundled Health + Term creators
    """)

    st.divider()

    # ======================================================
    # BUDGET SIMULATOR
    # ======================================================

    st.subheader("Budget Reallocation Simulator")

    budget_shift = st.slider(
        "Increase Top Creator Budget (%)",
        0,
        50,
        20
    )

    projected_roi = 3.2 + (budget_shift * 0.03)

    st.metric(
        "Projected ROI",
        f"{projected_roi:.2f}x"
    )

    st.divider()

    # ======================================================
    # RECOMMENDATION ENGINE
    # ======================================================

    if st.button("Generate Founder Recommendations"):

        st.success("""
        Recommended Next Actions

        • Increase allocation toward LinkedIn creators.

        • Reduce low efficiency creator spend.

        • Expand bundled insurance campaigns.

        • Improve SLA tracking before scaling outreach.
        """)

    st.divider()

    # ======================================================
    # STRATEGIC NOTES
    # ======================================================

    st.subheader("Strategic Operating Notes")

    st.info("""
    • LinkedIn creators continue delivering strongest blended ROI.

    • Repeat creators materially outperform one-off activations.

    • Attribution consistency remains the biggest operational bottleneck.

    • Dedicated YouTube should be treated selectively as awareness inventory.
    """)
