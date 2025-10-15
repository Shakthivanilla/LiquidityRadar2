"""
Data Management for Smart Liquidity Monitor
Handles Snowflake connection and data processing
"""

import streamlit as st
import snowflake.connector
import pandas as pd
import os
import time
from typing import Dict, Optional

def get_snowflake_config() -> Dict[str, Optional[str]]:
    """Get Snowflake configuration from environment variables"""
    return {
        "user": os.environ.get("SF_USER"),
        "password": os.environ.get("SF_PASS"),
        "account": os.environ.get("SF_ACCOUNT"),
        "warehouse": os.environ.get("SF_WAREHOUSE", "AIX_SF_WH"),
        "database": os.environ.get("SF_DB", "AIX_SF_DB"),
        "schema": os.environ.get("SF_SCHEMA", "PUBLIC")
    }

@st.cache_resource
def get_snowflake_connection() -> Optional[snowflake.connector.SnowflakeConnection]:
    """
    Create and return Snowflake connection with retry logic
    
    Returns:
        Snowflake connection object or None if connection fails
    """
    config = get_snowflake_config()
    
    # Validate required credentials
    if not all([config.get("user"), config.get("password"), config.get("account")]):
        st.error("❌ Missing Snowflake credentials. Please set SF_USER, SF_PASS, and SF_ACCOUNT environment variables.")
        return None
    
    # Retry connection with exponential backoff
    max_retries = 3
    for attempt in range(max_retries):
        try:
            conn = snowflake.connector.connect(**config)
            return conn
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                st.warning(f"⚠️ Connection attempt {attempt + 1} failed. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                st.error(f"❌ Failed to connect to Snowflake after {max_retries} attempts: {e}")
                return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_member_data() -> Optional[pd.DataFrame]:
    """
    Fetch member liquidity data from Snowflake with caching
    
    Returns:
        DataFrame: Processed member data or None if fetch fails
    """
    conn = get_snowflake_connection()
    if conn is None:
        st.error("❌ No database connection available.")
        return None
    
    try:
        query = "SELECT member_id, name, cash_buffer_usd, exposure_usd, updated_at FROM AIX_SF_DB.PUBLIC.MEMBERS_NEW;"
        cursor = conn.cursor()
        cursor.execute(query)
        df = cursor.fetch_pandas_all()
        
        # Convert column names to lowercase for consistency
        df.columns = df.columns.str.lower()
        
        # Map exposure_usd to credit_headroom_usd for compatibility
        if 'exposure_usd' in df.columns and 'credit_headroom_usd' not in df.columns:
            df['credit_headroom_usd'] = df['exposure_usd']
        
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.info("💡 Please check your Snowflake connection and table structure.")
        return None

def calculate_risk_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate risk metrics for member data
    
    Args:
        df: DataFrame with member data
    
    Returns:
        DataFrame: Data with added risk metrics
    """
    # Risk Calculation
    df["risk_ratio"] = df["credit_headroom_usd"] / df["cash_buffer_usd"]
    df["risk_level"] = df["risk_ratio"].apply(
        lambda x: "HIGH" if x > 2 else "MEDIUM" if x > 1 else "LOW")
    
    # Risk Emoji Mapping
    def risk_emoji(level: str) -> str:
        return "🔴 High Risk" if level == "HIGH" else "🟡 Medium Risk" if level == "MEDIUM" else "🟢 Low Risk"
    
    df["Risk Insights"] = df["risk_level"].apply(risk_emoji)
    
    return df

def color_risk(val: str) -> str:
    """
    Return background color based on risk level (Dark theme compatible)
    
    Args:
        val: Risk level string
    
    Returns:
        str: CSS background color style
    """
    if val == "HIGH":
        return "background-color: rgba(255, 50, 50, 0.3); color: #ff6666"
    elif val == "MEDIUM":
        return "background-color: rgba(255, 193, 7, 0.3); color: #ffc107"
    else:
        return "background-color: rgba(40, 167, 69, 0.3); color: #4ade80"
