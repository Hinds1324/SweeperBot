from sweeperbot.user_inputs import *
from minesweeper import *


# List of custom emojis that represent Minesweeper tiles.
custom_tile_strings = [
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

# List of default emojis that represent Minesweeper tiles. These are used in case we can't use the custom emojis.
default_tile_strings = [
        "◼", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "💣"
    ]


async def generate(ctx, width: int = 0, height: int = 0, mines: int = 0):
    author = ctx.author

    # If the user doesn't pass an argument for width, height, or mines, then use the value they used last time they
    # executed the command. If they haven't executed the command before, then use the default values (8, 8, 12).
    width = resolve_input(author, "width", width, 8)
    height = resolve_input(author, "height", height, 8)
    mines = resolve_input(author, "mines", mines, 12)

    # Create the board using the given parameters.
    try:
        mb = MinesweeperBoard(width, height, mines)
    except UnplayableBoardError:
        # TODO: Seems like the exception is caught by the bot client before it's caught here? I don't know if that's
        #  what's actually happening but yeah. Basically I don't know how I'm supposed to handle my own exceptions
        #  because the message I'm trying to send here never gets sent.
        await ctx.send("Cannot create a playable board with these parameters. Try reducing the number of mines or increasing the dimensions of the board.")
        return

    # Uncover the central tile of the board (essentially, perform the first click for the user) and generate
    # a board string.
    mb.uncover(width // 2, height // 2)
    board_string = mb.get_board_string(custom_tile_strings, 2)
    response = f"[Mines: {mines}] \n" \
               f"{board_string}"

    # If the response is over 2000 characters, try using the default emojis to display the board instead.
    if len(response) > 2000:
        board_string = mb.get_board_string(default_tile_strings, 2)
        response = f"[Mines: {mines}] \n" \
                   f"{board_string}"

    # If the response is STILL over 2000 characters, there's nothing we can do.
    if len(response) > 2000:
        await ctx.send("This board takes up too many characters. Try reducing the dimensions of the board.")
        return

    # If all goes well, display the board as a chat message.
    await ctx.send(response)
