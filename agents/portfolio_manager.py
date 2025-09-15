# agents/portfolio_manager.py
from llm_provider.gemini_adapter import GeminiAdapter
from langsmith.run_helpers import traceable

class PortfolioManager:
    def __init__(self, llm: GeminiAdapter):
        self.llm = llm

    @traceable(name="Portfolio Manager")
    def node(self, state: dict):
        trader_plan = state.get("trader_investment_plan","")
        risk_history = state.get("risk_debate_state",{}).get("history","")
        prompt = f"""You are the Portfolio Manager. Review trader plan and risk debate and return a final binding decision: BUY / SELL / HOLD followed by a short justification and execution steps.
Trader Plan:
{trader_plan}
Risk Debate:
{risk_history}
"""
        out = self.llm.chat([prompt])
        return {"final_trade_decision": out}
