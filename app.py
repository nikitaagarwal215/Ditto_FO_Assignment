import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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
# CUSTOM CSS
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
    font-weight: 700 !important;
}

[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
    transition: all 0.3s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.08);
}

.stButton>button {
    background-color: #FF6B6B;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    padding: 10px 18px;
}

.stButton>button:hover {
    background-color: #F45B5B;
    """)
