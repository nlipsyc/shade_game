import abc


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

    def get_claimable_cells(self):
        claimable_cells = []
        claimable_columns = range(0, self.w, self.shade_size + 1)

        for row in range(self.h):
            for col in claimable_columns:
                claimable_cells.append((col, row))

        return claimable_cells
