# main.py
import sys, os
from workflow.build_workflow import app

# set env flag before build_workflow imports GeminiAdapter
if "--mock" in sys.argv:
    os.environ["MOCK_MODE"] = "1"
else:
    os.environ["MOCK_MODE"] = "0"

def run():
    ticker = "AAPL"
    print(f"Starting workflow for {ticker}")
    if os.environ["MOCK_MODE"] == "1":
        print("[MOCK GEMINI ACTIVE: No API calls to Gemini]")
    result = app.invoke({"ticker": ticker, "messages": []})
    print("\n--- FINAL RESULT ---")
    print(result)

if __name__ == "__main__":
    run()
