
import streamlit as st, os
from data import fetch_member_data, calculate_risk_metrics
st.set_page_config(layout='wide')
st.title('Reports & Export')

df = fetch_member_data()
df = calculate_risk_metrics(df)

st.markdown('Generate PDF reports for stakeholders.')
if st.button('Generate PDF Report'):
    # simple export - write CSV download for now
    csv = df.to_csv(index=False)
    st.download_button('Download CSV', csv, file_name='liquidity_snapshot.csv')
