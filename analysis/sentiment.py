import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news_sentiment(ticker):
    try:
        url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}&pageSize=5"
        response = requests.get(url)
        data = response.json()
        if data.get("status") != "ok" or not data.get("articles"):
            return "No recent news found"
        news_list = [f"{article['title']} ({article['source']['name']})" for article in data['articles']]
        return "\n".join(news_list)
    except Exception as e:
        return f"❌ News API Error: {str(e)}"
