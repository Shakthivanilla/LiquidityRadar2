
import streamlit as st
from data import fetch_member_data, calculate_risk_metrics, color_risk
st.set_page_config(layout='wide')
st.title('Risk Analysis')
st.markdown('Detailed table, heatmap and filters')

df = fetch_member_data()
if df is None or df.empty:
    st.error("❌ No data available")
    st.stop()
df = calculate_risk_metrics(df)

with st.expander('Filters'):
    min_ratio = st.slider('Minimum risk ratio', 0.0, 10.0, 0.0)
    show_level = st.multiselect('Show risk levels', ['LOW','MEDIUM','HIGH'], default=['HIGH','MEDIUM','LOW'])

filtered = df[df['risk_ratio'] >= min_ratio] if 'risk_ratio' in df.columns else df
filtered = filtered[filtered.get('risk_level', []).isin(show_level)] if 'risk_level' in filtered.columns else filtered

st.dataframe(filtered.style.map(color_risk, subset=['risk_level']) if 'risk_level' in filtered.columns else filtered, width='stretch')
