import abc


class CursorInitializer(abc.ABC):
    """Determines the starting index of an algorithm's cursor."""

    def __init__(self, claimable_cells):
        self.claimable_cells = claimable_cells

    @abc.abstractmethod
    def get_cursor_initial_index(self) -> int:
        pass


class OriginCursorInitializer(CursorInitializer):
    """Initializes our cursor at the first claimable cell of the first claimable row."""

    def get_cursor_initial_index(self) -> int:
        return 0
