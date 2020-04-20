import abc
import random


class AbstractAlgorithm(abc.ABC):
    def __init__(self, game_dimensions, shade_size, seed=None):
        self.w, self.h = game_dimensions
        self.shade_size = shade_size

        # Allow passing in a seed to our algorithms to allow for consistent testing
        # None or no argument seeds from current time or from an operating system specific randomness source
        random.seed(a=seed)

    @abc.abstractmethod
    def propose_move(self):
        """Propose a move to Game.attempt_move().
        This takes the form of tuple(x, y)

        If it is a legal move, attempt_move will return True our flow is done.
        If it is an illegal move, attempt_move will return False and we will try again with a different move.
        """
        pass


class RandomAlgorithm(AbstractAlgorithm):
    """Makes a completely random move given the game dimensions.

    Mostly just useful for a POC, but could also be used as a baseline to benchmark other algorithms.
    """

    def propose_move(self):

        x_move = random.randrange(self.w)
        y_move = random.randrange(self.h)

        return (x_move, y_move)


class SystematicMaxShade(AbstractAlgorithm):
    """Claimable spaces are columns 0 and 4. Random start point and go through in order.

    When we initialize the algorithm, we determine all claimable cells into a list an pick a cell that we will start at.
    After that we go through them systematically trying to claim the next one and advancing our cursor.
    """

    def __init__(self, game_dimensions, shade_size, seed=None):
        super().__init__(game_dimensions, shade_size, seed=seed)

        self._claimable_columns = [i for i in range(0, self.w, self.shade_size + 1)]

        self.claimable_cells = []
        for col in self._claimable_columns:
            for row in range(self.h):
                self.claimable_cells.append((col, row))

        self.claimable_cells_cursor = random.randint(0, len(self.claimable_cells) - 1)

    def propose_move(self):
        try:
            self.claimable_cells_cursor += 1
            return self.claimable_cells[self.claimable_cells_cursor]

        except IndexError:
            # We hit the end of our list, let's loop back around
            self.claimable_cells_cursor = 0
            return self.claimable_cells[self.claimable_cells_cursor]


"""
Systematic max shade
Claimable spaces are columns 0 and 4. Random start point and go through in order

Random max shade
Claimable spaces are columns 0 and 4. Random start point and go in random order

Systematic efficient
Claimable spaces are columns 0-MAX_SHADE and <- + 4. Random start point and go in order

Random efficient
Claimable spaces are columns 0-MAX_SHADE and <- + 4. Random start point and go in random order

Random
RandX RandY
"""
