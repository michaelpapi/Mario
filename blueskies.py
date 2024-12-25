import sys
from time import sleep

import pygame
from mario import Mario
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from bullet import Bullet
from monster import Monster
from pygame.sprite import Group



class BlueSkies:
    """General Overall class to manage all game assets and behaviour"""

    def __init__(self):
        """Initializes the game, and creates the game resources"""

        pygame.init()
        self.settings = Settings()
        

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Blue Skies")


        # Creates an instance to store game statstics and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.mario = Mario(self)
        self.bullets = Group() # Creates a group to store the bullets
        self.monsters = Group() #Creates a group to store the monsters
        self._create_fleet()

        # Make the Play button
        self.play_button = Button(self, 'Play')

        # Make Diifculty buttons
        self.easy_button = Button(self, "Easy", pos=(self.settings.screen_height // 1.3 - 100, self.settings.screen_height // 2 - 60))
        self.medium_button = Button(self, "Medium", pos=(self.settings.screen_height // 1.3 - 100, self.settings.screen_height // 2))
        self.hard_button = Button(self, "Hard", pos=(self.settings.screen_height // 1.3 - 100, self.settings.screen_height // 2 + 60))


    def run_game(self):
        """Starts the loop for the game"""

        while True:
            self._check_events()

            if self.stats.game_active:
                self.mario.update()
                self._update_bullets()
                self._update_monsters()
            
            #Drawing the screen from earlier
            self._update_screen()
           
    def _check_events(self):
        #Watches for the keyboard and mouse action.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.stats.difficulty_selected:
                    self._check_difficulty_buttons(mouse_pos)
                else:
                    self._check_play_button(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    
    def _check_keydown_events(self, event):
        """Responds to  the key presses"""

        """if event.key == pygame.K_RIGHT:
            self.mario.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.mario.moving_left = True"""
        if event.key == pygame.K_UP:
            self.mario.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.mario.moving_down = True
        elif event.key == pygame.K_SPACE: #Fires a bullet when Space is pressed
            self._fire_bullet()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()


    def _check_keyup_events(self, event):
        """Responds to Key releases"""

        """if event.key == pygame.K_RIGHT:
            self.mario.moving_right = False
        if event.key == pygame.K_LEFT:
            self.mario.moving_left = False"""
        if event.key == pygame.K_UP:
            self.mario.moving_up = False
        if event.key == pygame.K_DOWN:
            self.mario.moving_down = False
    
    def _check_play_button(self, mouse_pos):
        """Starts a new game when player clicks on play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings
            self.stats.difficulty_selected = True
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()

    def _check_difficulty_buttons(self, mouse_pos):
        """Check which difficulty was selected. """
        if self.easy_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty('easy')
            self._start_game()

        elif self.medium_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty('medium')
            self._start_game()

        elif self.hard_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty('hard')
            self._start_game()

    def _start_game(self):
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Hides difficulty buttons
            self.stats.difficulty_selected = False

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Gets rid of remaining monsters and bullets
            self.monsters.empty()
            self.bullets.empty()

            # Create a new fleet and centers mario
            self._create_fleet() # Check
            self.mario.center_mario()


    
    def _fire_bullet(self):
        """Creates a new bullet and add's it to the bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed: #Limits the number of bullets
            new_bullet = Bullet(self) #Creates an instance of bullet
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Updates position of the bullets and gets rid of the old bullets"""
        # Updates the bullet position
        self.bullets.update() 

        # Getting rid of  the bullets that have disappered  
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
                
        self._check_bullet_monster_collisions()

    def _check_bullet_monster_collisions(self):
        # Checking if any of the bullets have hit the monsters
        # If so, get rid of both monster and bullet
        collisions = pygame.sprite.groupcollide(self.bullets, self.monsters, True, True)

        if collisions:
            for monsters in collisions.values():
                self.stats.score += self.settings.monster_points * len(monsters)
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.monsters:
            self._start_new_level()

    def _start_new_level(self):
        """Starts a new level."""
        # Destroys existing bullets and creates a new fleet
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level
        self.stats.level += 1
        self.sb.prep_level()

    def _mario_hit(self):
        """Responds to mario being hit by a  monster. """
        if self.stats.marios_left > 0:
            # Decreases mario's left
            self.stats.marios_left -= 1
            self.sb.prep_marios()

            # Gets rid of any remaining moonsters and bullets.
            self.monsters.empty()
            self.bullets.empty()

            # Creates a new fleet and centers mario
            self._create_fleet()
            self.mario.center_mario()

            # Pauses the game
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Creates the fleet of monsters. """
        # Creates an monster and finds the number of aliens in a row.
        # Spacing between each monster is equal to one monster width
        monster = Monster(self)
        monster_width, monster_height = monster.rect.size
        mario_width = self.mario.rect.width

        # Gets space for monsters across the screen
        spacing_factor = 4 #Increase this factor to increase spacing
        available_space_x = (self.settings.screen_width - (3 * monster_width) - mario_width)
        number_monsters_x = available_space_x // (spacing_factor * monster_width)

        # Calculates the total width of the fleet
        #total_fleet_width = number_monsters_x * monster_width

        # Calculates the starting x position to ensure space on the left
        starting_x = 5 * monster_width


        # Determines the number of rows of monsters that fit the screen.
        avaliable_space_y = self.settings.screen_height - (2 * monster_height)
        number_rows = avaliable_space_y // (2 * monster_height)

        #Reduces number of rows by setting a maximum
        max_rows = 5
        number_rows = min(max_rows, number_rows)

        # Creates the first row of monsters
        for row_number in range(number_rows):
            for monster_number in range(number_monsters_x):
                self._create_monster(starting_x, monster_number, row_number, spacing_factor)

    def _create_monster(self, starting_x, monster_number, row_number, spacing_factor):
            # Creates a monster and places it in a row.
            monster = Monster(self)
            monster_width, monster_height = monster.rect.size
            monster.x = starting_x + spacing_factor * monster_width * monster_number
            monster.rect.x = monster.x
            monster.y = monster_height + 2 * monster_height * row_number
            monster.rect.y = monster.y
            self.monsters.add(monster)
    

    def _update_monsters(self):
        """Updates the position of the monsters in the fleet"""
        self._check_fleet_edges()
        self.monsters.update()
        # Look for monster-ship collision s
        if pygame.sprite.spritecollideany(self.mario, self.monsters):
            self._mario_hit()

        # Looks for monsters hitting the left of the screen
        self._check_monsters_hit_left()

    def _check_fleet_edges(self):
        #Responds immediately if any monsters have reached the edge.
        for monster in self.monsters.sprites():
            if monster.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        #Moves the entire fleet to the left and changes the fleet's direction
        for monster in self.monsters.sprites():
            monster.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 

    def _check_monsters_hit_left(self):
        """Checks if any aliens have reached the left of the screen"""
        screen_rect = self.screen.get_rect()
        for monster in self.monsters.sprites():
            if monster.rect.left <= screen_rect.left:
                # Treating like if mario got hit
                self._mario_hit()
                break

    def _update_screen(self):
        # Ensures screen is redrawn after each pass on the loop
        self.screen.fill(self.settings.bg_colour)
        self.mario.blitme()

        #Draws the bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.monsters.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            if self.stats.difficulty_selected:
                self.easy_button.draw_button()
                self.medium_button.draw_button()
                self.hard_button.draw_button()
            else:
                self.play_button.draw_button()


        pygame.display.flip()



if __name__ == "__main__":
    #Makes an instance of the game and runs it.

    bs = BlueSkies()
    bs.run_game()