from collections import Counter
from dataclasses import dataclass

from algorithms import random_algorithm_factory
from game import FreeForAllGame
from runtime import Runtime

NUMBER_OF_ROUNDS = 100

random_algorithm_0 = random_algorithm_factory()
random_algorithm_1 = random_algorithm_factory()
rt = Runtime(FreeForAllGame, random_algorithm_0, random_algorithm_1)
rt.simulate_game()


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
    player_0_score, player_1_score = rt.simulate_game()

    log = GameLog(game, player_0_score, player_1_score)
    game_log_collection.append(log)

    print(log)

    print("=======================\n")
player_0_score_counts = Counter([log.player_0_score for log in game_log_collection])
player_1_score_counts = Counter([log.player_1_score for log in game_log_collection])
print(f"Player 0 scores {sorted(player_0_score_counts.items())}")
print(f"Player 1 scores {sorted(player_1_score_counts.items())}")
print(f"Win counts{Counter([log.winner for log in game_log_collection]).items()}")
# print(
#     f"Player 0 wins {win_record[0]}\nPlayer 1 wins {win_record[1]}\nTies: {NUMBER_OF_ROUNDS - win_record[0] - win_record[1]}"
# )
# tie_percent = (NUMBER_OF_ROUNDS - win_record[0] - win_record[1]) / NUMBER_OF_ROUNDS
# print(
#     f"Player 0 wins {win_record[0] / NUMBER_OF_ROUNDS}\nPlayer 1 wins {win_record[1] / NUMBER_OF_ROUNDS}\nTies: {tie_percent}"
# )
