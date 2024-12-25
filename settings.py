class Settings:
    """Class to store all game settings"""

    def __init__(self):
        """Initializes game settings"""

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (50, 100, 200)

        #Mario's settings
        self.mario_limit = 3

        #Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 10
        self.bullet_height = 20
        self.rotation_speed = 4
        self.bullets_allowed = 3

        #Monster settings
        self.fleet_drop_speed = 10
       
       # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point value increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        self.mario_speed = 1.5
        self.bullet_speed = 1.5
        self.monster_speed = 1.0
        self.monster_count = 10

        # Fleet direction of 1 rrepresents right, while -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.monster_points = 50

    def set_difficulty(self, difficulty):
        """Sets the game difficulty. """
        if difficulty == 'easy':
            self.mario_speed = 1.0
            self.bullet_speed = 1.5
            self.monster_speed = 0.5

        elif difficulty == 'medium':
            self.initialize_dynamic_settings()

        elif difficulty == 'hard':
            self.mario_speed = 2.0
            self.bullet_speed = 3.0
            self.monster_speed = 1.5

    def increase_speed(self):
        """Increases the speed and monster point values. """
        self.mario_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.monster_speed *= self.speedup_scale

        self.monster_points = int(self.monster_points * self.score_scale)
        