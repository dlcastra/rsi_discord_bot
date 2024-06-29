# Python base libs
import os

# Installed libs
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

# Custom files
from constants import SYMBOL, HOUR_INTERVAL, OVERBOUGHT_THRESHOLD, OVERSOLD_THRESHOLD, RSI_PERIOD
from find_rsi import calculate_rsi, fetch_klines

""" ------ ENV ------ """
load_dotenv()
DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")
CHANNEL_ID: str = os.getenv("CHANNEL_ID")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

""" ------ SETTINGS ------ """
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)
session = HTTP(testnet=False, api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)

""" ------ BOT LOGIC FUNCTIONS ------ """


async def check_rsi() -> str or None:
    """
    Calculates what the RCI number is and then specifies an action for the bot
    :return str if found klines
    :return None if no klines found
    """
    klines: list = fetch_klines(session, "spot", SYMBOL, HOUR_INTERVAL, RSI_PERIOD)
    if klines is None:
        print("Failed to fetch klines data.")
        return

    rsi_value: float = calculate_rsi(klines, RSI_PERIOD)
    print(rsi_value)
    if rsi_value is None:
        print("Failed to calculate RSI.")
        return

    try:
        channel = client.get_channel(int(CHANNEL_ID))
        if rsi_value >= OVERBOUGHT_THRESHOLD:
            await channel.send(f"RSI is over {OVERBOUGHT_THRESHOLD}: {rsi_value}")
        elif rsi_value <= OVERSOLD_THRESHOLD:
            await channel.send(f"RSI is below {OVERSOLD_THRESHOLD}: {rsi_value}")
    except Exception as e:
        print("Error to get channel:", e)
        return None


@tasks.loop(hours=1)
async def scheduled_check_rsi():
    await check_rsi()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    scheduled_check_rsi.start()


client.run(DISCORD_TOKEN)
