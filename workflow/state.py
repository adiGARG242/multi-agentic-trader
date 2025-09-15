# workflow/state.py
from typing import TypedDict, List, Optional
import operator
from langgraph.graph import add_messages

class AgentState(TypedDict, total=False):
    # persist ticker across nodes
    ticker: str

    # messages handled with add_messages so they append, not overwrite
    messages: List[str]

    # analyst reports
    market_report: str
    sentiment_report: str
    news_report: str
    fundamentals_report: str

    # debate state
    investment_debate_state: dict

    # investment plan
    investment_plan: str

    # trader proposal
    trader_investment_plan: str

    # risk debate
    risk_debate_state: dict

    # final decision
    final_trade_decision: str

# LangGraph merge rules
graph_config = {
    "messages": add_messages,   # special function from langgraph
    "ticker": operator.or_,     # keep non-None ticker
}
