import os
import sweeperbot
from discord.ext import commands
from dotenv import load_dotenv


# Read bot token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create an instance of the bot client
bot = commands.Bot(command_prefix="sw?")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name="generate", aliases=["g"], help="Generate a game of Minesweeper.")
async def generate(ctx, width: int = 0, height: int = 0, mines: int = 0):
    await sweeperbot.generate(ctx, width, height, mines)


bot.run(TOKEN)
