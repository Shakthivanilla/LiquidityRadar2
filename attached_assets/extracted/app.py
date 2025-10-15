
import streamlit as st, os
st.set_page_config(layout="wide", page_title="Smart Liquidity Monitor", page_icon="💧")

# Load custom styles
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar branding
st.sidebar.image(os.path.join("assets", "logo.png"), use_column_width=True)
st.sidebar.markdown("### 💧 Smart Liquidity Monitor")
st.sidebar.markdown("_AI-driven Risk Intelligence_")

st.title("Welcome — LiquidityRadar")
st.markdown(
    """#### Futuristic, modular dashboard for liquidity risk monitoring.
Use the left sidebar to navigate between pages: Overview, Risk Analysis, AI Insights, Stress Tests, Reports, Settings."""
)
st.markdown("----")
st.markdown("**Quick actions**")
col1, col2, col3 = st.columns(3)
col1.button("Open Overview")
col2.button("Run Liquidity Scan")
col3.button("Generate Report")
st.caption("Tip: Use the 'AI Insights' page to ask natural language questions about the data.")
