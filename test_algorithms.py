import mock
import pytest

import constants

# from game import FreeForAllGame
from algorithms import (
    AlgorithmParamaters,
    ConstructedAlgorithm,
    GameParamaters,
    algorithm_factory,
    random_algorithm_factory,
)


@pytest.fixture()
def mock_game_params():
    return GameParamaters(constants.GAME_SIZE, mock.Mock())


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


def test_algorithm_factory(mock_algorithm_parameters):
    """Should return a valid ConstructedAlgorithm."""
    algorithm_instance = algorithm_factory(mock_algorithm_parameters, seed=42)
    assert isinstance(algorithm_instance, ConstructedAlgorithm)


def test_random_seed_move_proposal(mock_game_params, mock_algorithm_parameters):
    """Needs a valid cell calculator before this test makes sense."""
    """Should have the same results when intialized multiple times with the same seed."""
    algorithm_1 = algorithm_factory(mock_algorithm_parameters, seed=42)
    move_1 = algorithm_1.propose_move()

    algorithm_2 = algorithm_factory(mock_algorithm_parameters, seed=42)
    move_2 = algorithm_2.propose_move()

    assert move_1 == move_2


def test_different_seed_move_proposal(mock_game_params, mock_algorithm_parameters):
    """Needs a valid cell calculator before this test makes sense."""
    """Should have different results with different seeds.

    Because the first move is hardcoded as (0,0) with the OriginCurosrInitializer, we only expect the _second_ move to
    be random.

    This is being done to validate that the results of the above test are actually related to the seed value.
    """
    algorithm_1 = random_algorithm_factory(seed=42)
    algorithm_1.propose_move()  # should be (0, 0)
    move_1 = algorithm_1.propose_move()

    algorithm_2 = random_algorithm_factory(seed=43)
    algorithm_2.propose_move()  # should be (0, 0)
    move_2 = algorithm_2.propose_move()

    assert move_1 != move_2
