import abc


class CursorInitializer(abc.ABC):
    """Determines the starting index of an algorithm's cursor."""

    def __init__(self, claimable_cells):
        self.claimable_cells = claimable_cells

    @abc.abstractmethod
    def get_cursor_initial_index(self):
        pass


class OriginCursorInitializer(CursorInitializer):
    """Initializes our cursor at the first claimable cell of the first row.

    TODO Test me! I don't trust this
    TODO This breaks if the first row is unclaimable.  Handle that edge case when we get to it.
    """

    def get_cursor_initial_index(self):
        return self.claimable_cells[0]
