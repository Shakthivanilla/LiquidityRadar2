
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

# Load data
df = fetch_member_data()
if df is None or df.empty:
    st.error("❌ No data available")
    st.stop()
df = calculate_risk_metrics(df)

# fetch persisted display limit
display_limit = get_pref('display_limit', 50)

# ===============================
# KEY METRICS DASHBOARD
# ===============================
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Members", len(df))
col2.metric("High Risk", int((df['risk_level']=='HIGH').sum() if 'risk_level' in df.columns else 0))
col3.metric("Avg Risk Ratio", f"{df['risk_ratio'].mean():.2f}" if 'risk_ratio' in df.columns else "N/A")
col4.metric("Updated At", str(df['updated_at'].max()) if 'updated_at' in df.columns else "N/A")

st.markdown("---")

# ===============================
# MEMBER DATA TABLE (Collapsible)
# ===============================
with st.expander("📊 Member Data Table", expanded=True):
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

# ===============================
# ARIMA LIQUIDITY FORECASTING (Collapsible)
# ===============================
with st.expander("🔮 Liquidity Projection (Next 3 Months)", expanded=False):
    st.markdown("""
    Using **ARIMA (AutoRegressive Integrated Moving Average)** time series forecasting to predict future liquidity trends.
    Select a member below to see their projected cash buffer and credit headroom.
    """)
    
    # Member selection
    member_list = df['name'].tolist() if 'name' in df.columns else df['member_id'].tolist()
    selected_member_name = st.selectbox('Select Member for Forecast', member_list, key='forecast_member')
    
    if selected_member_name:
        selected_member_data = df[df['name'] == selected_member_name].iloc[0] if 'name' in df.columns else df[df['member_id'] == selected_member_name].iloc[0]
        
        # Display current metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Cash Buffer", f"${selected_member_data['cash_buffer_usd']:,.0f}")
        col2.metric("Current Credit Headroom", f"${selected_member_data['credit_headroom_usd']:,.0f}")
        col3.metric("Current Risk Ratio", f"{selected_member_data.get('risk_ratio', 0):.2f}")
        
        # Generate and display forecast
        with st.spinner("Generating ARIMA forecast..."):
            fig = create_liquidity_forecast(selected_member_data, selected_member_name)
            st.pyplot(fig)
        
        # Model Information
        with st.expander("ℹ️ About ARIMA Forecasting"):
            st.markdown("""
            **ARIMA Model:** AutoRegressive Integrated Moving Average (2,1,1)
            - **Order (2,1,1):** 2 autoregressive terms, 1 differencing, 1 moving average term
            - **Historical Data:** 12 months of simulated historical patterns
            - **Forecast Horizon:** 3 months ahead
            - **Features:** Cash Buffer and Credit Headroom trends
            
            **How to Interpret:**
            - **Upward trend:** Improving liquidity position
            - **Downward trend:** Potential liquidity concerns
            - **Gap widening:** Risk ratio may be increasing
            """)
    else:
        st.info("Select a member to view forecast.")
