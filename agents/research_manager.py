# agents/research_manager.py
from llm_provider.gemini_adapter import GeminiAdapter
from memory.longterm_memory import AgentMemory
from langsmith.run_helpers import traceable

class ResearchManager:
    def __init__(self, llm: GeminiAdapter, memory: AgentMemory):
        self.llm = llm
        self.memory = memory

    @traceable(name="Research Manager")
    def node(self, state: dict):
        debate = state.get("investment_debate_state", {})
        prompt = f"""As the Research Manager, critically evaluate the debate history and produce:
1) Recommendation: BUY / SELL / HOLD
2) Short rationale
3) Strategic actions (entries, stop losses, position sizing)

Debate History:
{debate.get('history','')}

Analyst Reports:
Market: {state.get('market_report','')}
Sentiment: {state.get('sentiment_report','')}
News: {state.get('news_report','')}
Fundamentals: {state.get('fundamentals_report','')}
"""
        out = self.llm.chat([prompt])
        # Save to state under 'investment_plan'
        return {"investment_plan": out}
