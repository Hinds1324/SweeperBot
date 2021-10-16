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


#######################################################################################################################
# Commands

# Note about default command arguments: Some command arguments will be set to have a default value of None. When this
# is the case, this doesn't mean that the default value of the argument should be thought of as None. Rather, this
# indicates that the argument is optional, and when the function receives None as an argument, this only represents that
# the particular argument has not been entered by the user, and it's up to the command function to decide what to do
# with that information.


@bot.command(name="generate", aliases=["g"], help="Generate a game of Minesweeper.")
async def generate(ctx, width: int = None, height: int = None, mines: int = None):
    await sweeperbot.generate(ctx, width, height, mines)


#######################################################################################################################
# Run the bot

bot.run(TOKEN)
