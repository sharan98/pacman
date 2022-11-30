import pygame
import pygame.locals
import time
from agents2 import *#ghost, pacman
from grid import *#Grid
from utils import *#DOWN, LEFT, RIGHT, STOP, UP, Colour

# SCREEN_SIZE =  (28 * 20, 31 * 20)
SCREEN_SIZE =  (17 * 30, 25 * 30)


pygame.init()
pygame.mixer.init()

FPS = 30
fpsClock = pygame.time.Clock()
SCREEN   = pygame.display.set_mode (SCREEN_SIZE) #, pygame.RESIZABLE)

font = pygame.font.SysFont("comicsansms", 30)
livestext = font.render("Hello, World", True, (255,255,0))
text = font.render("Hello, World", True, (255,255,0))
DISPSURF = pygame.display.get_surface()

coins_group = pygame.sprite.Group()
apples_group = pygame.sprite.Group()
grid_group = pygame.sprite.Group()
ghosts_group = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()

DIED = pygame.USEREVENT + 1
ATE_APPLE = pygame.USEREVENT + 2
SPEED_UP = pygame.USEREVENT + 3




class Game():

    maze = [#0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],#, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],#, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],#, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],#, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0],#, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],#, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0],#, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],#, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],#, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],#, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],#, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],#, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 1, 1, 2, 1, 1, 1, 1, 0, 1, 1, 0],#, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],#, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0],#, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],#, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],#, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#, 0, 0, 0],
            # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #, 0, 0, 0]
    ]

    def __init__(self, gridcolor = Colour.WHITE):
        # WHITE -> Colour of GRid walls, ORANGE -> Colour of coins
        self.grid = Grid(Game.maze, Colour.WHITE, Colour.ORANGE)
        # the following two lists are lists of sprites
        self.gridwalls = self.grid.gridwallsList
        self.coins = self.grid.coinsList
        self.score = 0
        self.apples = self.grid.appleList
        self.lives = 3
        
        coins_group.add(self.coins)
        apples_group.add(self.apples)
    
    def make_agents(self):
        self.Pacman = pacman(Colour.YELLOW, [45, 45])

        # [...] -> co-ordinates of the center of blinky
        Blinky = ghost(Colour.RED, [15*30 + 10, 17*30 +10], STOP , BLINKY)
        Inky = ghost(Colour.GREEN, [15*30 + 10, 1*30 +10], STOP , INKY)
        Blue = ghost(Colour.NAVYBLUE, [9*30 + 10, 9*30 +10], STOP , BLUE)
        Clyde = ghost(Colour.ORANGE, [1*30 + 10, 17*30 +10], STOP , CLYDE)

        ghosts_group.add(Blinky, Inky, Blue, Clyde)
        all_sprites.add(self.gridwalls, coins_group.sprites(), apples_group.sprites(), self.Pacman, ghosts_group.sprites())

    def play(self):
        ghosts_group.empty()
        # coins_group.empty()
        # apples_group.empty()
        all_sprites.empty()
        self.make_agents()
        Agent.set_grid(self.grid)
        return self.Pacman

    def delete_agents(self):
        all_sprites.empty()
        all_sprites.add(self.gridwalls)

game = Game()

# [45, 45] -> co-ordinates of the center of pacman
# Pacman = pacman(Colour.YELLOW, [45, 45])#, game.grid)

# [...] -> co-ordinates of the center of blinky
# Blinky = ghost(Colour.RED, [15*30 + 10, 17*30 +10], STOP , game.grid, BLINKY)
# Inky = ghost(Colour.GREEN, [15*30 + 10, 1*30 +10], STOP , game.grid, INKY)
# Blue = ghost(Colour.NAVYBLUE, [9*30 + 10, 9*30 +10], STOP , game.grid, BLUE)
# Clyde = ghost(Colour.ORANGE, [1*30 + 10, 17*30 +10], STOP , game.grid, CLYDE)
# Blinky = ghost(Colour.RED, [15*30 + 10, 17*30 +10], STOP , BLINKY)
# Inky = ghost(Colour.GREEN, [15*30 + 10, 1*30 +10], STOP , INKY)
# Blue = ghost(Colour.NAVYBLUE, [9*30 + 10, 9*30 +10], STOP , BLUE)
# Clyde = ghost(Colour.ORANGE, [1*30 + 10, 17*30 +10], STOP , CLYDE)

# ghosts_group.add(Blinky, Inky, Blue, Clyde)
# coins_group.add(game.coins)
# apples_group.add(game.apples)
# all_sprites.add(game.gridwalls, game.coins, game.apples, Pacman, Blinky, Inky, Blue, Clyde)

if __name__ == '__main__':
    # game.play()
    closed = False
    count = -1
    t = 0
    Pacman = game.play()
    Agent.set_grid(game.grid)
    while not closed:
        SCREEN.fill(Colour.BLACK.value)
        SCREEN.blit(text,(320,560))
        SCREEN.blit(livestext,(120,560))
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                print ("window closed")
                closed = True

            # pacman collides with ghost
            elif event.type == DIED:
                # game.delete_agents()
                game.lives -= 1
                if game.lives > 0:
                    Pacman = game.play()
                else:
                    Agent.stop(Pacman)
                    map(Agent.stop, ghosts_group.sprites())
            # pacman ate apple: all ghosts stop for 6 seconds
            elif event.type == ATE_APPLE:
                ghost.slow_down()
            elif event.type == SPEED_UP:
                ghost.speed_up()
            elif event.type == pygame.locals.KEYDOWN:
                all_sprites.update(event.key)

        x = pygame.sprite.spritecollide(Pacman, coins_group, True)
        y = pygame.sprite.spritecollide(Pacman, apples_group, True)
        z = pygame.sprite.spritecollide(Pacman, ghosts_group, False)

        """ len(z) > 0 if Pacman collides with a ghost """
        if len(z) > 0:
            dead = pygame.event.Event(DIED)
            pygame.event.post(dead)

        """ len(y) > 0 if Pacman eats apple """
        if len(y) > 0:
            count = FPS * 6                     # The ghosts stop moving for 6 seconds
            e = pygame.event.Event(ATE_APPLE)
            pygame.event.post(e)

        if count > 0:       # don't change the ghosts' speed for 6 seconds
            count -= 1
        if count == 0:  
            count -= 1      # after 6 seconds increase the speed of ghosts
            s = pygame.event.Event(SPEED_UP)
            pygame.event.post(s)
            
        game.score += len(x)
        game.score += len(y) * 3
        text = font.render("Score: "+ str(game.score), True, (255,255,0))
        if game.lives < 0:
            livestext = font.render("GAME OVER", True, (255,0,0))
        else:
            livestext = font.render("Lives: "+ str(game.lives), True, (255,255,0))
        all_sprites.update()
        all_sprites.draw(SCREEN)
        #SCREEN.blit(DISPSURF, (0, 0))
        pygame.display.update()
        fpsClock.tick(FPS)
    
    print('Score: ' + str(game.score))
