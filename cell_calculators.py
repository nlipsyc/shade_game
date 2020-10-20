import abc


class CellCalculator(abc.ABC):
    """Determines which cells on the board can be claimed by our algorithm. """

    def __init__(self, game_params):
        self.game_dimensions = game_params.game_dimensions
        self.shade_size = game_params.shade_size

    @abc.abstractmethod
    def get_claimable_cells(self) -> list[tuple[int, int]]:
        """Retruns a one dimensional list of tuples representing the ordered coordinates of the cells."""
        pass


class AllCellCalculator(CellCalculator):
    """All cells on the board can be claimed."""

    def get_claimable_cells(self):
        claimable_cells = []
        h, w = self.game_dimensions
        for row in range(h):
            for col in range(w):
                claimable_cells.append((col, row))

        return claimable_cells
