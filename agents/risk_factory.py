# agents/risk_factory.py
from llm_provider.gemini_adapter import GeminiAdapter
from memory.longterm_memory import AgentMemory
from langsmith.run_helpers import traceable

def create_risk_node(llm: GeminiAdapter, memory: AgentMemory, persona_prompt: str, name: str):
    @traceable(name=f"Risk-{name}")
    def risk_node(state: dict):
        trader_plan = state.get("trader_investment_plan","")
        debate_history = state.get("risk_debate_state", {"history":"", "count":0})
        prompt = f"""{persona_prompt}
Given the trader's proposal below, evaluate risks and propose changes or guardrails. Provide a short note.
Trader Plan:
{trader_plan}
Risk debate history:
{debate_history.get('history','')}
"""
        out = llm.chat([prompt])
        new_state = debate_history.copy()
        new_state["history"] = new_state.get("history","") + "\n" + f"{name}: {out}"
        new_state["count"] = new_state.get("count",0) + 1
        return {"risk_debate_state": new_state}
    return risk_node
