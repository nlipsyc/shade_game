import abc
import random


class MoveProposer(abc.ABC):
    """Proposes a cursor index that will be used to make the next move.

    The move proposer is not responsible for determing if a move is valid.  Its sole responsibility is advancing the
    cursor based on its internal logic.
    """

    def __init__(self, game_params, claimable_cells: list, cursor_index: int):
        self._game_params = game_params
        self._claimable_cells = claimable_cells
        self._count_of_claimable_cells = len(self._claimable_cells)
        self._cursor_index = cursor_index

    @abc.abstractmethod
    def propose_move(self) -> int:
        pass


class RandomMoveProposer(MoveProposer):
    """Proposes a random move.

    Because all moves are random and independent of the previous one, we don't need to use the initial cursor index.
    """

    def propose_move(self) -> int:
        return random.choice(range(self._count_of_claimable_cells))


class SystematicMoveProposer(MoveProposer):
    """Proposes all given cells in order, starting at the supplied cursor index."""

    # Claimable cells should work, but the docstring needs updating to reflect the variability introduced by the
    # injected column calculator
    def propose_move(self) -> int:
        self._cursor_index += 1

        if self._cursor_index == self._count_of_claimable_cells:
            # We've hit the end of our list, looping back around
            self._cursor_index = 0

        return self._cursor_index
