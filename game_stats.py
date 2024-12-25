class GameStats:
    """Tracks statistics for Blue Skies Game"""


    def __init__(self, bs_game):
        """Initializes statistics."""
        self.settings = bs_game.settings
        self.reset_stats()

        # Starts Blue Skies in an active state.
        self.game_active = False

        # Diffficulty Flag
        self.difficulty_selected = False

        # High score should not be reset
        self.high_score = self._load_high_score()

        
    def reset_stats(self):
        """Initializes stats that can change during the game."""
        self.marios_left = self.settings.mario_limit

        # Score settings
        self.score = 0
        self.level = 1

    def _load_high_score(self):
        """Loads the high score from a file."""
        try:
            with open("high_score.txt", "r") as file:
                high_score = int(file.read())
        except FileNotFoundError:
            high_score = 0
        return high_score
    
    def save_high_score(self):
        """Save the high score to a file."""
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))