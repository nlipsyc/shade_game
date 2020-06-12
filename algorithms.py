import abc
import random

# The move proposer is the new class type of what we were previously calling algorithms


class CellCalculator(abc.ABC):
    """Determines which cells on the board can be claimed by our algorithm"""

    def __init__(self, game_dimensions, shade_size):
        self.game_dimensions = game_dimensions
        self.shade_size = shade_size

    @abc.abstractmethod
    def get_claimable_cells(self):
        pass


class CursorInitializer(abc.ABC):
    """Determines the starting index of an algorithm's cursor."""

    def __init__(self, claimable_cells):
        self.claimable_cells = claimable_cells

    @abc.abstractmethod
    def get_cursor_initial_index(self):
        pass


class MoveProposer(abc.ABC):
    """Proposes a new cursor index that will be used to make a move."""

    @abc.abstractmethod
    def propose_move(self, claimable_cells, claimable_cells_cursor):
        pass


class AbstractAlgorithm(abc.ABC):
    def __init__(self, game_dimensions, shade_size, column_calculator, seed=None):
        self.w, self.h = game_dimensions
        self.shade_size = shade_size
        self._column_calculator = column_calculator
        # Allow passing in a seed to our algorithms to allow for consistent testing
        # None or no argument seeds from current time or from an operating system specific randomness source
        random.seed(a=seed)

    @property
    def _claimable_columns(self):
        return self.column_calculator(self.w, self.shade_size)

    @abc.abstractmethod
    def propose_move(self):
        """Propose a move to Game.attempt_move().
        This takes the form of tuple(x, y)

        If it is a legal move, attempt_move will return True our flow is done.
        If it is an illegal move, attempt_move will return False and we will try again with a different move.
        """
        pass


def all_column_calculator(w, shade_size):
    """To maintain consistency, we need a column calculator for times when we don't want to restrict based on column."""

    claimable_columns = list(range(w))

    return claimable_columns


def random_regular_column_calculator(w, shade_size):
    """Sets the claimable columns to a random one and then spaces them out by 1 `shade_size`."""
    offset = random.randint(0, shade_size)
    claimable_columns = list((offset, w, shade_size + 1))

    return claimable_columns


def efficient_regular_column_calculator(w, shade_size):
    """Sets the claimable columns to the leftmost one and then spaces them out by 1 `shade_size`.

    This minimizes the chance of any cell being shaded by the algorithm's own moves or the other's.
    """
    claimable_columns = list(range(0, w, shade_size + 1))

    return claimable_columns


class RandomAlgorithm(AbstractAlgorithm):
    """Makes a completely random move given the game dimensions.

    Mostly just useful for a POC, but could also be used as a baseline to benchmark other algorithms.
    """

    def propose_move(self):

        x_move = random.randrange(self.w)
        y_move = random.randrange(self.h)

        return (x_move, y_move)


class SystematicAlgorithm(MoveProposer):
    """Proposes a the claim and goes through the rest in order.

    The column_calculator determine all claimable cells. We then pick a cell that we will start at and that we go
    through them systematically trying to claim the next one and advancing our cursor.
    """

    # Claimable cells should work, but the docstring needs updating to reflect the variability introduced by the
    # injected column calculator
    def __init__(self, game_dimensions, shade_size, column_calculator, seed=None):
        super().__init__(game_dimensions, shade_size, column_calculator=column_calculator, seed=seed)

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


class ConstructedAlgorithm(AbstractAlgorithm):
    def __init__(
        self, game_dimensions, shade_size, cell_calculator_class, cursor_initializer_class, move_proposer_class, seed
    ):
        self.claimable_cells = cell_calculator_class(game_dimensions, shade_size).get_claimable_cells()

        self.claimable_cells_cursor = cursor_initializer_class(self.claimable_cells).get_cursor_initial_index
        self.move_proposer = move_proposer_class(game_dimensions, shade_size)

    def propose_move(self):
        """Propose the next move to attempt.

        MoveProposer.propose_move will return a cursor position
        """
        # In order to allow the cursor to start where the cursor suggests it should, we want to return the _current_
        # position and then advance the cursor to prepare for the next move.
        move_to_propose = self.claimable_cells[self.claimable_cells_cursor]

        new_cursor_position = self.move_proposer.propose_move(self.claimable_cells, self.claimable_cells_cursor)

        self.claimable_cells_cursor = new_cursor_position

        return move_to_propose


class GameParamaters(object):
    """Config object that helps us ensure we have all needed game parameters when creating an algorithm."""

    def __init__(self, game_dimensions, shade_size):
        self.game_dimensions = game_dimensions
        self.shade_size = shade_size


class AlgorithmParamaters(object):
    """Config object that helps us ensure we have all needed algorithm parameters when creating an algorithm."""

    def __init__(self, cell_calculator_class, cursor_initializer_class, move_proposer_class):
        self.cell_calculator_class = cell_calculator_class
        self.cursor_initializer_class = cursor_initializer_class
        self.move_proposer_class = move_proposer_class


def algorithm_factory(game_parameters, algorithm_paramaters, seed=None):
    # Maybe algorithms should maintain track of turns elapsed? Use that to feed other params?
    """Builds algorithms using packages of config options.  A set of configurations is need for the game itself as well
    as one for each algorithm (currently only supports single-alg creation).

    Currently these are the three elements required to make an algorithm, but if that expands, this is the place to add
    them into the pipeline.

    Moving forward, we can use this to build up algorithms from multiple other ones.
    """
    return ConstructedAlgorithm(
        game_parameters.game_dimensions,
        game_parameters.shade_size,
        algorithm_paramaters.cell_calculator_class,
        algorithm_paramaters.cursor_initializer_class,
        algorithm_paramaters.move_proposer_class,
        seed,
    )


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
