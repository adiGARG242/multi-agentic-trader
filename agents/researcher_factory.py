# agents/researcher_factory.py
from typing import Callable
from llm_provider.gemini_adapter import GeminiAdapter
from memory.longterm_memory import AgentMemory
from langsmith.run_helpers import traceable

def create_researcher_node(llm: GeminiAdapter, memory: AgentMemory, role_prompt: str, agent_name: str) -> Callable:
    @traceable(name=f"Researcher-{agent_name}")
    def researcher_node(state: dict):
        # Consolidate analyst reports that were stored in the state by analyst nodes
        situation_summary = (
            f"Market Report: {state.get('market_report','')}\n"
            f"Sentiment Report: {state.get('sentiment_report','')}\n"
            f"News Report: {state.get('news_report','')}\n"
            f"Fundamentals Report: {state.get('fundamentals_report','')}\n"
        )

        # Query past memories (AgentMemory)
        past_memories = memory.get_memories(situation_summary)
        past_memory_str = "\n".join([m.get("document","") for m in past_memories]) if past_memories else "No past memories."

        # debate state object in state
        debate_state = state.get("investment_debate_state", {
            "history": "",
            "bull_history": "",
            "bear_history": "",
            "current_response": "",
            "count": 0
        })

        opponent_last = debate_state.get("current_response", "")

        prompt = f"""{role_prompt}
You are '{agent_name}'. Use the situation summary below, the debate history, the opponent's last argument, and past memories.
Situation Summary:
{situation_summary}

Debate History:
{debate_state['history']}

Opponent's last:
{opponent_last}

Your Past Similar Cases:
{past_memory_str}

Produce a single short argument (1-4 paragraphs)."""
        response = llm.chat([prompt])
        argument = f"{agent_name}: {response}"

        # Update debate state
        new_state = debate_state.copy()
        new_state["history"] = new_state.get("history","") + "\n" + argument
        if "Bull" in agent_name:
            new_state["bull_history"] = new_state.get("bull_history","") + "\n" + argument
        else:
            new_state["bear_history"] = new_state.get("bear_history","") + "\n" + argument
        new_state["current_response"] = argument
        new_state["count"] = new_state.get("count",0) + 1

        # Optionally store this argument in agent memory
        try:
            memory.add_memory(f"{state.get('ticker')}_{agent_name}_{new_state['count']}", argument)
        except Exception:
            pass

        return {"investment_debate_state": new_state}
    return researcher_node
