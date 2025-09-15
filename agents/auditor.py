# agents/auditor.py
from llm_provider.gemini_adapter import GeminiAdapter
from langsmith.run_helpers import traceable

class Auditor:
    def __init__(self, llm: GeminiAdapter):
        self.llm = llm

    @traceable(name="Auditor")
    def audit(self, state: dict):
        trader_plan = state.get("trader_investment_plan","")
        risk_summary = state.get("risk_debate_state",{}).get("history","")
        schema = {
            "action":"buy/sell/hold",
            "quantity_usd":"number or null",
            "stop_loss":"number or null",
            "price_target_low":"number or null",
            "price_target_high":"number or null",
            "confidence":"low/medium/high"
        }
        parsed = self.llm.structured_output([f"Parse this trade:\n{trader_plan}"], schema)
        # Basic sanity checks
        notes=[]
        ok=True
        if parsed.get("action") not in ("buy","sell","hold"):
            ok=False; notes.append("invalid action")
        return {"parsed_proposal": parsed, "checks_passed": ok, "notes": notes}
