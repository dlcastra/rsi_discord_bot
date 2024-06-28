# Python base libs
import os

# Installed libs
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv

# Custom files
from constants import SYMBOL, HOUR_INTERVAL, OVERBOUGHT_THRESHOLD, OVERSOLD_THRESHOLD, RSI_PERIOD
from find_rsi import calculate_rsi, fetch_klines

""" ------ ENV ------ """
load_dotenv()
DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")
CHANNEL_ID: int = int(os.getenv("CHANNEL_ID"))

""" ------ MAIN LOGIC FUNCTIONS ------ """
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)


async def background():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Test")


async def check_rsi() -> str or None:
    """
    Calculates what the RCI number is and then specifies an action for the bot
    :return str if found klines
    :return None if no klines found
    """
    klines: list = fetch_klines("spot", SYMBOL, HOUR_INTERVAL, RSI_PERIOD)
    if klines is None:
        print("Failed to fetch k-lines data.")
        return

    rsi_value: float = calculate_rsi(klines)
    print(rsi_value)
    if rsi_value is None:
        print("Failed to calculate RSI.")
        return

    try:
        channel = client.get_channel(CHANNEL_ID)
        if rsi_value > OVERBOUGHT_THRESHOLD:
            await channel.send(f"RSI is over {OVERBOUGHT_THRESHOLD}: {rsi_value}")
        elif rsi_value < OVERSOLD_THRESHOLD:
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
    await check_rsi()
    scheduled_check_rsi.start()


client.run(DISCORD_TOKEN)
