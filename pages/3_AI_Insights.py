
import streamlit as st
from data import fetch_member_data, calculate_risk_metrics
from ai_utils import run_liquidity_agent, get_ai_response_with_retry
from prompts import get_ai_summary_prompt
st.set_page_config(layout='wide')
st.title('AI Insights')

df = fetch_member_data()
if df is None or df.empty:
    st.error("❌ No data available")
    st.stop()
df = calculate_risk_metrics(df)

st.subheader('AI Summary (Quick)')
if st.button('Generate AI Summary'):
    st.info('Calling AI model...')
    df_string = df.head(50).to_csv(index=False)
    prompt = get_ai_summary_prompt(df_string)
    resp = get_ai_response_with_retry(prompt)
    st.code(resp or 'No response from AI.')

st.markdown('---')
st.subheader('Liquidity Advisor (Ask a question)')
query = st.text_input('Ask the Liquidity Advisor', value='Which members are likely to be high risk next quarter?')
if st.button('Run Agent'):
    with st.spinner('Running agent...'):
        resp = run_liquidity_agent(df, query, top_k=5)
        if resp:
            st.markdown('**Agent Response**')
            st.write(resp)
        else:
            st.error('Agent returned no response.')
