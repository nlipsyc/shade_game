import unittest
from game import FreeForAllGame
from algorithms import RandomAlgorithm, SystematicMaxShade


class TestGame(unittest.TestCase):
    def test_attempt_move_is_valid(self):
        """Should return True and toggle the board state given a valid move"""
        game = FreeForAllGame(8, 8)
        attempted_move = game.attempt_move((4, 3), 0)

        self.assertTrue(attempted_move)
        self.assertTrue(game.game_board[4][3].is_angled)
        self.assertEqual(game.game_board[4][3].claimed_by, 0)

    def test_attempt_move_is_invalid(self):
        """Should return False and not toggle the board state given a invalid move"""
        game = FreeForAllGame(8, 8)
        game.game_board[4][3].claimable = False
        attempted_move = game.attempt_move((4, 3), 0)

        self.assertFalse(attempted_move)
        self.assertFalse(game.game_board[4][3].is_angled)
        self.assertEqual(game.game_board[4][3].claimed_by, None)

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


class TestAlgorithims(unittest.TestCase):
    def test_initialization(self):
        alg = RandomAlgorithm((4, 6), 3)
        self.assertAlmostEqual(alg.w, 4)
        self.assertAlmostEqual(alg.shade_size, 3)

    def test_random_seed_repeatability(self):
        """Should yield the same results when intialized multiple times with the same seed."""

        alg1 = RandomAlgorithm((4, 6), 3, seed=42)
        move1 = alg1.propose_move()

        alg2 = RandomAlgorithm((4, 6), 3, seed=42)
        move2 = alg2.propose_move()

        self.assertEqual(move1, move2)

    def test_systematic_shade_columns(self):
        """Should be choosing from the most efficient columns on the board."""
        alg1 = SystematicMaxShade((8, 8), 3)
        self.assertEqual(alg1._claimable_columns, [0, 4])

        alg2 = SystematicMaxShade((16, 8), 3)
        self.assertEqual(alg2._claimable_columns, [0, 4, 8, 12])

        alg3 = SystematicMaxShade((12, 8), 4)
        self.assertEqual(alg3._claimable_columns, [0, 5, 10])

    def test_systematic_movement_through_cells(self):
        """Should vertically iterate through possible cells and then loop."""
        alg = SystematicMaxShade((8, 8), 3, seed=42)

        number_of_possible_moves = len(alg.claimable_cells)

        proposed_moves = []
        for move in range(number_of_possible_moves + 1):
            proposed_moves.append(alg.propose_move())

        # With a seed of 42 we start at (0, 4), let's make sure the next one is one bellow it
        self.assertEqual(proposed_moves[1][1], 5)

        # It looped successfully
        self.assertEqual(proposed_moves[0], proposed_moves[-1])


if __name__ == "__main__":
    unittest.main()
