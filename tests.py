import unittest
from main import Cell, AbstractGame, FreeForAllGame


class TestGame(unittest.TestCase):
    def test_attempt_move_is_valid(self):
        """Should return True and toggle the board state given a valid move"""
        game = FreeForAllGame(8, 8)
        attempted_move = game.attempt_move((3, 4), 0)

        self.assertTrue(attempted_move)
        self.assertTrue(game.game_board[3][4].is_angled)
        self.assertEqual(game.game_board[3][4].claimed_by, 0)

    def test_attempt_move_is_invalid(self):
        """Should return False and not toggle the board state given a invalid move"""
        game = FreeForAllGame(8, 8)
        game.game_board[3][4].claimable = False
        attempted_move = game.attempt_move((3, 4), 0)

        self.assertFalse(attempted_move)
        self.assertFalse(game.game_board[3][4].is_angled)
        self.assertEqual(game.game_board[3][4].claimed_by, None)

    def test_calculate_score_shade_handling(self):
        """Should not score a shaded cell."""
        game = FreeForAllGame(8, 8)
        game.attempt_move((3, 4), 0)
        # This cell is in shade now
        game.attempt_move((4, 4), 1)

        game.apply_shade()

        # Player 0 should be blocking player 1 from scoring
        score = game.calculate_score()
        self.assertEqual(score, (1, 0))

    def test_calculate_score_claimed_by_handling(self):
        """Should assign score to the last player to interact with a cell."""
        game = FreeForAllGame(8, 8)
        game.attempt_move((3, 4), 0)
        game.attempt_move((3, 4), 1)

        game.apply_shade()

        score = game.calculate_score()
        self.assertEqual(score, (0, 1))


if __name__ == "__main__":
    unittest.main()
