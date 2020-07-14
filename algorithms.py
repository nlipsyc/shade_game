import abc
import random

from typing import Tuple, List

# The move proposer is the new class type of what we were previously calling algorithms


class GameParamaters(object):
    """Config object that helps us ensure we have all needed game parameters when creating an algorithm."""

    def __init__(self, game_dimensions, shade_size):
        self.game_dimensions = game_dimensions
        self.shade_size = shade_size


class CellCalculator(abc.ABC):
    """Determines which cells on the board can be claimed by our algorithm"""

    def __init__(self, game_params):
        self.game_dimensions = game_params.game_dimensions
        self.shade_size = game_params.shade_size

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
    """Proposes a the cursor index that will be used to make the next move.

    The move proposer is not responsible for determing if a move is valid.  Its sole responsibility is advancing the
    cursor based on its internal logic.
    """

    # Might need python 3.8?
    def __init__(self, game_params: GameParamaters, claimable_cells: List, cursor_index: int):
        foo = 1
        self._game_params = game_params
        self._claimable_cells = claimable_cells
        self._cursor_index = cursor_index

    @abc.abstractmethod
    def propose_move(self):
        pass


class AlgorithmParamaters(object):
    """Config object that helps us ensure we have all needed algorithm parameters when creating an algorithm."""

    def __init__(
        self,
        cell_calculator_class: CellCalculator,
        cursor_initializer_class: CursorInitializer,
        move_proposer_class: MoveProposer,
    ):
        self.cell_calculator_class = cell_calculator_class
        self.cursor_initializer_class = cursor_initializer_class
        self.move_proposer_class = move_proposer_class


class AbstractAlgorithm(abc.ABC):
    def __init__(self, game_params, alg_params, seed=None):
        # Pass a seed to the RNG if it is provided
        random.seed(a=seed)

        self._game_params = game_params
        self._alg_params = alg_params

        # Convenience methods
        self.game_dimensions = game_params.game_dimensions
        self.shade_size = game_params.shade_size
        self.cell_calculator_class = alg_params.cell_calculator_class
        self.cursor_initializer_class = alg_params.cursor_initializer_class
        self.move_proposer_class = alg_params.move_proposer_class

    @abc.abstractmethod
    def propose_move(self) -> Tuple:
        """Propose a move to Game.attempt_move().
        This takes the form of tuple(x, y)

        If it is a legal move, attempt_move will return True our flow is done.
        If it is an illegal move, attempt_move will return False and we will try again with a different move.
        """
        pass

    @property
    @abc.abstractmethod
    def claimable_cells(self):
        pass

    @property
    @abc.abstractmethod
    def claimable_cells_cursor(self):
        pass

    @property
    @abc.abstractmethod
    def move_proposer(self):
        pass


# TODO Turn into subclass of cell calculator
def all_column_calculator(w, shade_size):
    """To maintain consistency, we need a column calculator for times when we don't want to restrict based on column."""

    claimable_columns = list(range(w))

    return claimable_columns


# TODO Turn into subclass of cell calculator
def random_regular_column_calculator(w, shade_size):
    """Sets the claimable columns to a random one and then spaces them out by 1 `shade_size`."""
    offset = random.randint(0, shade_size)
    claimable_columns = list((offset, w, shade_size + 1))

    return claimable_columns


# TODO Turn into subclass of cell calculator
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


class SystematicMoveProposer(MoveProposer):
    """Proposes a the claim and goes through the rest in order.

    The column_calculator determine all claimable cells. We then pick a cell that we will start at and that we go
    through them systematically trying to claim the next one and advancing our cursor.
    """

    # Claimable cells should work, but the docstring needs updating to reflect the variability introduced by the
    # injected column calculator
    def propose_move(self):
        try:
            self._cursor_index += 1
            return self._claimable_cells[self._cursor_index]

        except IndexError:
            # We hit the end of our list, let's loop back around
            self._cursor_index = 0
            return self._claimable_cells[self._cursor_index]


class ConstructedAlgorithm(AbstractAlgorithm):
    @property
    def claimable_cells(self):
        cell_calculator = self.cell_calculator_class(self._game_params)
        return cell_calculator.get_claimable_cells()

    @property
    def claimable_cells_cursor(self):
        cursor_initializer = self.cursor_initializer_class(self.claimable_cells)
        return cursor_initializer.get_cursor_initial_index()

    @property
    def move_proposer(self):
        return self.move_proposer_class(self._game_params)

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


def algorithm_factory(game_params: GameParamaters, alg_params: AlgorithmParamaters, seed=None):
    # Maybe algorithms should maintain track of turns elapsed? Use that to feed other params?
    """Builds algorithms using packages of config options.  A set of configurations is need for the game itself as well
    as one for each algorithm (currently only supports single-alg creation).

    Currently these are the three elements required to make an algorithm, but if that expands, this is the place to add
    them into the pipeline.

    Moving forward, we can use this to build up algorithms from multiple other ones.
    """
    return ConstructedAlgorithm(GameParamaters, AlgorithmParamaters, seed)


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
