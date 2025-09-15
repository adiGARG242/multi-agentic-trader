# workflow/build_workflow.py

from langgraph.graph import StateGraph, START, END
from workflow.state import AgentState
from workflow.conditional_logic import ConditionalLogic

from agents.analyst_factory import create_analyst_node
from agents.researcher_factory import create_researcher_node
from agents.research_manager import ResearchManager
from agents.trader import TraderNode
from agents.risk_factory import create_risk_node
from agents.portfolio_manager import PortfolioManager
from agents.auditor import Auditor

from tools.toolkit import Toolkit
from memory.longterm_memory import AgentMemory
from llm_provider.gemini_adapter import GeminiAdapter


# -------------------------------
# 1. Initialize toolkit + LLMs
# -------------------------------
toolkit = Toolkit()
quick_llm = GeminiAdapter(model_name="gemini-1.5-flash")  # fast analysts & debaters
deep_llm = GeminiAdapter(model_name="gemini-1.5-pro")    # strategic agents

# -------------------------------
# 2. Initialize memories
# -------------------------------
bull_memory = AgentMemory("bull_memory")
bear_memory = AgentMemory("bear_memory")
research_manager_memory = AgentMemory("research_manager")

# -------------------------------
# 3. Create Analyst Nodes
# -------------------------------
market_analyst_node = create_analyst_node(quick_llm, toolkit, "Market Analyst")
social_analyst_node = create_analyst_node(quick_llm, toolkit, "Social Analyst")
news_analyst_node = create_analyst_node(quick_llm, toolkit, "News Analyst")
fundamentals_analyst_node = create_analyst_node(quick_llm, toolkit, "Fundamentals Analyst")

# -------------------------------
# 4. Create Debate Nodes
# -------------------------------
bull_prompt = "You are a Bull Analyst. Argue FOR investing in the ticker."
bear_prompt = "You are a Bear Analyst. Argue AGAINST investing in the ticker."

bull_researcher_node = create_researcher_node(quick_llm, bull_memory, bull_prompt, "Bull Analyst")
bear_researcher_node = create_researcher_node(quick_llm, bear_memory, bear_prompt, "Bear Analyst")

# -------------------------------
# 5. Manager, Trader, Risk, Portfolio
# -------------------------------
research_manager_node = ResearchManager(deep_llm, research_manager_memory).node
trader_node = TraderNode(quick_llm).node

risky_node = create_risk_node(quick_llm, AgentMemory("risky_memory"), "Aggressive risk persona", "Risky Analyst")
safe_node = create_risk_node(quick_llm, AgentMemory("safe_memory"), "Conservative risk persona", "Safe Analyst")
neutral_node = create_risk_node(quick_llm, AgentMemory("neutral_memory"), "Balanced risk persona", "Neutral Analyst")

portfolio_manager_node = PortfolioManager(deep_llm).node

# -------------------------------
# 6. Utility Node
# -------------------------------
def msg_clear_node(state):
    """Clear messages but keep ticker intact."""
    return {"messages": []}

# -------------------------------
# 7. Build Workflow Graph
# -------------------------------
workflow = StateGraph(AgentState)

# Register nodes
workflow.add_node("Market Analyst", market_analyst_node)
workflow.add_node("Social Analyst", social_analyst_node)
workflow.add_node("News Analyst", news_analyst_node)
workflow.add_node("Fundamentals Analyst", fundamentals_analyst_node)
workflow.add_node("Msg Clear", msg_clear_node)

workflow.add_node("Bull Researcher", bull_researcher_node)
workflow.add_node("Bear Researcher", bear_researcher_node)
workflow.add_node("Research Manager", research_manager_node)

workflow.add_node("Trader", trader_node)
workflow.add_node("Risky Analyst", risky_node)
workflow.add_node("Safe Analyst", safe_node)
workflow.add_node("Neutral Analyst", neutral_node)
workflow.add_node("Portfolio Manager", portfolio_manager_node)

# -------------------------------
# 8. Graph Logic
# -------------------------------
logic = ConditionalLogic(max_debate_rounds=2, max_risk_rounds=2)

# --- Analysts flow ---
workflow.set_entry_point("Market Analyst")
workflow.add_edge("Market Analyst", "Social Analyst")
workflow.add_edge("Social Analyst", "News Analyst")
workflow.add_edge("News Analyst", "Fundamentals Analyst")
workflow.add_edge("Fundamentals Analyst", "Msg Clear")

# --- Msg Clear → Bull Researcher ---
workflow.add_edge("Msg Clear", "Bull Researcher")

# --- Research Debate Loop ---
workflow.add_edge("Bull Researcher", "Bear Researcher")
workflow.add_edge("Bear Researcher", "Bull Researcher")

# After debate → Research Manager
workflow.add_edge("Bull Researcher", "Research Manager")
workflow.add_edge("Bear Researcher", "Research Manager")

# --- Manager → Trader ---
workflow.add_edge("Research Manager", "Trader")

# --- Risk Debate ---
workflow.add_edge("Trader", "Risky Analyst")
workflow.add_edge("Risky Analyst", "Safe Analyst")
workflow.add_edge("Safe Analyst", "Neutral Analyst")
workflow.add_edge("Neutral Analyst", "Risky Analyst")

# Risk → Portfolio Manager
workflow.add_edge("Risky Analyst", "Portfolio Manager")
workflow.add_edge("Safe Analyst", "Portfolio Manager")
workflow.add_edge("Neutral Analyst", "Portfolio Manager")

# --- Portfolio Manager → END ---
workflow.add_edge("Portfolio Manager", END)

# -------------------------------
# 9. Compile App
# -------------------------------
app = workflow.compile()
