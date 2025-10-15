"""
AI Utilities for Smart Liquidity Monitor
Helper functions for Gemini AI interactions
"""

import streamlit as st
from google import genai
import os
import time
from typing import Optional
import pandas as pd

def get_gemini_client() -> Optional[genai.Client]:
    """Initialize and return Gemini AI client"""
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        st.error("❌ Missing GEMINI_API_KEY environment variable.")
        return None
    return genai.Client(api_key=gemini_api_key)

def get_ai_response(prompt: str, model: str = "gemini-2.5-flash", temperature: float = 0.3) -> Optional[str]:
    """
    Centralized function for Gemini AI API calls with retry logic
    
    Args:
        prompt: The prompt to send to Gemini AI
        model: The Gemini model to use (default: gemini-2.5-flash)
        temperature: Temperature for response generation (default: 0.3)
    
    Returns:
        str: AI response text or None if error occurs
    """
    client = get_gemini_client()
    if not client:
        return None
    
    # Retry with exponential backoff
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait_time)
            else:
                st.error(f"❌ Error calling Gemini AI after {max_retries} attempts: {e}")
                return None

def get_ai_response_with_retry(prompt: str, model: str = "gemini-2.5-flash", temperature: float = 0.3) -> Optional[str]:
    """
    Alias for get_ai_response for backward compatibility
    """
    return get_ai_response(prompt, model, temperature)

def run_liquidity_agent(df: pd.DataFrame, user_query: str, top_k: int = 5, model: str = "gemini-2.5-flash") -> Optional[str]:
    """
    Simple retrieval + prompt agent:
    - selects top_k rows by risk_ratio
    - builds a concise context string and asks Gemini the user's question
    
    Args:
        df: DataFrame with member liquidity data
        user_query: User's natural language question
        top_k: Number of top risky members to include in context (default: 5)
        model: Gemini model to use (default: gemini-2.5-flash)
    
    Returns:
        str: AI text response or None on error
    """
    try:
        if df is None or df.empty:
            return "No data available to analyze. Please ensure Snowflake connection is configured."
        
        # Ensure risk_ratio column exists
        if "risk_ratio" not in df.columns:
            # fallback: compute if possible
            if {"exposure_usd", "cash_buffer_usd"}.issubset(df.columns):
                df = df.copy()
                df["risk_ratio"] = df["exposure_usd"] / df["cash_buffer_usd"].replace({0: 1})
            elif {"credit_headroom_usd", "cash_buffer_usd"}.issubset(df.columns):
                df = df.copy()
                df["risk_ratio"] = df["credit_headroom_usd"] / df["cash_buffer_usd"].replace({0: 1})
            else:
                return "Dataset doesn't contain required columns for agent analysis."

        # pick top K risky members
        top_df = df.sort_values("risk_ratio", ascending=False).head(top_k)
        
        # small context: keep only key columns to avoid giant prompt
        cols_for_prompt = ["member_id", "name", "cash_buffer_usd", "exposure_usd", "credit_headroom_usd", "risk_ratio", "updated_at"]
        cols_for_prompt = [c for c in cols_for_prompt if c in top_df.columns]
        context_csv = top_df[cols_for_prompt].to_csv(index=False)

        # Build agent prompt. Keep it explicit and structured for consistent outputs
        agent_prompt = f"""
You are an expert financial risk advisor. The user asked: "{user_query}"

Below is tabular context of the top {top_k} members by liquidity risk (CSV).
Context:
{context_csv}

Tasks:
1) Answer the user's question concisely using the context.
2) Provide 2-3 actionable remediation steps (prioritized).
3) Provide a short confidence estimate (0-100%).

Respond in plain text with headings: "Answer:", "Recommended Actions:", "Confidence:".
"""
        # call existing wrapper
        resp = get_ai_response(agent_prompt, model=model)
        return resp
    except Exception as e:
        st.error(f"❌ Agent error: {e}")
        return None
