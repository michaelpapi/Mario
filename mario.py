import pygame
from pygame.sprite import Sprite

class Mario(Sprite):
    """A class to manage the ship"""

    def __init__(self, bs_game, width=50, height=50):
        """Initialize the mario and set its starting point."""
        super().__init__()
        self.screen = bs_game.screen
        self.settings = bs_game.settings
        self.screen_rect = bs_game.screen.get_rect()

        #Load mario's image and get his rect.

        self.image = pygame.image.load("images/mario.png")
        self.image = pygame.transform.scale(self.image,(width, height))
        self.rect = self.image.get_rect()

        #Start each new mario character at the buttom centre of the screen
        self.rect.midleft = self.screen_rect.midleft

        #Store a decimal value for the ship's horizontal position
        """self.x = float(self.rect.x)"""
        self.y = float(self.rect.y)

        #Movememnt flags
        """self.moving_right = False
        self.moving_left = False"""
        self.moving_up = False
        self.moving_down = False


    def update(self):
        """Updates mario's position on movement flag"""
        #Updates mario's x value not the rect.
        """if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.mario_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.mario_speed"""

        #Updates mario's y value not the rect.
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.mario_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.mario_speed


        """self.rect.x = self.x"""
        self.rect.y = self.y

    def blitme(self):
        """Draws mario at it's current location"""
        self.screen.blit(self.image, self.rect)

    def center_mario(self):
        """Centers mario back on the screen"""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)