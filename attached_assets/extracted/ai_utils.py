"""
AI Utilities for Smart Liquidity Monitor
Helper functions for Gemini AI interactions
"""

import streamlit as st
from google import genai
import os

def get_gemini_client():
    """Initialize and return Gemini AI client"""
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=gemini_api_key)

def get_ai_response(prompt, model="gemini-2.5-flash", temperature=0.3):
    """
    Centralized function for Gemini AI API calls
    
    Args:
        prompt (str): The prompt to send to Gemini AI
        model (str): The Gemini model to use (default: gemini-2.5-flash)
        temperature (float): Temperature for response generation (default: 0.3)
    
    Returns:
        str: AI response text or None if error occurs
    """
    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text
    except Exception as e:
        st.error(f"Error calling Gemini AI: {e}")
        return None


import time
import logging
logging.getLogger(__name__).setLevel(logging.INFO)

def get_ai_response_with_retry(prompt, model="gemini-2.5-flash", temperature=0.3, retries=3, backoff=2):
    """
    Wrapper to call get_ai_response with simple retry/backoff.
    Returns string or None.
    """
    for attempt in range(1, retries+1):
        try:
            resp = get_ai_response(prompt, model=model, temperature=temperature)
            return resp
        except Exception as e:
            logging.warning("AI call failed attempt %s/%s: %s", attempt, retries, e)
            if attempt < retries:
                time.sleep(backoff ** attempt)
    return None

def run_liquidity_agent(df, user_query, top_k=5, model="gemini-2.5-flash"):
    \"\"\"Simple retrieval + prompt agent:
    - selects top_k rows by risk_ratio
    - builds a concise context string and asks Gemini the user's question
    Returns: AI text response (string) or None on error
    \"\"\"
    try:
        import pandas as pd
        if df is None or df.empty:
            return "No data available to analyze. Please ensure Snowflake connection is configured."
        # Ensure risk_ratio column exists
        if "risk_ratio" not in df.columns:
            if {"exposure_usd", "cash_buffer_usd"}.issubset(df.columns):
                df = df.copy()
                df["risk_ratio"] = df["exposure_usd"] / df["cash_buffer_usd"].replace({0: 1})
            else:
                return "Dataset doesn't contain required columns for agent analysis."

        top_df = df.sort_values("risk_ratio", ascending=False).head(top_k)
        cols_for_prompt = ["member_id", "name", "cash_buffer_usd", "exposure_usd", "risk_ratio", "updated_at"]
        cols_for_prompt = [c for c in cols_for_prompt if c in top_df.columns]
        context_csv = top_df[cols_for_prompt].to_csv(index=False)

        agent_prompt = f\"\"\"You are an expert financial risk advisor. The user asked: \"{user_query}\"

Below is tabular context of the top {top_k} members by liquidity risk (CSV).
Context:
{context_csv}

Tasks:
1) Answer the user's question concisely using the context.
2) Provide 2-3 actionable remediation steps (prioritized).
3) Provide a short confidence estimate (0-100%).

Respond in plain text with headings: \"Answer:\", \"Recommended Actions:\", \"Confidence:\".
\"\"\"

        resp = get_ai_response_with_retry(agent_prompt, model=model)
        return resp
    except Exception as e:
        try:
            import streamlit as st
            st.error(f\"Agent error: {e}\")
        except Exception:
            pass
        return None
