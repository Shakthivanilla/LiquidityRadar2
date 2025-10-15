
import streamlit as st, os
from redis_cache import get_pref, set_pref

st.set_page_config(layout='wide')
st.title('Settings & Configuration')
st.markdown('Configure environment variables and thresholds (local settings only).')
st.info('Important: Do NOT store secrets in repo. Use environment variables in deployment.')

# Load persisted prefs (or defaults)
high_risk_default = get_pref('high_risk_threshold', 2.0)
low_risk_default = get_pref('low_risk_threshold', 0.8)
display_limit_default = get_pref('display_limit', 50)

col1, col2 = st.columns(2)
with col1:
    high_risk = st.number_input('High risk threshold (risk ratio)', value=float(high_risk_default), step=0.1)
    low_risk = st.number_input('Low risk threshold (risk ratio)', value=float(low_risk_default), step=0.1)
with col2:
    display_limit = st.number_input('Table display limit', value=int(display_limit_default), step=1)
    st.write('Environment variables (visible):')
    st.text('SF_USER: ' + (os.environ.get('SF_USER') or 'not set'))

if st.button('Save Settings'):
    set_pref('high_risk_threshold', float(high_risk))
    set_pref('low_risk_threshold', float(low_risk))
    set_pref('display_limit', int(display_limit))
    st.success('Settings saved.')
    st.rerun()

st.markdown('---')
st.write('Note: Preferences are persisted to Redis when REDIS_URL is configured; otherwise persisted to a local file `assets/preferences.json`.')
