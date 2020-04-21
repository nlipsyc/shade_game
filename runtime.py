from constants import SHADE_SIZE, GAME_SIZE, TURNS_PER_GAME


class Runtime(object):
    def __init__(self, game_class, player_0_class, player_1_class, **kwargs):
        self.number_of_turns = 32
        self.print_moves = False
        self.print_scores = False
        self.print_game_board = False
        self.print_final_score = True
        self.shade_size = SHADE_SIZE
        self.game_size = GAME_SIZE
        self.turns_per_game = TURNS_PER_GAME

        # Overwrite any of the defaults if they were passed in
        self.__dict__.update(kwargs)

        self.game = game_class(*self.game_size)
        player_0_instance = player_0_class(self.game_size, self.shade_size)
        player_1_instance = player_1_class(self.game_size, self.shade_size)

        self.player_0 = {"algorithm": player_0_instance, "name": 0}
        self.player_1 = {"algorithm": player_1_instance, "name": 1}

    def make_move(self, player):
        """For a given player, recursively attempt moves until one succeeds."""
        move_to_attempt = player["algorithm"].propose_move()

        try:
            # Move was successful
            self.game.attempt_move(move_to_attempt, player["name"])
            return move_to_attempt
        except PermissionError:
            # An illegal move was attempted.  Let's try again.
            return self.make_move(player)

    def do_ply(self):
        """Make moves for a single ply (one move for each player)."""
        player_0_move = self.make_move(self.player_0)
        self.game.apply_shade()
        self.game.calculate_score()

        player_1_move = self.make_move(self.player_1)
        self.game.apply_shade()
        player_0_score, player_1_score = self.game.calculate_score()

        if self.print_moves:
            print(f"Player 0 Move: {player_0_move}\nPlayer 1 Move: {player_1_move}")
        if self.print_scores:
            print(f"Player 0 score: {player_0_score}\nPlayer 1 score: {player_1_score}")
        if self.print_game_board:
            self.game.draw_game()

    def simulate_game(self):
        for turn in range(self.turns_per_game):
            self.do_ply()

        score = self.game.calculate_score()
        return score

        if self.print_final_score:
            player_0_score, player_1_score = score
            print(f"Player 0 score: {player_0_score}\nPlayer 1 score: {player_1_score}")