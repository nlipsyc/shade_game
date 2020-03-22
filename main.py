import abc

MAX_SHADE = 4

# Set up ownership and claimability next
# How will we identify players? Do they need their own object, or just a string?
# We should probably set claimable when initializing...


class PermissionError(Exception):
    def __init__(self, coordinates, player):
        self.coordinates = coordinates
        self.player = player

    def __str__(self):
        return f"PermissionError: Player {player} attempted to illegally toggle cell at {coordinates}"


class Cell(object):
    """Represents a single solar cell on our game board."""

    def __init__(self, coordinates):
        self.is_angled = False
        self.is_shaded = False
        self.coordinates = coordinates
        self.claimable = True
        self.claimed_by = None

    def __repr__(self):
        return "<Cell({})>".format(self.coordinates)

    def toggle_angle(self, player=None):
        """Toggle the angle of this solar cell.
        If claimable, anyone can toggle the angle and then claim it for themselves.
        If not claimable, only the owner may toggle the cell.
        """
        if self.claimed_by != player and not self.claimable:
            return PermissionError(self.coordinates, player)
        else:
            self.is_angled = not self.is_angled
            self.claimed_by = player
            return self.is_angled

    def draw(self):
        angle_representation = "↖" if self.is_angled else "_"
        # Shaded/unshaded
        shade_representation = "☁️" if self.is_shaded else "☀️"
        return f"[{angle_representation} | {shade_representation}]"


class AbstractGame(abc.ABC):
    """Represents game state and the physical game board."""

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.game_board = self.create_game_board()
        self.player_0_score = 0
        self.player_1_score = 0
        self._sun_angle = MAX_SHADE

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
            try:
                current_cell = self.game_board[x + i][y]
                current_cell.is_shaded = True
                cells_affected.append(current_cell)
            except IndexError:
                # The current shaddow is being cast at least partially off of the board
                pass

        return cells_affected

    def draw_game(self):
        rows = [[] for i in range(self.h)]

        for row in range(self.h):
            for column in self.game_board:
                rows[row].append(column[row].draw())

        for row in rows:
            print(row)
            print("\n")

    def apply_shade(self):
        """Calculate shade for all cells in the game board."""

        # Lets go over each cell, left-to-right, top-to-bottom
        for i, column in enumerate(self.game_board):
            for j, row in enumerate(column):
                cell = self.game_board[i][j]

                if cell.is_angled:
                    # We've found a cell that is casting a shade
                    self._cast_shaddow((i, j))

    def attempt_move(self, coordinates, player):
        x, y = coordinates
        try:
            self.game_board[x][y].toggle_angle(player=player)
            self.apply_shade()
            player_0_round_score, player_1_round_score = self.calculate_score()
            self.player_0_score += player_0_round_score
            self.player_1_score += player_1_round_score

            return True
        except PermissionError:
            # Handle cases where we try to claim an unclaimable square
            return False

    def calculate_score(self):
        """Return a tuple of both players' scores based on the current game board."""
        player_0_score = 0
        player_1_score = 0
        for row in range(self.h):
            for column in self.game_board:
                cell = column[row]

                if cell.claimed_by == 0 and not cell.is_shaded:
                    player_0_score += 1
                elif cell.claimed_by == 1 and not cell.is_shaded:
                    player_1_score += 1

        return (player_0_score, player_1_score)


class FreeForAllGame(AbstractGame):
    """All cells are claimable by defaultt, so no need to change anything here."""

    pass


# game = FreeForAllGame(8, 8)
# game.game_board[0][0].toggle_angle(player=0)
# game.apply_shade()

# game.draw_game()

# print(game.calculate_score())

game = FreeForAllGame(8, 8)
game.attempt_move((3, 4), 0)
game.attempt_move((4, 4), 1)
game.apply_shade()

game.draw_game()
print(game.calculate_score())
