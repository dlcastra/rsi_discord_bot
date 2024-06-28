# Python base libs
import os

# Installed libs
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv

# Custom files
from constants import SYMBOL, INTERVAL, OVERBOUGHT_THRESHOLD, OVERSOLD_THRESHOLD
from find_rsi import calculate_rsi, fetch_klines

""" ------ ENV ------ """
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

""" ------ MAIN LOGIC FUNCTIONS ------ """
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)


async def check_rsi():
    klines = fetch_klines(SYMBOL, INTERVAL)
    if klines is None:
        print("Failed to fetch k-lines data.")
        return

    rsi_value = calculate_rsi(klines)
    print(rsi_value)
    if rsi_value is None:
        print("Failed to calculate RSI.")
        return

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        if rsi_value > OVERBOUGHT_THRESHOLD:
            await channel.send(f"RSI is over {OVERBOUGHT_THRESHOLD}: {rsi_value}")
        elif rsi_value < OVERSOLD_THRESHOLD:
            await channel.send(f"RSI is below {OVERSOLD_THRESHOLD}: {rsi_value}")
    else:
        print(f"Channel with ID {CHANNEL_ID} not found.")


@tasks.loop(hours=1)
async def scheduled_check_rsi():
    await check_rsi()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await check_rsi()
    scheduled_check_rsi.start()


client.run(DISCORD_TOKEN)
