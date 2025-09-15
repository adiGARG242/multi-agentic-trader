# tools/toolkit.py
import yfinance as yf
import os
try:
    import finnhub
except Exception:
    finnhub = None
from dotenv import load_dotenv
load_dotenv()

FINNHUB_KEY = os.getenv("FINNHUB_API_KEY")

def get_yfinance_data(ticker: str, period: str = "6mo"):
    """
    Fetch historical stock price data for a given ticker using Yahoo Finance.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").
        period (str): The period of history to fetch (default: "6mo").
    
    Returns:
        str: JSON string of recent stock data (last 20 days).
    """
    t = yf.Ticker(ticker)
    hist = t.history(period=period)
    return hist.tail(20).to_json()

def get_finnhub_news(ticker: str, _from: str = None, to: str = None):
    """
    Fetch recent company news headlines and summaries from Finnhub API.
    
    Args:
        ticker (str): The stock ticker symbol.
        _from (str): Start date in YYYY-MM-DD format (optional).
        to (str): End date in YYYY-MM-DD format (optional).
    
    Returns:
        str: Concatenated string of news headlines and summaries.
    """
    if finnhub is None or not FINNHUB_KEY:
        return "Finnhub not configured; no news."
    client = finnhub.Client(api_key=FINNHUB_KEY)
    try:
        news = client.company_news(ticker, _from=_from, to=to)
        items = []
        for n in news[:5]:
            items.append(f"Headline: {n.get('headline')}\nSummary: {n.get('summary','')}")
        return "\n\n".join(items) if items else "No recent news"
    except Exception as e:
        return f"Error fetching Finnhub: {e}"

def get_social_media_sentiment(ticker: str, date: str = None):
    """
    Retrieve recent social media sentiment for a given ticker.
    
    Args:
        ticker (str): The stock ticker symbol.
        date (str): Optional date filter (YYYY-MM-DD).
    
    Returns:
        str: Sentiment analysis summary (stubbed).
    """
    return f"Social sentiment stub for {ticker} on {date}."

def get_fundamental_analysis(ticker: str):
    """
    Retrieve basic fundamental analysis for a given ticker.
    
    Args:
        ticker (str): The stock ticker symbol.
    
    Returns:
        str: Summary of fundamental metrics (stubbed).
    """
    return f"Fundamentals stub for {ticker}."
    

class Toolkit:
    """
    Toolkit class aggregating all external data tools used by analyst nodes
    and the ToolNode in the workflow.
    """
    def __init__(self):
        self.get_yfinance_data = get_yfinance_data
        self.get_finnhub_news = get_finnhub_news
        self.get_social_media_sentiment = get_social_media_sentiment
        self.get_fundamental_analysis = get_fundamental_analysis
