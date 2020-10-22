import abc

import random


class CellCalculator(abc.ABC):
    """Determines which cells on the board can be claimed by our algorithm. """

    def __init__(self, game_params):
        self.w, self.h = game_params.game_dimensions
        self.shade_size = game_params.shade_size

    @abc.abstractmethod
    def get_claimable_cells(self) -> list[tuple[int, int]]:
        """Retruns a one dimensional list of tuples representing the ordered coordinates of the cells."""
        pass


class AllCellCalculator(CellCalculator):
    """All cells on the board can be claimed."""

    def get_claimable_cells(self):
        claimable_cells = []
        for row in range(self.h):
            for col in range(self.w):
                claimable_cells.append((col, row))

        return claimable_cells


class MaxShadeCellCalculator(CellCalculator):
    """Claim all possible cells that we can guarantee will not case shade on each other."""

    def __init__(self, game_params, offset_seed=0):
        super().__init__(game_params)
        # This way we can give an arbitrarily large random number and make sure we're still getting the max shade
        self.offset = offset_seed % self.shade_size

    def get_claimable_cells(self):
        claimable_cells = []
        claimable_columns = range(0 + self.offset, self.w, self.shade_size + 1)

        for row in range(self.h):
            for col in claimable_columns:
                claimable_cells.append((col, row))

        return claimable_cells


class RandomOffsetMaxShadeCellCalculator(MaxShadeCellCalculator):
    """Instead of starting the MaxShadeCalculator at column 0, start it at a random column between 0 and SHADE_SIZE."""

    def __init__(self, game_params):
        offset_seed = random.randint(1, 1000)
        super().__init__(game_params, offset_seed=offset_seed)
