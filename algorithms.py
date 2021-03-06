import abc
import random

import constants
from cell_calculators import (
    AllCellCalculator,
    CellCalculator,
    MaxShadeCellCalculator,
    RandomOffsetMaxShadeCellCalculator,
)
from cursor_initializers import CursorInitializer, OriginCursorInitializer, RandomCursorInitializer
from move_proposers import MoveProposer, RandomMoveProposer, SystematicMoveProposer

# The move proposer is the new class type of what we were previously calling algorithms


class GameParamaters(object):
    """Config object that helps us ensure we have all needed game parameters when creating an algorithm."""

    # TODO This should be a dataclass

    def __init__(self, game_dimensions: list[int], shade_size):
        self.game_dimensions = game_dimensions
        self.shade_size = shade_size


class DefaultGameParameters(GameParamaters):
    def __init__(self):
        super().__init__(constants.GAME_SIZE, constants.SHADE_SIZE)


class AlgorithmParamaters(object):
    """Config object that helps us ensure we have all needed algorithm parameters when creating an algorithm.

    Algorithms are defined by 3 factors, the cells they are allowed to suggest (CellCalculator), the way they will
    choose which of the available cells they will start on (CursorInitializer), and the specific algorithm they use
    to determine which cell should be chosen next (MoveProposer).
    """

    # TODO This should be a dataclass

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
    def propose_move(self) -> tuple:
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
    def move_proposer(self):
        pass


class ConstructedAlgorithm(AbstractAlgorithm):
    """The canonical way to build up an algorithm.

    Other classes inhering from AbstractAlgorithm are done for demo/POC purposes.
    """

    def __init__(self, game_params, alg_params, seed=None):
        super().__init__(game_params, alg_params, seed=seed)
        cursor_initializer = self.cursor_initializer_class(self.claimable_cells)
        self.claimable_cells_cursor = cursor_initializer.get_cursor_initial_index()

    @property
    def claimable_cells(self):
        cell_calculator = self.cell_calculator_class(self._game_params)
        return cell_calculator.get_claimable_cells()

    @property
    def move_proposer(self):
        return self.move_proposer_class(self._game_params, self.claimable_cells, self.claimable_cells_cursor)

    def propose_move(self):
        """Propose the next move to attempt.

        MoveProposer.propose_move will return a cursor position
        """
        # In order to allow the cursor to start where the cursor suggests it should, we want to return the _current_
        # position and then advance the cursor to prepare for the next move.
        move_to_propose = self.claimable_cells[self.claimable_cells_cursor]

        new_cursor_position = self.move_proposer.propose_move()

        self.claimable_cells_cursor = new_cursor_position

        return move_to_propose


def algorithm_factory(
    alg_params: AlgorithmParamaters, game_params: GameParamaters = DefaultGameParameters(), seed: int = None
):
    # Maybe algorithms should maintain track of turns elapsed? Use that to feed other params?
    """Builds algorithms using packages of config options.  A set of configurations is need for the game itself as well
    as one for each algorithm (currently only supports single-alg creation).

    Currently these are the three elements required to make an algorithm, but if that expands, this is the place to add
    them into the pipeline.

    Moving forward, we can use this to build up algorithms from multiple other ones.
    """
    return ConstructedAlgorithm(game_params, alg_params, seed)


def random_algorithm_factory(seed=None) -> ConstructedAlgorithm:
    """Makes a completely random move given the game dimensions.

    Mostly just useful for a POC, but could also be used as a baseline to benchmark other algorithms.
    """
    alg_params = AlgorithmParamaters(AllCellCalculator, OriginCursorInitializer, RandomMoveProposer)

    return algorithm_factory(alg_params, seed=seed)


def systematic_max_shade_factory(seed=None) -> ConstructedAlgorithm:
    """Claimable spaces are columns 0 and 4. Starts at the origin and and goes through available spaces in order.

    This algorithm works in order but only makes moves in columns that have no chance of casting shade on a
    move it has already made.
    """
    alg_params = AlgorithmParamaters(MaxShadeCellCalculator, OriginCursorInitializer, SystematicMoveProposer)

    return algorithm_factory(alg_params, seed=seed)


def random_start_systematic_max_shade_factory(seed=None) -> ConstructedAlgorithm:
    """Claimable spaces are columns 0 and 4. Starts at a random cell and and goes through available spaces in order."""

    alg_params = AlgorithmParamaters(MaxShadeCellCalculator, RandomCursorInitializer, SystematicMoveProposer)

    return algorithm_factory(alg_params, seed=seed)


def random_start_random_offset_max_shade_factory(seed=None) -> ConstructedAlgorithm:
    """Claimable spaces are 2 random columns spaced MAX_SHADE apart. Starts at a random cell and and goes through available spaces in order."""

    alg_params = AlgorithmParamaters(RandomOffsetMaxShadeCellCalculator, RandomCursorInitializer, RandomMoveProposer)

    return algorithm_factory(alg_params, seed=seed)


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
