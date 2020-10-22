from collections import Counter
from dataclasses import dataclass

from algorithms import (
    systematic_max_shade_factory,
    random_start_systematic_max_shade_factory,
    random_start_random_offset_max_shade_factory,
)
from game import FreeForAllGame
from runtime import Runtime

NUMBER_OF_ROUNDS = 100


def setup_game(switch_order=False):
    algorithm_0 = random_start_systematic_max_shade_factory()
    algorithm_1 = systematic_max_shade_factory()
    rt = Runtime(FreeForAllGame, algorithm_0, algorithm_1, print_moves=True)
    return rt


@dataclass
class GameLog:
    """A log of the results of a single game."""

    game_number: int
    player_0_score: int
    player_1_score: int

    def __str__(self):
        return f"Player 0 Score: {player_0_score}\nPlayer 1 Score: {player_1_score}\nWinner: {self.winner}"

    @property
    def winner(self):
        if self.player_0_score == self.player_1_score:
            return None

        if self.player_0_score > self.player_1_score:
            return 0
        else:
            return 1


game_log_collection = []
for game in range(NUMBER_OF_ROUNDS):
    print(f"Game {game}\n")
    # The order that players go confers a clear advantage, let's switch these each time to eliminate that noise
    should_switch_order = game % 2 == 1
    rt = setup_game(switch_order=should_switch_order)
    player_0_score, player_1_score = rt.simulate_game()

    log = GameLog(game, player_0_score, player_1_score)
    game_log_collection.append(log)

    print(log)

    print("=======================\n")
player_0_score_counts = Counter([log.player_0_score for log in game_log_collection])
player_0_score_counts = sorted(player_0_score_counts.items())
player_0_score_counts = ", ".join(f"{score}:{count}" for score, count in player_0_score_counts)

player_1_score_counts = Counter([log.player_1_score for log in game_log_collection])
player_1_score_counts = sorted(player_1_score_counts.items())
player_1_score_counts = ", ".join(f"{score}:{count}" for score, count in player_1_score_counts)

win_counts = Counter([log.winner for log in game_log_collection]).items()
win_counts = ", ".join(f"{winner}: {count}" for winner, count in win_counts)
print(f"Player 0 (score: count) -- {player_0_score_counts}")
print(f"Player 1 (score: count) -- {player_1_score_counts}")
print(f"Win counts (winner: count) -- {win_counts}")
