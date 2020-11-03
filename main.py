# The base skeleton for any big python project

import sys

import pygame

from settings import *

class Program:
    def __init__(self):
        '''
        Initializing the main attributes of a program
        '''
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True  # If this var is true - the game runs
        self.load_data()

    def load_data(self):
        '''
        This function is responsible for loading data
        '''
        # This is for paused screen
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))


    def new(self):
        '''
        This function is responsible for starting a new game
        '''
        # Start the program
        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.paused = False

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
            if not self.paused:
                self.update()
            self.draw()


    def update(self):
        '''
        Responsible for the whole game loop and every game process
        '''
        self.all_sprites.update()



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


    def draw(self):
        '''
        Here we draw everything that is needed
        '''

        self.screen.fill(BROWN)
        # Dim the screen if paused
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text('Paused', 105, RED, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()


    def show_start_screen(self):
        '''
        Responsible for showing the start menu
        '''
        pass


    def show_go_screen(self):
        '''
        Responsible for showing the end screen
        '''
        pass

    def draw_text(self, text: str, size: int, color: tuple, x: int, y: int, align='center'):
        '''
        Draws text at specified position and aligned specifically(nw - north west, etc.)
        '''
        font = pygame.font.SysFont('Arial', size)
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


# Start the program
p = Program()
p.show_start_screen()
while True:
    p.new()
    p.run()
    p.show_go_screen()

