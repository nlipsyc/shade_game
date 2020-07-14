import mock
import pytest

# from game import FreeForAllGame
from algorithms import AlgorithmParamaters, ConstructedAlgorithm, GameParamaters, algorithm_factory


@pytest.fixture()
def mock_game_params():
    return GameParamaters(mock.Mock(), mock.Mock())


@pytest.fixture()
def mock_algorithm_parameters():
    return AlgorithmParamaters(mock.Mock(), mock.Mock(), mock.Mock())


def test_game_params():
    """Should initialize a GameParameters object."""
    expected_dimensions = mock.Mock()
    expected_shade_size = mock.Mock()

    game_params = GameParamaters(expected_dimensions, expected_shade_size)

    assert game_params.game_dimensions is expected_dimensions
    assert game_params.shade_size is expected_shade_size


def test_algorithm_parameters():
    expected_cell_calculator = mock.Mock()
    expected_cursor_initializer = mock.Mock()
    expected_move_proposer = mock.Mock()

    alg_params = AlgorithmParamaters(expected_cell_calculator, expected_cursor_initializer, expected_move_proposer)

    assert alg_params.cell_calculator_class is expected_cell_calculator
    assert alg_params.cursor_initializer_class is expected_cursor_initializer
    assert alg_params.move_proposer_class is expected_move_proposer


def test_algorithm_factory(mock_game_params, mock_algorithm_parameters):
    """Should return a valid ConstructedAlgorithm."""
    algorithm_instance = algorithm_factory(mock_game_params, mock_algorithm_parameters, seed=42)
    assert isinstance(algorithm_instance, ConstructedAlgorithm)


# def test_random_seed_move_proposal(mock_game_params, mock_algorithm_parameters):
#     """Needs a valid cell calculator before this test makes sense."""
#     """Should have the same results when intialized multiple times with the same seed."""
#     algorithm_1 = algorithm_factory(mock_game_params, mock_algorithm_parameters, seed=42)
#     move_1 = algorithm_1.propose_move()

#     algorithm_2 = algorithm_factory(mock_game_params, mock_algorithm_parameters, seed=42)
#     move_2 = algorithm_2.propose_move()

#     assert move_1 == move_2


# def test_different_seed_move_proposal(mock_game_params, mock_algorithm_parameters):
#     """Needs a valid cell calculator before this test makes sense."""
#     """Should have different results with different seeds.

#     This is being done to validate that the results of the above test are actually related to the seed value.
#     """
#     algorithm_1 = algorithm_factory(mock_game_params, mock_algorithm_parameters, seed=42)
#     move_1 = algorithm_1.propose_move()

#     algorithm_2 = algorithm_factory(mock_game_params, mock_algorithm_parameters, seed=43)
#     move_2 = algorithm_2.propose_move()

#     assert move_1 != move_2


# class TestAlgorithims(unittest.TestCase):
#     def test_random_seed_repeatability(self):
#         """Should yield the same results when intialized multiple times with the same seed."""

#         alg1 = RandomAlgorithm((4, 6), 3, seed=42)
#         move1 = alg1.propose_move()

#         alg2 = RandomAlgorithm((4, 6), 3, seed=42)
#         move2 = alg2.propose_move()

#         self.assertEqual(move1, move2)

#     def test_systematic_shade_columns(self):
#         """Should be choosing from the most efficient columns on the board."""
#         alg1 = SystematicMaxShade((8, 8), 3)
#         self.assertEqual(alg1._claimable_columns, [0, 4])

#         alg2 = SystematicMaxShade((16, 8), 3)
#         self.assertEqual(alg2._claimable_columns, [0, 4, 8, 12])

#         alg3 = SystematicMaxShade((12, 8), 4)
#         self.assertEqual(alg3._claimable_columns, [0, 5, 10])

#     def test_systematic_movement_through_cells(self):
#         """Should vertically iterate through possible cells and then loop."""
#         alg = SystematicMaxShade((8, 8), 3, seed=42)

#         number_of_possible_moves = len(alg.claimable_cells)

#         proposed_moves = []
#         for move in range(number_of_possible_moves + 1):
#             proposed_moves.append(alg.propose_move())

#         # With a seed of 42 we start at (0, 4), let's make sure the next one is one bellow it
#         self.assertEqual(proposed_moves[1][1], 5)

#         # It looped successfully
#         self.assertEqual(proposed_moves[0], proposed_moves[-1])


# if __name__ == "__main__":
#     unittest.main()
