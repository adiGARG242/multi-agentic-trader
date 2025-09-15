# workflow/conditional_logic.py
class ConditionalLogic:
    def __init__(self, max_debate_rounds=2, max_risk_rounds=2):
        self.max_debate_rounds = max_debate_rounds
        self.max_risk_rounds = max_risk_rounds

    def should_continue_analyst(self, state: dict):
        print("[DEBUG] should_continue_analyst called")
    # If analyst already produced something, maybe go to tools
        if state.get("messages"):
            print("[DEBUG] Analyst produced messages → sending to tools")
            return "tools"
        print("[DEBUG] Analyst finished → continue")
        return "continue"


    def should_continue_debate(self, state):
        debate_state = state.get("investment_debate_state", {})
        if debate_state.get("count",0) >= 2 * self.max_debate_rounds:
            return "Research Manager"
        # alternate: if count even -> Bull, else Bear (as article alternates speakers)
        if debate_state.get("count",0) % 2 == 0:
            return "Bull Researcher"
        return "Bear Researcher"

    def should_continue_risk(self, state):
        rs = state.get("risk_debate_state",{})
        if rs.get("count",0) >= self.max_risk_rounds * 3: # 3 personas
            return "Risk Judge"
        # cycle through Risky -> Safe -> Neutral
        c = rs.get("count",0) % 3
        if c == 0:
            return "Risky Analyst"
        if c == 1:
            return "Safe Analyst"
        return "Neutral Analyst"
