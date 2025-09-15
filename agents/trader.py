# agents/trader.py
from llm_provider.gemini_adapter import GeminiAdapter
from langsmith.run_helpers import traceable

class TraderNode:
    def __init__(self, llm: GeminiAdapter):
        self.llm = llm

    @traceable(name="Trader")
    def node(self, state: dict):
        plan = state.get("investment_plan","")
        prompt = f"""You are a trading agent. Convert the investment plan into a concrete trading proposal.
Include: Action (BUY/SELL/HOLD), quantity (USD), price limits, stop-loss, rationale.
**IMPORTANT:** Your response MUST end with a single line tag exactly like:
FINAL TRANSACTION PROPOSAL: **BUY**  (or **SELL** / **HOLD**)
"""
        out = self.llm.chat([prompt])
        return {"trader_investment_plan": out}
