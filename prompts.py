"""
AI Prompt Templates for Smart Liquidity Monitor
Centralized prompts for Gemini AI interactions
"""

from typing import List

def get_ai_summary_prompt(df_string: str) -> str:
    """Generate prompt for AI liquidity risk summary"""
    return f"""
    You are a financial risk analyst. Summarize which members are most at liquidity risk
    and give 2 recommendations to reduce exposure.
    Data:
    {df_string}
    """

def get_natural_language_query_prompt(query_input: str, columns: List[str]) -> str:
    """Generate prompt for converting natural language to pandas filter"""
    return f"""
    Convert the following query into a pandas filter expression for df:
    '{query_input}'
    DataFrame columns: {columns}
    Return only the valid Python code to filter the dataframe.
    """

def get_optimization_plan_prompt(df_string: str) -> str:
    """Generate prompt for AI liquidity optimization plan"""
    return f"""
    You are an expert liquidity strategist.
    Given the following data, propose a 3-step action plan to lower risk ratios below 1.5
    while maintaining minimum cash buffers. Include confidence score (0–100%).
    Data:
    {df_string}
    """

def get_aquamind_agent_prompt(df_string: str) -> str:
    """Generate prompt for AquaMind AI Agent analysis"""
    return f"""
    You are AquaMind, an autonomous AI liquidity agent.
    Your job is to:
    1. Detect any abnormal liquidity risks.
    2. Predict who will be at high risk next quarter.
    3. Provide actionable recommendations with confidence scores.
    4. Suggest any stress scenarios that could impact stability.

    Data:
    {df_string}

    Respond concisely in the following format:
    **Detected Risks:** ...
    **Predicted High-Risk Members:** ...
    **Recommended Actions:** ...
    **Confidence:** (as %)
    """
