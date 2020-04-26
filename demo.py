from runtime import Runtime
from algorithms import RandomAlgorithm
from game import FreeForAllGame

NUMBER_OF_ROUNDS = 5000

rt = Runtime(FreeForAllGame, RandomAlgorithm, RandomAlgorithm)
rt.simulate_game()


win_record = {0: 0, 1: 0}
for game in range(NUMBER_OF_ROUNDS):
    print(f"Game {game}\n")
    player_0_score, player_1_score = rt.simulate_game()

    if player_0_score > player_1_score:
        win_record[0] += 1

    elif player_0_score < player_1_score:
        win_record[1] += 1
        print("=======================\n")

print(
    f"Player 0 wins {win_record[0]}\nPlayer 1 wins {win_record[1]}\nTies: {NUMBER_OF_ROUNDS - win_record[0] - win_record[1]}"
)
tie_percent = (NUMBER_OF_ROUNDS - win_record[0] - win_record[1]) / NUMBER_OF_ROUNDS
print(
    f"Player 0 wins {win_record[0] / NUMBER_OF_ROUNDS}\nPlayer 1 wins {win_record[1] / NUMBER_OF_ROUNDS}\nTies: {tie_percent}"
)

