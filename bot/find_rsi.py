# Python base libs
import os

# Installed libs
import pandas as pd
from dotenv import load_dotenv
from pybit.unified_trading import HTTP
from ta.momentum import RSIIndicator

# Custom files
from constants import RSI_PERIOD

load_dotenv()
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
session = HTTP(testnet=False, api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)


def fetch_klines(symbol, interval):
    try:
        response = session.get_kline(category="spot", symbol=symbol, interval=interval, limit=RSI_PERIOD)
        # print(response)
        if response["retCode"] == 0 and "list" in response["result"]:
            return response["result"]["list"]
        else:
            print("Error in response:", response["retMsg"])
            return None
    except Exception as e:
        print("Error fetching klines:", e)
        return None


def calculate_rsi(data):
    if not data or len(data) == 0:
        print("No data to calculate RSI.")
        return None

    # Extract the 'close' prices from the data
    closes = [float(item[4]) for item in data]
    df = pd.DataFrame(closes, columns=["close"])

    rsi = RSIIndicator(df["close"], RSI_PERIOD).rsi()
    return rsi.iloc[-1]
