import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_stock_news(stock_name):
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": stock_name,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "ok":
        print(data)
        return []

    articles = data.get("articles", [])

    if not articles:
        return []

    return articles
