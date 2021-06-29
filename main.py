# main.py
import os
import random
import time
import re
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions
from bs4 import BeautifulSoup
import cryptocompare
import json
from discord.utils import find

intents = discord.Intents.default()
intents.members = True



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!')



bot.load_extension("cogs.trading")
bot.load_extension("cogs.crypto_price")

bot.run(TOKEN)
