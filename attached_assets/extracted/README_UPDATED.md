Smart Liquidity Monitor - Updated (Agent added)

Changes made:
- Added a simple Liquidity Advisor Agent (ai_utils.run_liquidity_agent) that answers natural-language queries using top-risk member context.
- Added get_ai_response_with_retry wrapper for resiliency.
- Cached fetch_member_data with @st.cache_data(ttl=300) to reduce Snowflake calls.
- Added Agent UI in app.py for interactive queries and export of responses.
- Removed unused sklearn import from app.py.
- Created this README_UPDATED.md describing env vars and usage.

Environment variables (set these securely; do NOT commit keys):
- GEMINI_API_KEY : Google Gemini API key
- SF_USER, SF_PASS, SF_ACCOUNT : Snowflake credentials

Testing tips:
- If you don't have GEMINI_API_KEY while testing, temporarily mock ai_utils.get_ai_response to return a test string.
- Run: streamlit run app.py
