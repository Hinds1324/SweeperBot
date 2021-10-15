# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
from minesweeper import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="sw?")
last_user_inputs = {}


def get_last_user_input(user, key):
    input_dict = last_user_inputs.get(user)
    if input_dict is None: return
    else: return input_dict.get(key)


def set_last_user_input(user, key, value):
    input_dict = last_user_inputs.get(user) or {}
    input_dict[key] = value
    last_user_inputs[user] = input_dict


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name="generate", aliases=["g"], help="Generate a game of Minesweeper.")
async def generate(ctx, width: int = 0, height: int = 0, mines: int = 0):
    author = ctx.author

    # If the user doesn't pass an argument for width, height, or mines, then use the value they used last time they
    # executed the command. If they haven't executed the command before, then use the default values (8, 8, 12).
    width = width or get_last_user_input(author, "width") or 8
    height = height or get_last_user_input(author, "height") or 8
    mines = mines or get_last_user_input(author, "mines") or 12

    set_last_user_input(author, "width", width)
    set_last_user_input(author, "height", height)
    set_last_user_input(author, "mines", mines)

    try:
        mb = MinesweeperBoard(width, height, mines)
    except UnplayableBoardError:
        # TODO: Seems like the exception is caught by the bot client before it's caught here? I don't know if that's
        #  what's actually happening but yeah. Basically I don't know how I'm supposed to handle my own exceptions
        #  because the message I'm trying to send here never gets sent.
        await ctx.send("Cannot create a playable board with these parameters. Try reducing the number of mines or increasing the dimensions of the board.")
        return

    mb.uncover(width // 2, height // 2)

    tile_strings = [
        "<:tile0:540918716586655744>",
        "<:tile1:540918716632924181>",
        "<:tile2:540918716624535552>",
        "<:tile3:540918716460826672>",
        "<:tile4:540918716163162134>",
        "<:tile5:540918716595044352>",
        "<:tile6:540918716674736148>",
        "<:tile7:540918716599107584>",
        "<:tile8:540918716649701406>",
        "<:tilem:540918716809084938>"
    ]
    response = f"[Mines: {mines}] \n" \
               f"{mb.get_board_string(tile_strings, 2)}"

    if len(response) > 2000:
        await ctx.send("This board takes up too many characters. Try reducing the dimensions of the board.")
    else:
        await ctx.send(response)


bot.run(TOKEN)
