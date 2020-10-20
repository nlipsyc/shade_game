import abc
import random


class MoveProposer(abc.ABC):
    """Proposes a the cursor index that will be used to make the next move.

    The move proposer is not responsible for determing if a move is valid.  Its sole responsibility is advancing the
    cursor based on its internal logic.
    """

    def __init__(self, game_params, claimable_cells: list, cursor_index: int):
        self._game_params = game_params
        self._claimable_cells = claimable_cells
        self._cursor_index = cursor_index

    @abc.abstractmethod
    def propose_move(self):
        pass


class RandomMoveProposer(MoveProposer):
    def propose_move(self):
        return random.choice(self._claimable_cells)
