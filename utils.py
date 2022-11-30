from enum import Enum, unique

@unique     
class Colour(Enum):
    """ Usage: Colour.RED, Colour.Yellow """
    NAVYBLUE    =  (60, 60, 100)
    WHITE       =  (255, 255, 255)
    RED         =  (255, 0, 0)
    GREEN       =  (0, 255, 0)
    YELLOW      =  (255, 255, 0)
    ORANGE      =  (255, 128, 0)
    CYAN        =  (0, 255, 255)
    BLACK       =  (0, 0, 0)

class Direction(list):
    """ Direction like UP, LEFT etc are lists """
    def __init__(self, val):
        # val is a list
        super().__init__(val)
        self.__direction = val

    """ used for speed, i.e., UP * 2 will be [0,-2] and UP * 3 will be [0, -3] """
    """ For changing the speed """
    """ Pacman: UP * 3 and ghosts: UP * 2 .... generally """
    def __mul__(self, n):
        return [i * n for i in self.__direction]

    def __call__(self):
        return self.__direction

UP      = Direction([0, -1])
DOWN    = Direction([0, 1])
LEFT    = Direction([-1, 0])
RIGHT   = Direction([1, 0])
STOP    = Direction([0, 0])

GRID_SIZE   = 30

BLINKY  = 1
INKY    = 2
BLUE    = 3
CLYDE   = 4

PAC_SPEED   = 3
GHOST_SPEED = 1.8