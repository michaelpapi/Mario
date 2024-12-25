import pygame
from pygame.sprite import Sprite

class Monster(Sprite):
    """A class used to represent a single monster in the game"""

    def __init__(self, bs_game, width = 50, height = 50):
        """Initializes the monster and sets the starting position """
        super().__init__()
        self.screen = bs_game.screen
        self.settings = bs_game.settings

        #Loads the monster image and sets its rect attribute
        self.image = pygame.image.load('images/monsters.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

        # Starts a new monster
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Stores the alien's exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def check_edges(self):
        """Return True if monster is at the edge of the screen """
        screen_rect = self.screen.get_rect()
        if self.rect.top <= screen_rect.top or self.rect.bottom >= screen_rect.bottom:
            return True
       # return False

    def update(self):
        #Moves the monster to either the top or the bottom.
        self.y -= (self.settings.monster_speed * self.settings.fleet_direction)
        
        self.rect.y = self.y