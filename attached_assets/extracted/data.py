"""
Data Management for Smart Liquidity Monitor
Handles Snowflake connection and data processing
"""

import streamlit as st
import snowflake.connector
import pandas as pd
import os

def get_snowflake_config():
    """Get Snowflake configuration from environment variables"""
    return {
        "user": os.environ.get("SF_USER"),
        "password": os.environ.get("SF_PASS"),
        "account": os.environ.get("SF_ACCOUNT"),
        "warehouse": "COMPUTE_WH",
        "database": os.environ.get("SF_DB", "LIQUIDITY_RADAR"),
        "schema": os.environ.get("SF_SCHEMA", "HACKATHON")
    }

def get_snowflake_connection():
    """Create and return Snowflake connection"""
    config = get_snowflake_config()
    return snowflake.connector.connect(**config)

@st.cache_data(ttl=300)
def fetch_member_data(conn):
    """
    Fetch member liquidity data from Snowflake
    
    Args:
        conn: Snowflake connection object
    
    Returns:
        DataFrame: Processed member data with risk calculations
    """
    try:
        query = "SELECT member_id, name, cash_buffer_usd, exposure_usd, updated_at FROM members;"
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
        st.error(f"Error loading data: {e}")
        st.info("Please check your Snowflake connection and table structure.")
        return None

def calculate_risk_metrics(df):
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
    def risk_emoji(level):
        return "🔴 High Risk" if level == "HIGH" else "🟡 Medium Risk" if level == "MEDIUM" else "🟢 Low Risk"
    
    df["Risk Insights"] = df["risk_level"].apply(risk_emoji)
    
    return df

def color_risk(val):
    """
    Return background color based on risk level
    
    Args:
        val: Risk level string
    
    Returns:
        str: CSS background color style
    """
    if val == "HIGH":
        return "background-color: #ffcccc"
    elif val == "MEDIUM":
        return "background-color: #fff3cd"
    else:
        return "background-color: #d4edda"
