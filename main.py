class Cell(object):
    def __init__(self, coordinates):
        self.is_angled = False
        self.is_shaded = False
        self.coordinates = coordinates

    def __repr__(self):
        return "<Cell(Angled: {})>".format(self.is_angled)

    def toggle_angle(self):
        self.is_angled = not self.is_angled
        return self.is_angled


class Game(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.game_board = self.create_game_board()
        self._sun_angle = 4

    def __repr__(self):
        return "<Game({}, {})>".format(self.w, self.h)

    @property
    def sun_angle(self):
        """ The angle that the sun is at relative to the game board. It coresponds to the number of cells to the
        right that a cell is able to shade.

        The sun starts at its most oblique angle (sun_angle=3). As it moves through the day, closer to straight on
        to the game board, the block becomes less effective (sun_angle==1)

        Because the sun_angle has a min of 1, a cell can always block at least 1 cell next to it.
        """
        return self._sun_angle

    @sun_angle.setter
    def sun_angle(self, val):
        if val in range(1, 4):
            self._angle = val
        else:
            raise ValueError("Sun angle must be betewen 1-3")

    def create_column(self, column_number):
        column = []
        for row_number in range(self.w):
            column.append(Cell((row_number, column_number)))

        return column

    def create_game_board(self):
        game_board = []
        for column_number in range(self.h):
            game_board.append(self.create_column(column_number))
        return game_board

    def calculate_light_absorbed(self):
        pass

    def _clear_all_shaddows(self):
        """Sets `is_shaded` property of all cells on the game board to False

        This is a helper function that allows us to start each application of
        shade from a clean state.
        """
        for column in self.game_board:
            for cell in column:
                cell.is_shaded = False

    def _cast_shaddow(self, cell_location):
        """Takes a tuple representing the X/Y coordinates of a cell and
        applies shade to adjacent cells as dictated by the Game's sun_angle.
        """

        # TODO figure out why we aren't shading all the cells we should be.
        x, y = cell_location
        cells_affected = []
        for i in range(1, self.sun_angle + 1):
            current_cell = self.game_board[x][y]
            current_cell.is_shaded = True
            cells_affected.append(current_cell)

        return cells_affected

    # def apply_shade(self):
    #     """Calculate shade for all cells in the game board."""

    #     # Lets go over each cell, left-to-right, top-to-bottom
    #     for enumerate(row, i) in self.game_board:
    #         for enumerate(column, j) in row:
    #             cell = self.game_board[i][j]

    #             if cell.is_angled:
    #                 # We've found a cell that is casting a shade


game = Game(8, 8)
print("a")
game._cast_shaddow((0, 0))

for i in range(8):
    print(game.game_board[i][0].is_shaded)
