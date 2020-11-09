# The base skeleton for any big python project

# Standart libraries
import sys
import os
import random
# Community libraries
import pygame
# Custom libraries
from settings import *
from sprites import *
from number_functions import *
from map_handler import *



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
        snd_folder = os.path.join(game_folder, 'sounds')
        # Map data
        self.map = Map(os.path.join(map_folder, random.choice(['map1.txt', 'map2.txt', 'map3.txt'])))
        # The all sprite images
        self.player_image = pygame.image.load(os.path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.wall_image = pygame.image.load(os.path.join(img_folder, WALL_IMG)).convert_alpha()
        self.boss_image = pygame.image.load(os.path.join(img_folder, BOSS_IMG)).convert_alpha()
        self.key_image = pygame.image.load(os.path.join(img_folder, KEY_IMG)).convert_alpha()
        self.chest_image = pygame.image.load(os.path.join(img_folder, CHEST_IMG)).convert_alpha()
        # self.grass_image = pygame.image.load(os.path.join(img_folder, 'grass.png')).convert_alpha()
        self.candy_image = pygame.image.load(os.path.join(img_folder, CANDY_IMG)).convert_alpha()

        # This is for paused screen
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.key_sound = pygame.mixer.Sound(os.path.join(snd_folder, KEY_SOUND))
        self.key_sound.set_volume(0.1)

        self.correct_sound = pygame.mixer.Sound(os.path.join(snd_folder, CORRECT_SOUND))
        self.correct_sound.set_volume(0.1)

        self.wrong_sound = pygame.mixer.Sound(os.path.join(snd_folder, WRONG_SOUND))
        self.wrong_sound.set_volume(0.1)


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
        self.candy_group = pygame.sprite.Group()
        self.total_eggs = 0
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
                    self.total_eggs += 1
                    Chest(self, col, row)
                if tile == 'B':
                    Boss(self, col, row)

        # New game data
        self.eggs_found = 0
        self.keys_found = 0
        self.candy = 0
        self.given_question = ''
        self.timeleft = ''
        # New game flags
        self.question_asked = False
        self.paused = False
        self.draw_debug = False


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

        # Collision with eggs
        hits = pygame.sprite.spritecollide(self.player, self.eggs, False)
        for hit in hits:
            if self.keys_found >= 1:
                self.question('rand')
                self.eggs_found += 1
                # We use our key and kill the chest object
                self.keys_found -= 1
                hit.kill()

        # Collision with keys
        hits = pygame.sprite.spritecollide(self.player, self.keys_group, False)
        for hit in hits:
            # Just add up keys here
            self.keys_found += 1
            self.key_sound.play()
            hit.kill()

        # Collision with a boss
        hits = pygame.sprite.spritecollide(self.player, self.bosses, False)
        for hit in hits:
            if self.eggs_found == self.total_eggs:
                # Boss asks 3 questions by default
                for i in range(3):
                    if self.question('rand', boss=True):
                        self.candy += 5
                    else:
                        self.candy = 'lose'
                        if self.candy == 'lose':
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

            # # won
            # if event.type == pygame.USEREVENT + 1:
            #     if self.playing:
            #         self.playing = False
            #         print('showing won go', self.candy)
            #         self.show_go_screen(won=True)
            # # lost
            # if event.type == pygame.USEREVENT + 2:
            #     if self.playing:
            #         self.playing = False
            #         print('showing lost go', self.candy)
            #         self.show_go_screen(won=False)

    def draw(self, yesno=True):
        '''
        Here we draw everything that is needed
        '''
        # print('draw yesno:', yesno)
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
            self.draw_question(self.given_question, yesno=yesno)
            self.draw_text(self.timeleft.replace('1 seconds', '1 second'), 20, RED, WIDTH / 2, 20)
            print('writing it')
        pygame.display.flip()

    def wait_for_key(self):
        '''
        Stops the game and waits if a key is pressed. Returns the key value for the question
        '''
        pygame.event.wait()
        waiting = True
        key = ''
        # print('drawing text', self.timeleft)
        # seconds_passed = 0
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        key = 'y'
                        waiting = False
                    if event.key == pygame.K_n:
                        key = 'n'
                        waiting = False
                    if event.key == pygame.K_a:
                        key = 'a'
                        waiting = False
                    if event.key == pygame.K_b:
                        key = 'b'
                        waiting = False
                    if event.key == pygame.K_c:
                        key = 'c'
                        waiting = False
                    if event.key == pygame.K_d:
                        key = 'd'
                        waiting = False
                # if time is up
                if self.running:
                    if event.type == pygame.USEREVENT:
                        self.seconds_passed += 1
                        self.timeleft = str(MAX_SECONDS - self.seconds_passed) + ' seconds left'
                        self.draw(self.yesno)
                        if self.seconds_passed >= MAX_SECONDS:
                            print('time\'s up!')
                            self.time_is_up = True
                            self.timeleft = ''
                            return 'timeout'
        return key

    def wait_for_any_key(self):
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def show_start_screen(self):
        '''
        Responsible for showing the start menu
        '''
        # self.screen.fill((176, 231, 154))
        self.draw_text('NUMBER MAZE', 60, GREEN, WIDTH / 2, HEIGHT / 8)
        self.draw_text('[w]|[a]|[s]|[d] to move', 16, RED, WIDTH / 2, HEIGHT / 5)
        self.draw_text('You\'ve been put in a maze and your only way to get out is to collect all the keys and open all the chests with them.',
                       12, BLUE, WIDTH / 2, HEIGHT / 4)
        self.draw_text('When you\'ve opened all of the chests, you must defeat a robot boss to escape the maze',
            12, BLUE, WIDTH / 2, HEIGHT / 4 + 20)
        self.draw_text('When you open a chest, you have time to answer as much questions as possible. You get candy depending on jour answers',
                       11, BLUE, WIDTH / 2, HEIGHT / 4 + 40)
        self.draw_text('Press any button to play', 30, WHITE,
                       WIDTH / 2, (HEIGHT / 2) - 150)
        self.draw_text('This game helps you learn three different number types.', 12, WHITE,
                       WIDTH / 2, (HEIGHT / 2) - 70)
        self.draw_text('Here\'s a quick guide:', 12, WHITE,
                       WIDTH / 2, (HEIGHT / 2) - 30)
        self.draw_text('An Ulam number is a member of an Ulam sequence, which starts with 1 and 2. The next member is',
                       12, CYAN, WIDTH / 2, (HEIGHT / 2) + 20)
        self.draw_text('defined as the next smallest integer which is the sum of exactly one pair of previous terms.',
                       12, CYAN, WIDTH / 2, (HEIGHT / 2) + 40)
        self.draw_text('Thus, the first 8 elements of Ulam`s sequence are 1, 2, 3, 4, 6, 8, 11, 13... And so on.', 12,
                       CYAN, WIDTH / 2, (HEIGHT / 2) + 60)

        self.draw_text('A prime number is a positive integer that has exactly two positive integer factors, 1 and', 12,
                       CYAN, WIDTH / 2, (HEIGHT / 2) + 100)
        self.draw_text('itself. Say, 12 is not a prime number as 1, 2 and 3 are its factors. ', 12, CYAN, WIDTH / 2,
                       (HEIGHT / 2) + 120)
        self.draw_text('However, 7 is a prime number, as its factors are 1 and 7 only.', 12, CYAN, WIDTH / 2,
                       (HEIGHT / 2) + 140)

        self.draw_text('A lucky number is a natural number in a set generated by a certain sieve.', 12, CYAN, WIDTH / 2,
                       (HEIGHT / 2) + 180)
        self.draw_text(
            'To begin the sieving process, first write down all natural numbers starting from 1: 1, 2, 3, 4…', 12, CYAN,
            WIDTH / 2, (HEIGHT / 2) + 200)
        self.draw_text('Then, remove every second item from your list and get 1, 3, 5, 7, 9… The second number in this',
                       12, CYAN, WIDTH / 2, (HEIGHT / 2) + 220)
        self.draw_text(
            'new sequence is 3, so for the next iteration, remove every third element from it: 1, 3, 7, 9, 13, 15....',
            12, CYAN, WIDTH / 2, (HEIGHT / 2) + 240)
        self.draw_text('Now, the first surviving number in your sequence is 7, so continue removing every 7th number,',
                       12, CYAN, WIDTH / 2, (HEIGHT / 2) + 260)
        self.draw_text(
            'get 1, 3, 7, 9, 13, 15, 21, 25… Now, the first surviving number in your sequence is 7, so continue removing',
            12, CYAN, WIDTH / 2, (HEIGHT / 2) + 280)
        self.draw_text(
            'every 7th number, get 1, 3, 7, 9, 13, 15, 21, 25… and continue iterating till you reach a needed number.',
            12, CYAN, WIDTH / 2, (HEIGHT / 2) + 300)

        pygame.display.flip()
        # We wait for a pressed key
        self.wait_for_any_key()

    def show_go_screen(self, won=False):
        '''
        Responsible for showing the game over screen
        '''
        # self.screen.fill((176, 231, 154))
        print('showing go', self.candy)
        if won:
            self.draw_text('YOU WON', 60, BLUE, WIDTH / 2, HEIGHT / 2)
            self.draw_text('Press y or n to play again', 30, BLACK,
                           WIDTH / 2, 3 * HEIGHT / 4)
            self.draw_text('Candy collected: ' + str(self.candy), 30, BLACK,
                           WIDTH / 2, 3 * HEIGHT / 4 - 120)
        else:
            self.draw_text('GAME OVER', 60, RED, WIDTH / 2, HEIGHT / 2)
            self.draw_text('Press y or n to play again', 30, BLACK,
                           WIDTH / 2, 3 * HEIGHT / 4)
        pygame.display.flip()
        # We wait for a pressed key
        self.wait_for_any_key()

    def draw_text(self, text: str, size: int, color: tuple, x: int, y: int, align='center'):
        '''
        Draws text at specified position and aligned specifically(nw - north west, etc.)
        '''
        font = pygame.font.Font('Pixeled.ttf', size)
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

    def question(self, diff_level='std', boss=False):
        ''' Asks player a question of a given difficulty '''
        print('timer initiatied')
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        self.time_is_up = False
        self.seconds_passed = 0
        self.timeleft = str(MAX_SECONDS) + ' seconds left'

        while self.time_is_up == False:

            self.question_asked = True

            question = theQuestion()

            self.given_question, expected_key = question[0]
            self.yesno = question[1]
            print('yesno', self.yesno)

            # Call self.draw again so the question is drawn on the screen during this function lifetime
            self.draw(self.yesno)
            # Gey the answer
            answer = self.wait_for_key()

            # Return the value depending on the answer
            if answer == expected_key:
                print('Correct! XP increased')
                self.candy += 3
                self.question_asked = False
                self.correct_sound.play()
            else:
                print('Wrong! XP decreased')
                self.candy -= 2
                self.question_asked = False
                self.wrong_sound.play()
                if boss:
                    return False

        return None


    def draw_hud(self):
        '''
        Draws the player HUD up the top
        '''
        self.screen.blit(self.candy_image, (160, 0))
        self.screen.blit(pygame.transform.scale(self.key_image, (48, 48)), (40, 0))
        self.draw_text(str(self.keys_found), 20, BLACK, 20, -5, align='nw')
        self.draw_text(str(self.candy), 20, BLACK, 120, -5, align='nw')

    def draw_question(self, given_question, yesno=False):
        # bg_rect = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 - 70, 200, 70)
        # bg_rect_outline = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 - 70, 200, 70)
        # pygame.draw.rect(self.screen, LIGHTGREY, bg_rect)
        # pygame.draw.rect(self.screen, BLACK, bg_rect_outline, 3)
        self.draw_text(given_question, 20, YELLOW, WIDTH / 2, HEIGHT / 2)
        if yesno:
            self.draw_text('press [y] if yes | press [n] if no', 15, BLACK, WIDTH / 2, HEIGHT / 2 + 70)
        else:
            self.draw_text('press [a], [b], [c] or [d]', 15, BLACK, WIDTH / 2, HEIGHT / 2 + 70)


# Start the program
p = Program()
p.show_start_screen()
while True:
    # Keep starting a new game until we exit
    p.new()
    p.run()
    p.show_go_screen()

