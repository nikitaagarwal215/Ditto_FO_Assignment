import pandas as pd
import streamlit as st
import plotly.express as px
import time

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Ditto Influencer Operating System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CUSTOM CSS — DITTO STYLE
# ======================================================

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #FFFFFF;
    color: #1E293B;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #F8FAFC;
}

/* Headers */
h1, h2, h3 {
    color: #1E293B !important;
    font-weight: 700 !important;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
    transition: all 0.3s ease;
}

/* Hover Animation */
[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    box-shadow: 0px 6px 16px rgba(0,0,0,0.08);
}

/* Buttons */
.stButton>button {
    background-color: #FF6B6B;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    padding: 10px 18px;
}

.stButton>button:hover {
    background-color: #F45B5B;
    color: white;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

/* Expanders */
.streamlit-expanderHeader {
    font-weight: 600;
    color: #1E293B;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOADING
# ======================================================

with st.spinner("Loading Ditto Operating System..."):
    time.sleep(1)

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

executive_mode = st.sidebar.checkbox(
    "Executive Summary Mode"
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

st.success("🟢 All systems operational")

st.caption("Last synced: 10-May-2026 | 11:42 PM")

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

    with st.container(border=True):

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Total Spend",
            f"₹{total_spend/10000000:.2f} Cr",
            "+12% vs last cycle"
        )

        col2.metric(
            "Premiums Generated",
            f"₹{total_premium/10000000:.2f} Cr",
            "+18% vs last cycle"
        )

        col3.metric(
            "Portfolio ROI",
            f"{portfolio_roi:.2f}x",
            "+0.4x improvement"
        )

        col4.metric(
            "Conversions",
            int(filtered_df["Total_converts"].sum()),
            "+9%"
        )

        col5.metric(
            "Negative ROI %",
            f"{negative_roi_pct:.1f}%",
            "-3%"
        )

    st.progress(82)
    st.caption("Portfolio Efficiency Score")

    st.divider()

    # ======================================================
    # TABS
    # ======================================================

    tab1, tab2, tab3 = st.tabs([
        "Portfolio Overview",
        "Content Analysis",
        "Risk Intelligence"
    ])

    # ======================================================
    # TAB 1
    # ======================================================

    with tab1:

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

    # ======================================================
    # TAB 2
    # ======================================================

    with tab2:

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

    # ======================================================
    # TAB 3
    # ======================================================

    with tab3:

        st.subheader("Portfolio Risk Alerts")

        st.error("""
        🔴 Dedicated YouTube campaigns continue underperforming blended portfolio ROI.

        🔴 Portfolio ROI remains concentrated among repeat creators.

        🔴 Standalone Term campaigns continue showing weaker conversion efficiency.
        """)

        st.warning("""
        🟡 4 campaigns pending follow-up beyond SLA timelines.

        🟡 2 creators awaiting revised pricing approvals.
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

    st.success("🟢 CRM System Healthy")

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

    with st.expander("View Campaign Data"):

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

    if st.button("Generate Founder Recommendations"):

        st.toast("Top creators identified for scale allocation")

        st.success("""
        Recommended Next Actions

        • Increase allocation toward LinkedIn creators.

        • Reduce low efficiency creator spend.

        • Expand bundled insurance campaigns.

        • Improve SLA tracking before scaling outreach.
        """)

    st.divider()

    st.subheader("Strategic Operating Notes")

    st.info("""
    • LinkedIn creators continue delivering strongest blended ROI.

    • Repeat creators materially outperform one-off activations.

    • Attribution consistency remains the biggest operational bottleneck.

    • Dedicated YouTube should be treated selectively as awareness inventory.
    """)
