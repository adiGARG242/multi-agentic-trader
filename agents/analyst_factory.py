# agents/analyst_factory.py
from typing import Callable
from llm_provider.gemini_adapter import GeminiAdapter
from tools.toolkit import Toolkit
from langsmith.run_helpers import traceable

def create_analyst_node(llm: GeminiAdapter, toolkit: Toolkit, analyst_name: str) -> Callable:
    def analyst_node(state: dict):
        ticker = state.get("ticker")
        situation = {
            "market": toolkit.get_yfinance_data(ticker),
            "news": toolkit.get_finnhub_news(ticker),
            "sentiment": toolkit.get_social_media_sentiment(ticker),
            "fundamentals": toolkit.get_fundamental_analysis(ticker),
        }
        prompt = f"""You are {analyst_name}. Provide a concise report for {ticker}.
Situation: {situation}"""
        out = llm.chat([prompt])

        # map analyst to correct field
        field_map = {
            "Market Analyst": "market_report",
            "Social Analyst": "sentiment_report",
            "News Analyst": "news_report",
            "Fundamentals Analyst": "fundamentals_report"
        }
        field_name = field_map.get(analyst_name, f"{analyst_name.lower().replace(' ','_')}_report")

        return {field_name: out}
    return analyst_node
