# Python base libs

# Installed libs
import pandas as pd
from ta.momentum import RSIIndicator

# Custom files
from constants import RSI_PERIOD


def fetch_klines(session, category: str, symbol: str, interval: int, limit: int) -> list or None:
    try:
        response = session.get_kline(category=category, symbol=symbol, interval=interval, limit=limit)
        if response["retCode"] == 0 and "list" in response["result"]:
            return response["result"]["list"]
        else:
            print("Error in response:", response["retMsg"])
            return None

    except Exception as e:
        print("Error fetching klines:", e)
        return None


def calculate_rsi(data: list) -> float or None:
    if not data or len(data) == 0:
        print("No data to calculate RSI.")
        return None

    # Extract the 'close' prices from the data
    closes = [float(item[4]) for item in data]
    df = pd.DataFrame(closes, columns=["close"])

    rsi = RSIIndicator(df["close"], RSI_PERIOD).rsi()
    return rsi.iloc[-1]
