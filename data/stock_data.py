import yfinance as yf

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="6mo")

        if df.empty:
            return None, None

        info = {
            "longName": ticker.replace(".NS", "")
        }

        return df, info

    except Exception as e:
        print("Stock fetch error:", e)
        return None, None
