import pytest
from game import FreeForAllGame


@pytest.fixture
def mock_game():
    return FreeForAllGame(8, 8)


def test_game_initialization():
    width = 8
    height = 8
    free_for_all_game = FreeForAllGame(width, height)

    assert free_for_all_game.w is width
    assert free_for_all_game.h is height


def test_attempt_move_is_valid(mock_game):
    """Should return True, toggle the board state, and claim the cell for player 0."""
    attempted_move = mock_game.attempt_move((4, 3), 0)

    assert attempted_move is True
    assert mock_game.game_board[4][3].is_angled is True
    assert mock_game.game_board[4][3].claimed_by == 0


def test_attempt_move_is_invalid(mock_game):
    """Should return False and not toggle the board state given a invalid move."""
    mock_game.game_board[4][3].claimable = False
    attempted_move = mock_game.attempt_move((4, 3), 0)

    assert attempted_move is False
    assert mock_game.game_board[4][3].is_angled is False
    assert mock_game.game_board[4][3].claimed_by is None


def test_calculate_score_shade_handling(mock_game):
    """Should not score a shaded cell."""
    mock_game.attempt_move((3, 4), 0)
    # This cell is in shade now
    mock_game.attempt_move((4, 4), 1)

    mock_game.apply_shade()

    # Player 0 should be blocking player 1 from scoring
    score = mock_game.calculate_score()
    assert score == (1, 0)


def test_calculate_score_claimed_by_handling(mock_game):
    """Should assign score to the last player to interact with a cell."""
    mock_game.attempt_move((3, 4), 0)
    mock_game.attempt_move((3, 4), 1)

    mock_game.apply_shade()

    score = mock_game.calculate_score()
    assert score == (0, 1)
