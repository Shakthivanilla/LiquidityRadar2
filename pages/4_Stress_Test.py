
import streamlit as st
from data import fetch_member_data, calculate_risk_metrics
from visualizations import create_monte_carlo_simulation
st.set_page_config(layout='wide')
st.title('Stress Tests & Scenarios')

df = fetch_member_data()
if df is None or df.empty:
    st.error("❌ No data available")
    st.stop()
df = calculate_risk_metrics(df)

st.markdown('Simulate shocks to liquidity buffers and view Monte Carlo outcomes.')
shock = st.slider('Stress shock multiplier', 0.5, 3.0, 1.2)
if st.button('Run Stress Simulation'):
    st.info('Running simulation...')
    fig = create_monte_carlo_simulation(df, shock)
    st.pyplot(fig)
    st.caption(f"Simulation run with shock multiplier: {shock}")
