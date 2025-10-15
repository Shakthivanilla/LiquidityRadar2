
import streamlit as st, os
from data import fetch_member_data, calculate_risk_metrics
from visualizations import create_liquidity_forecast
from redis_cache import get_pref
st.set_page_config(layout="wide")
# Background and Lottie header
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Background handled by CSS - no need for image overlay

# Try to show lottie animation if library available, else show title
try:
    from streamlit_lottie import st_lottie
    import json
    lottie_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sci_fi_header_lottie.json")
    with open(lottie_path, "r", encoding="utf-8") as f:
        lottie_json = json.load(f)
    st_lottie(lottie_json, height=200)
except Exception:
    st.title("Overview — LiquidityRadar")

st.title("Overview")
st.markdown("High-level metrics and recent trends")

# Load data
df = fetch_member_data()
if df is None or df.empty:
    st.error("❌ No data available")
    st.stop()
df = calculate_risk_metrics(df)

# fetch persisted display limit
display_limit = get_pref('display_limit', 50)

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Members", len(df))
col2.metric("High Risk", int((df['risk_level']=='HIGH').sum() if 'risk_level' in df.columns else 0))
col3.metric("Avg Risk Ratio", f"{df['risk_ratio'].mean():.2f}" if 'risk_ratio' in df.columns else "N/A")
col4.metric("Updated At", str(df['updated_at'].max()) if 'updated_at' in df.columns else "N/A")

st.markdown("---")

# Display data table
st.subheader("📊 Member Data Table")
# Reorder columns to place Risk Insights next to name
cols = df.columns.tolist()
if 'name' in cols and 'Risk Insights' in cols:
    cols.remove('Risk Insights')
    name_idx = cols.index('name')
    cols.insert(name_idx + 1, 'Risk Insights')
    df_display = df[cols]
else:
    df_display = df
st.dataframe(df_display.head(display_limit), width='stretch')

st.markdown("---")
# Forecast for top member
top = df.sort_values('risk_ratio', ascending=False).head(1)
if not top.empty:
    member_name = top['name'].iloc[0] if 'name' in top.columns else top['member_id'].iloc[0]
    st.subheader(f"Liquidity Forecast — {member_name}")
    fig = create_liquidity_forecast(top.iloc[0], member_name)
    st.pyplot(fig)
else:
    st.info("No member data to show.")
