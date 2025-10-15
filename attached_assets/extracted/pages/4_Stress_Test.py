
import streamlit as st
from data import fetch_member_data, calculate_risk_metrics
from visualizations import create_montecarlo_simulation
st.set_page_config(layout='wide')
st.title('Stress Tests & Scenarios')

df = fetch_member_data()
df = calculate_risk_metrics(df)

st.markdown('Simulate shocks to liquidity buffers and view Monte Carlo outcomes.')
shock = st.slider('Stress shock multiplier', 0.5, 3.0, 1.2)
if st.button('Run Stress Simulation'):
    st.info('Running simulation...')
    fig = create_montecarlo_simulation(df) if 'create_montecarlo_simulation' in dir(__import__('visualizations')) else None
    if fig is not None:
        st.pyplot(fig)
    else:
        st.info('Simulation function not available.')
