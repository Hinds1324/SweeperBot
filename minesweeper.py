import random

class TooManyMinesError(Exception):
    pass


class MinesweeperTile:
    def __init__(self):
        """
        Create a Minesweeper tile that is part of a Minesweeper board.
        """
        self.is_covered = True
        self.is_mine = False
        self.value = 0


class MinesweeperBoard:
    def __init__(self, width, height, mines):
        """
        Create a Minesweeper board.
        :param width: The width of the board.
        :param height: The height of the board.
        :param mines: The number of mines on the board.
        """
        self.width = width
        self.height = height
        self.mines = mines
        self.board = [MinesweeperTile() for _ in range(width * height)]
        self.is_fresh_board = True

    def __str__(self):
        return self.get_board_string()

    def is_within_board(self, x, y):
        """
        Checks that the coord (x,y) is not outside the board.
        """
        return (0 <= x < self.width) and (0 <= y < self.height)

    def get_tile_at(self, x, y):
        """
        Returns the tile object located at the coord (x,y) on the board.
        """
        return self.board[self.height * y + x]

    def board_coords(self):
        """
        Generator that yields coords for every tile on the board.
        """
        for x in range(self.width):
            for y in range(self.height):
                yield (x, y)

    def adjacent_coords(self, x, y):
        """
        Generator that yields all coords on the board adjacent to (x,y), including (x,y) itself.
        """
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                current_coord = (x + i, y + j)
                if self.is_within_board(*current_coord):
                    yield current_coord

    def uncover(self, x, y):
        """
        Uncover the tile located and x,y on the board. If this is the first tile to be uncovered,
        then also generate the rest of the mines on the board.
        """
        selected_tile = self.get_tile_at(x, y)

        ### If the tile is already uncovered we shouldn't try to uncover it again.
        if not selected_tile.is_covered: return

        ### If this is the first tile to be uncovered, we need to generate the board.
        if self.is_fresh_board:
            self.generate_mines(x, y)
            self.is_fresh_board = False

        ### Uncover the selected tile.
        selected_tile.is_covered = False

        ### If we uncover a blank tile (a tile with 0 mines near it), then we should automatically
        ### uncover all of its adjacent tiles.
        if selected_tile.value == 0:
            for i, j in self.adjacent_coords(x, y):
                if not (i == j == 0): self.uncover(i, j)

        return selected_tile

    def generate_mines(self, uncover_x, uncover_y):
        """
        Generates all mines on the board after the first mine is uncovered. No mines will be placed inside the 3x3
        box centered around the uncovered tile.
        """
        ### Generate mines.
        # Create a list of all tiles on the board excluding all tiles within the 3x3 box centered around the uncovered tile.
        tiles_list = [self.get_tile_at(x, y) for x, y in self.board_coords()
                      if not (x, y) in self.adjacent_coords(uncover_x, uncover_y)]
        for i in range(self.mines):
            if tiles_list == []:
                raise TooManyMinesError("Cannot create a playable board with these parameters. Try reducing the number of mines or increasing the dimensions of the board.")
            
            new_mine = random.choice(tiles_list)
            new_mine.is_mine = True
            tiles_list.remove(new_mine)

        ### Assign values to each tile.
        for x, y in self.board_coords():
            current_tile = self.get_tile_at(x, y)
            for i, j in self.adjacent_coords(x, y):
                if self.get_tile_at(i, j).is_mine: current_tile.value += 1

    def get_board_string(self, tile_strings=["0 ", "1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "X ", ". "], covered_tiles_mode=0, spoilers=("||","||")):
        """
        Returns a string representation of the board, where each of the different types of tiles
        (Tiles with values 0, 1, 2, ... 8, and mine tiles) are represented by the strings given in
        tile_strings.

        A tile whose value is n is represented by tile_strings[n], and mine tiles are represented
        by tile_strings[9].

        If a tile is covered, then the covered_tiles_mode parameter allows the user to customise how these tiles
        should be displayed. The following modes are available:

        covered_tiles_mode = 0: Covered tiles are hidden, and represented by the string in tile_strings[10].

        covered_tiles_mode = 1: Covered tiles are shown as if they were uncovered.

        covered_tiles_mode = 2: Covered tiles are wrapped in spoiler tags as defined in the spoilers parameter.
        By default, these spoiler tags are set to be the spoiler tags used by Discord.
        """
        return_string = ""

        for y in range(self.height):
            current_row = ""
            for x in range(self.width):
                tile = self.get_tile_at(x, y)
                tile_string = ""

                if tile.is_mine: tile_string = tile_strings[9]
                else: tile_string = tile_strings[tile.value]

                if tile.is_covered:
                    if covered_tiles_mode == 0: tile_string = tile_strings[10]
                    elif covered_tiles_mode == 2: tile_string = spoilers[0] + tile_string + spoilers[1]

                current_row += tile_string

            return_string += current_row + ("\n" if y < self.height - 1 else "")

        return return_string
