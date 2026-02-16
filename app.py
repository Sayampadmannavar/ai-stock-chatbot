import streamlit as st
import plotly.graph_objects as go
from data.stock_data import get_stock_data
from analysis.technicals import add_indicators
from analysis.sentiment import get_news_sentiment
from utils.llm import ask_ai

st.set_page_config(layout="wide")
st.title("📈 Free AI Stock Market Chatbot")

ticker = st.text_input("Enter NSE Stock (e.g., RELIANCE)")

if ticker:
    if not ticker.endswith(".NS"):
        ticker = ticker.upper() + ".NS"

    # Get stock data
    df, info = get_stock_data(ticker)

    if df is None or df.empty:
        st.error("Invalid stock symbol or no price data available")
        st.stop()

    df = add_indicators(df)

    # 💰 Show price first (safe)
    if 'Close' not in df or df['Close'].isnull().all():
        st.error("No price data available for this stock")
        st.stop()

    latest_price = float(df['Close'].iloc[-1])
    previous_price = float(df['Close'].iloc[-2]) if len(df) > 1 else latest_price

    change = latest_price - previous_price
    percent_change = (change / previous_price) * 100 if previous_price != 0 else 0

    st.subheader(f"💰 Current Price: ₹{latest_price:.2f}")

    if change > 0:
        st.success(f"▲ {percent_change:.2f}% today")
    else:
        st.error(f"▼ {percent_change:.2f}% today")

    # 📊 Candlestick Chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    ))

    st.plotly_chart(fig, width='stretch')

    # Indicators (safe display)
    st.subheader("📊 Indicators")
    st.write("RSI:", round(df['RSI'].iloc[-1], 2) if df['RSI'].iloc[-1] is not None else "N/A")
    st.write("MACD:", round(df['MACD_12_26_9'].iloc[-1], 2) if df['MACD_12_26_9'].iloc[-1] is not None else "N/A")
    st.write("SMA 20:", round(df['SMA_20'].iloc[-1], 2) if df['SMA_20'].iloc[-1] is not None else "N/A")
    st.write("EMA 20:", round(df['EMA_20'].iloc[-1], 2) if df['EMA_20'].iloc[-1] is not None else "N/A")

    # 📰 News Sentiment
    st.subheader("📰 News Sentiment")
    sentiment = get_news_sentiment(ticker.replace(".NS", ""))
    st.write(sentiment)

    # 🤖 Ask AI Section
    st.subheader("🤖 Ask AI about this stock")
    user_question = st.text_input("Type your question")

    if user_question:
        prompt = f"""
Stock: {ticker}
Current Price: {latest_price}
RSI: {df['RSI'].iloc[-1]}
MACD: {df['MACD_12_26_9'].iloc[-1]}
SMA 20: {df['SMA_20'].iloc[-1]}
EMA 20: {df['EMA_20'].iloc[-1]}
Sentiment: {sentiment}

Question: {user_question}
"""
        answer = ask_ai(prompt)
        st.write(answer)
