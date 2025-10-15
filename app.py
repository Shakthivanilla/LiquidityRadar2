import streamlit as st
import os

# ===============================
#  🔧 PAGE CONFIGURATION
# ===============================
st.set_page_config(
    layout="wide", 
    page_title="Smart Liquidity Monitor", 
    page_icon="💧"
)

# ===============================
#  🎨 CUSTOM STYLING
# ===============================
# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===============================
#  🧭 SIDEBAR BRANDING
# ===============================
logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
st.sidebar.markdown("### 💧 Smart Liquidity Monitor")
st.sidebar.markdown("_AI-driven Risk Intelligence_")

# ===============================
#  🏠 MAIN LANDING PAGE
# ===============================
st.title("Welcome — LiquidityRadar")
st.markdown(
    """#### Futuristic, modular dashboard for liquidity risk monitoring.
Use the left sidebar to navigate between pages: Overview, Risk Analysis, AI Insights, Stress Tests, Reports, Settings."""
)

st.markdown("----")

# ===============================
#  🚀 QUICK ACTIONS
# ===============================
st.markdown("**Quick actions**")
col1, col2, col3 = st.columns(3)
col1.button("📊 Open Overview")
col2.button("🔍 Run Liquidity Scan")
col3.button("📄 Generate Report")

st.markdown("----")

# ===============================
#  💡 GETTING STARTED
# ===============================
st.subheader("Getting Started")
st.markdown("""
**Welcome to Smart Liquidity Monitor!** This AI-powered dashboard helps you:

- 📊 **Monitor Liquidity**: View real-time member liquidity positions
- ⚠️ **Risk Analysis**: Identify high-risk members with predictive ML models
- 🤖 **AI Insights**: Ask natural language questions about your data
- 🎯 **Stress Testing**: Run Monte Carlo simulations for worst-case scenarios
- 📄 **Reports**: Generate comprehensive PDF reports

**Navigation:**
- Use the sidebar to access different pages
- Start with **Overview** for a high-level dashboard
- Try **AI Insights** for natural language queries
""")

st.caption("💡 Tip: Use the 'AI Insights' page to ask natural language questions about the data.")
