# tools/yfinance_tool.py
import yfinance as yf

def get_yfinance_data(ticker: str, period: str = "6mo"):
    t = yf.Ticker(ticker)
    hist = t.history(period=period)
    return hist.tail(20).to_json()  # small recent window, JSON-friendly
