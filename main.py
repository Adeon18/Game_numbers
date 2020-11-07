# The base skeleton for any big python project

# Standart libraries
import sys
import os
# Community libraries
import pygame
# Custom libraries
from settings import *
from sprites import *
from number_functions import *
from map_handler import *
from game_core import *


class Program:
    def __init__(self):
        '''
        Initializing the main attributes of a program
        '''
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True  # If this var is true - the game runs

        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        '''
        This function is responsible for loading data
        '''
        # Game folders where data is stored
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')
        map_folder = os.path.join(game_folder, 'maps')
        # Map data
        self.map = Map(os.path.join(map_folder, 'map1.txt'))
        # The all sprite images
        self.player_image = pygame.image.load(os.path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.wall_image = pygame.image.load(os.path.join(img_folder, WALL_IMG)).convert_alpha()
        self.boss_image = pygame.image.load(os.path.join(img_folder, BOSS_IMG)).convert_alpha()
        self.key_image = pygame.image.load(os.path.join(img_folder, KEY_IMG)).convert_alpha()
        self.chest_image = pygame.image.load(os.path.join(img_folder, CHEST_IMG)).convert_alpha()
        #self.grass_image = pygame.image.load(os.path.join(img_folder, 'grass.png')).convert_alpha()

        # This is for paused screen
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))


    def new(self):
        '''
        This function is responsible for starting a new game
        '''
        # These are the sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.keys_group = pygame.sprite.Group()
        self.eggs = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        # Read the data from a map file and blit it to the screen(spawn sprites)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row)
                if tile == 'K':
                    Key(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Chest(self, col, row)
                if tile == 'B':
                    Boss(self, col, row)

        # New game data
        self.eggs_found = 0
        self.keys_found = 0
        self.given_question = ''
        # New game flags
        self.question_asked = False
        self.paused = False
        self.draw_debug = False
        # Run the game loop
        self.run()


    def quit(self):
        '''
        Responsible for quitting from the program
        '''
        pygame.quit()
        sys.exit()


    def run(self):
        '''
        Game loop - set self.playing = False to end the game
        '''
        self.playing = True

        while self.playing:
            # This is delta time
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            # Here we check for events and whether we quit
            self.events()
            # Pause stops the game loop
            if not self.paused:
                self.update()
            self.draw()


    def update(self):
        '''
        Responsible for the whole game loop and every game process
        '''
        self.all_sprites.update()
        # We end the game if our health is gone
        if self.player.health < 0:
            self.playing = False

        # Collision with eggs
        hits = pygame.sprite.spritecollide(self.player, self.eggs, False)
        for hit in hits:
            if self.keys_found >= 1:
                if self.question('rand'):
                    # We add to health for the player if the answer is right
                    self.player.health += 1
                    self.eggs_found += 1
                else:
                    self.player.health -= 1
                # We use our key and kill the chest object
                self.keys_found -= 1
                hit.kill()

        # Collision with keys
        hits = pygame.sprite.spritecollide(self.player, self.keys_group, False)
        for hit in hits:
            # Just add up keys here
            self.keys_found += 1
            hit.kill()

        # Collision with a boss
        hits = pygame.sprite.spritecollide(self.player, self.bosses, False)
        for hit in hits:
            # Boss asks 3 questions by default
            for i in range(3):
                if self.question('rand'):
                    self.player.health += 1
                else:
                    # If we get 1 question wrong, we lose, and end the game
                    self.player.health -= PLAYER_HEALTH_MAX
                    if self.player.health < 0:
                        self.playing = False
                        break
            # Kill the boss if all questions are right
            hit.kill()



    def events(self):
        '''
        Check for events in the game
        '''
        for event in pygame.event.get():
            # Check for player quitting
            if event.type == pygame.QUIT:
                self.quit()
            # Check for pressed keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                # Check for pausing the game
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                # Toggle the debug mode
                if event.key == pygame.K_F3:
                    self.draw_debug = not self.draw_debug


    def draw(self):
        '''
        Here we draw everything that is needed
        '''
        # Draw everything
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_hud()
        # Dim the screen if paused
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text('Paused', 105, RED, WIDTH / 2, HEIGHT / 2)
        # Debug mode
        if self.draw_debug:
            # This just draws the collision rectangle when you press F3
            for sprite in self.all_sprites:
                pygame.draw.rect(self.screen, CYAN, sprite.rect, 1)
            self.draw_text("{:.2f}".format(self.clock.get_fps()), 25, CYAN, WIDTH / 2, 30)
        # This draws the questions to the screen
        if self.question_asked:
            self.draw_question(self.given_question)
        pygame.display.flip()

    def wait_for_key(self):
        '''
        Stops the game and waits if a key is pressed. Returns the key value for the question
        '''
        pygame.event.wait()
        waiting = True
        key = ''
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        key = 'yes'
                        waiting = False
                    if event.key == pygame.K_n:
                        key = 'no'
                        waiting = False

        return key


    def show_start_screen(self):
        '''
        Responsible for showing the start menu
        '''
        self.screen.fill((176, 231, 154))
        self.draw_text('NUMBERS GAME', 100, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text('Press y or n to play', 75, BLACK,
                       WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        # We wait for a pressed key
        self.wait_for_key()


    def show_go_screen(self):
        '''
        Responsible for showing the game over screen
        '''
        self.screen.fill((176, 231, 154))
        self.draw_text('GAME OVER', 100, BLACK, WIDTH / 2, HEIGHT / 2)
        self.draw_text('Press y or n to play again', 75, BLACK,
                       WIDTH / 2, 3 * HEIGHT / 4)
        pygame.display.flip()
        # We wait for a pressed key
        self.wait_for_key()

    def draw_text(self, text: str, size: int, color: tuple, x: int, y: int, align='center'):
        '''
        Draws text at specified position and aligned specifically(nw - north west, etc.)
        '''
        font = pygame.font.SysFont('Comic sans ms', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


    def question(self, diff_level='std'):
        ''' Asks player a question of a given difficulty '''
        self.question_asked = True
        if diff_level == 'rand':
            funcs = {'Ulam': ulam_number, 'happy': happy_number, 'prime': prime_number}
            randint = random.choice(range(100))
            rand_number_type = random.choice(list(funcs.keys()))
            print('Question: is', randint, 'a', rand_number_type, 'number?')
            self.given_question = 'Question: is {} a {} number?'.format(randint, rand_number_type)
            expected_answer = 'yes' if funcs[rand_number_type](randint) else 'no'
            print('Expected answer:', expected_answer)
        else:
            return None
        # Call self.draw again so the question is drawn on the screen during this function lifetime
        self.draw()
        # Gey the answer
        answer = self.wait_for_key()

        # Return the value depending on the answer
        if answer == expected_answer:
            print('Correct! XP increased')
            self.question_asked = False
            return True
        else:
            print('Wrong! XP decreased')
            self.question_asked = False
            return False

    def draw_hud(self):
        '''
        Draws the player HUD up the top
        '''
        bg_rect = pygame.Rect(0, 0, 200, 70)
        bg_rect_outline = pygame.Rect(0, 0, 200, 70)
        pygame.draw.rect(self.screen, LIGHTGREY, bg_rect)
        pygame.draw.rect(self.screen, BLACK, bg_rect_outline, 3)
        self.draw_player_health(5, 10, self.player.health / 10)
        self.draw_text('Keys: {}'.format(self.keys_found), 20, BLACK, 10, 35, align='nw')

    def draw_player_health(self, x, y, pct):
        '''
        Responsible for displaying player health
        '''
        if pct < 0:
            pct = 0
        BAR_LENGTH = 110
        BAR_HEIGHT = 25
        fill = pct * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = (x, y, fill, BAR_HEIGHT)
        if pct > 0.6:
            col = GREEN
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        pygame.draw.rect(self.screen, col, fill_rect)
        pygame.draw.rect(self.screen, BLACK, outline_rect, 3)
        self.draw_text('health', 20, BLACK, outline_rect.centerx, outline_rect.centery + 3)

    def draw_question(self, given_question):
        # bg_rect = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 - 70, 200, 70)
        # bg_rect_outline = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 - 70, 200, 70)
        # pygame.draw.rect(self.screen, LIGHTGREY, bg_rect)
        # pygame.draw.rect(self.screen, BLACK, bg_rect_outline, 3)
        self.draw_text(given_question, 70, YELLOW, WIDTH / 2, HEIGHT / 2)
        self.draw_text('press y if yes | press n if no', 70, BLACK, WIDTH / 2, HEIGHT / 2 + 70)


# Start the program
p = Program()
p.show_start_screen()
while True:
    # Keep starting a new game until we exit
    p.new()
    p.run()
    p.show_go_screen()

