import pandas as pd
import pandas_ta as ta  # make sure pandas_ta is installed

def add_indicators(df):
    # Safe RSI
    try:
        rsi = ta.rsi(df['Close'], length=14)
        if rsi is not None and not rsi.empty:
            df['RSI'] = rsi
        else:
            df['RSI'] = None
    except Exception:
        df['RSI'] = None

    # Safe MACD
    try:
        macd = ta.macd(df['Close'])
        if macd is not None and not macd.empty:
            df = df.join(macd)
        else:
            df['MACD_12_26_9'] = None
    except Exception:
        df['MACD_12_26_9'] = None

    # Safe SMA and EMA
    try:
        sma = ta.sma(df['Close'], length=20)
        df['SMA_20'] = sma if sma is not None and not sma.empty else None
    except Exception:
        df['SMA_20'] = None

    try:
        ema = ta.ema(df['Close'], length=20)
        df['EMA_20'] = ema if ema is not None and not ema.empty else None
    except Exception:
        df['EMA_20'] = None

    return df
