import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class to manage bullets fired from mario"""

    def __init__(self, bs_game):
        """Creates a bullet object at the ship's current location"""
        super().__init__()
        self.screen = bs_game.screen
        self.settings = bs_game.settings

        #Loads the bullet image.
        self.image = pygame.image.load('images/bullet.png')

        #Resizes the bullet to the desired width and height.
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_width, self.settings.bullet_height))

        #Getting the rect of the scaled image.
        self.rect = self.image.get_rect()

        #Set's the bullet initial position
        self.rect.midright = bs_game.mario.rect.midright

        #Store the bullet's position as a decimal value
        self.x = float(self.rect.x)

        self.angle = 0

    def update(self):
        """Moves the bullet up the screen"""
        # Updates the decimal position of the bullet.
        self.x += self.settings.bullet_speed
        #Updates the rect position
        self.rect.x = self.x

        #Updates the rotation angle
        self.angle += self.settings.rotation_speed


    def draw_bullet(self):
        """Draw the bullet to the screen."""
        # Rotates the image 
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        # Get the rect of the rotated image
        new_rect = rotated_image.get_rect(center=self.rect.center)
        # Draw the rotated image to the screen
        self.screen.blit(rotated_image, new_rect) 
