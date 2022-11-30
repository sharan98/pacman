import pygame

from utils import Colour, GRID_SIZE

GRID_SIZE = [GRID_SIZE, GRID_SIZE]
COIN_SIZE = [5, 5]

class gridwalls(pygame.sprite.Sprite):
    """ x, y -> x and y co-ordinates """    
    size = []
    def __init__(self, x, y, color = Colour.WHITE, size = GRID_SIZE):
        pygame.sprite.Sprite.__init__(self)

        gridwalls.size = size
        self.image = pygame.surface.Surface(gridwalls.size)
        self.image.fill(color.value)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class apple(pygame.sprite.Sprite):
    def __init__(self, x, y, color = Colour.RED, size = COIN_SIZE):
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        self.image = pygame.surface.Surface(size)     
        self.image.fill(color.value)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.centery = y 

    # def remove(self, group):
    #     Grid.stop = True
    #     super().kill()
    #     pass

class coin(pygame.sprite.Sprite):
    def __init__(self, x, y, color = Colour.ORANGE, size = COIN_SIZE):
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        self.image = pygame.surface.Surface(size)     
        self.image.fill(color.value)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.centery = y 
    

class Grid():
    def __init__(self, maze, mazecolor = Colour.WHITE, coincolor = Colour.ORANGE):
        self.stop = False
        self.maze = maze
        self.mazecolor = mazecolor
        self.coincolor = coincolor
        self.gridwallsList = []
        self.coinsList = []
        self.appleList = []
        # self.listOfGridwalls()
        # self.listOfCoins()
        self.populateGrid()

    # returns list

    def populateGrid(self):
        self.gridwallsList   = [gridwalls(0, 0)]
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 0:
                    # j -> the horizontal co-ordinate;   i -> vertical co-ordinate
                    self.gridwallsList.append(gridwalls(j * gridwalls.size[0], i * gridwalls.size[1], color = self.mazecolor))
                elif self.maze[i][j] == 1:
                    # j -> the horizontal co-ordinate;   i -> vertical co-ordinate
                    self.coinsList.append(coin(j * GRID_SIZE[0] + 15,i * GRID_SIZE[1] + 15, color = self.coincolor))
                elif self.maze[i][j] == 2:
                    c = apple(j * GRID_SIZE[0] + 15,i * GRID_SIZE[1] + 15, color = Colour.RED, size = [5*1.5, 5*1.5])
                    self.appleList.append(c)
                    # self.coinsList.append(c)

    def listOfGridwalls(self):
        self.gridwallsList   = [gridwalls(0, 0)]
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 0:
                    # j -> the horizontal co-ordinate;   i -> vertical co-ordinate
                    self.gridwallsList.append(gridwalls(j * gridwalls.size[0], i * gridwalls.size[1], color = self.mazecolor))
                
    def listOfCoins(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 1:
                    # j -> the horizontal co-ordinate;   i -> vertical co-ordinate
                    self.coinsList.append(coin(j * GRID_SIZE[0] + 15,i * GRID_SIZE[1] + 15, color = self.coincolor))
    
    # def getGridwallsList(self):
    #     return self.gridwallsList
    
    # def getCoinsList(self):
    #     return self.coinsList
