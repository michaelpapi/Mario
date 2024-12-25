import pygame.font

class Button:

    def __init__(self, bs_game, msg, pos=None):
        """Initializes button attributes. """
        self.screen = bs_game.screen
        self.screen_rect = self.screen.get_rect()


        # Set the dimensions and properties of the button. 

        self.width, self.height = 200, 50
        self.button_colour = (200, 100, 50)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it. 
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        if pos:
            self.rect.topleft = pos

        else:
            self.rect.center = self.screen_rect.center

        # Preps the message button
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn's the msg int o a rendered image and centers text to the button. """
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draws a blank button, then displays the mesg
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)