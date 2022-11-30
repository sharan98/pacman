import logging
import time
import pygame
from utils import *#DOWN, LEFT, RIGHT, STOP, UP, Colour, GRID_SIZE

logging.basicConfig(filename='agent.log',level=logging.DEBUG)

class Agent(pygame.sprite.Sprite):
    """ Parent class for pacman and ghosts """

    # pacman_position is class variable because the ghosts need it
    pacman_position = pygame.rect
    dead = False
    grid = None

    def set_grid(g):
        Agent.grid = g
    staticmethod(set_grid)

    # grid -> Grid object has maze, lists of gridwalls and coins
    def __init__(self, color, pos, grid):
        pygame.sprite.Sprite.__init__(self)
        self.grid = grid
        # print (self.grid.stop)
        self.gridlist = grid.gridwallsList

        """ MUST BE EVEN """
        width = height = 16

        # Create an image of the block, and fill it with a color.
        self.image = pygame.surface.Surface([width, height])
        self.image.fill(color.value)
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

    """ True if Agent will collide with wall in the new direction"""
    def willHitWall(self, newdirection):
        
        """ displace by (grid_size - agent-size)/2 + 1 in newdirection """
        displace = newdirection * ((GRID_SIZE - self.rect.width) / 2 + 1) # [i * ((GRID_SIZE - self.rect.width) / 2 + 1) for i in newdirection]

        future_pos = self.rect.move(displace)
        if future_pos.collidelist([l.rect for l in self.gridlist]) == -1:
            return False
        return True
    
    """ Adjusts the position to align with the center of the path """
    def adjust(self):
        x = self.rect.centerx
        y = self.rect.centery
        
        """ If moving horizontally, change the y co-odinate of the center """
        if self.speed[1] == 0:
            # if y % (GRID_SIZE + GRID_SIZE / 2) != 0:
            y = (y // GRID_SIZE) * GRID_SIZE + 15
            self.rect.centery = y
        
        """ If moving vertically, change the x co-ordinate of the center """
        if self.speed[0] == 0:
            # if x % (GRID_SIZE + GRID_SIZE / 2) != 0:
            x = (x // GRID_SIZE) * GRID_SIZE + 15
            self.rect.centerx = x

    def stop(agent):
        Agent.dead = True
        # agent.speed = STOP * 1
    staticmethod(stop)


class pacman(Agent):

    # Constructor. Pass in the color of the block,
    # pos -> [x, y] ------- co-ordinates of the CENTER of sprite
    # grid -> Grid object
    def __init__(self, color, pos, grid):
        Agent.__init__(self, color, pos, grid)
        self.speed = RIGHT * PAC_SPEED
        self.direction = RIGHT
        Agent.pacman_position = self.rect



    def update(self, key = None):
        newdirection = self.direction

        """ update new direction according to key pressed """
        if key == pygame.K_UP:
            newdirection = UP #* 3
        elif key == pygame.K_RIGHT:
            newdirection = RIGHT #* 3
        elif key == pygame.K_DOWN:
            newdirection = DOWN #* 3
        elif key == pygame.K_LEFT:
            newdirection = LEFT #* 3
        else:
            pass
        
        """ move a copy of the rectangle slightly in the new direction
            and check if pacman will collide with the grid wall """
        
        # eg -  newspeed = [0, 3] -> displace = [0, 11] (self.rect.width // 2 + 1)
        # displace = newdirection * ((GRID_SIZE - self.rect.width) / 2 + 1) # [i * ((GRID_SIZE - self.rect.width) / 2 + 1) for i in newdirection]
        if not self.willHitWall(newdirection):
            """ if there will not be a collision """
            self.direction = newdirection
            self.speed = newdirection * PAC_SPEED
        elif self.speed == newdirection * PAC_SPEED:
            """ if there is a head-on collision """
            self.speed = STOP       # STOP MUST be multiplied by any integer


        if (Agent.dead):
            self.speed = STOP * 1
         # update coordinates of pacman
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1] 
        self.adjust()
        Agent.pacman_position = self.rect



class ghost(Agent):

    speed_scale = 1
    
    def __init__(self, color, pos, direction, grid, id):
        Agent.__init__(self, color, pos, grid)
        # ghost slower than pacman
        self.speed = direction * GHOST_SPEED #2
        self.id = id
        self.direction = direction
    
    def slow_down():
        ghost.speed_scale = 0
    staticmethod(slow_down)

    def speed_up():
        ghost.speed_scale = 1
    staticmethod(speed_up)


    def update(self, key = None):
        me = (self.rect.centery // GRID_SIZE, self.rect.centerx // GRID_SIZE)
        if self.id == BLINKY:
            pac = (Agent.pacman_position.centery // GRID_SIZE, Agent.pacman_position.centerx // GRID_SIZE)
        elif self.id == INKY:
            pac = (Agent.pacman_position.centery // GRID_SIZE + 4, Agent.pacman_position.centerx // GRID_SIZE)
            if abs(me[0] - pac[0]) < 2 or abs(me[1] - pac[1]) < 2:
                pac = (15, 1)
        elif self.id == BLUE:
            pac = (Agent.pacman_position.centery // GRID_SIZE, Agent.pacman_position.centerx // GRID_SIZE + 4)
            if abs(me[0] - pac[0]) < 2 or abs(me[1] - pac[1]) < 2:
                pac = (9, 9)
        else:
            pac = (Agent.pacman_position.centery // GRID_SIZE, Agent.pacman_position.centerx // GRID_SIZE)

        # coord = (self.rect.centery / GRID_SIZE, self.rect.centerx / GRID_SIZE)
        p = []
        
        # the functions writes into the list p
        astar(self.grid.maze, me, pac, p)
        oldspeed = self.direction * (GHOST_SPEED * ghost.speed_scale)
        newdirection = self.direction
        # p = p[::-1]
        p.reverse()
        try:
            next_pos = p[1]
            if me[0] == next_pos[0]:
                if me[1] > next_pos[1]:
                    newdirection = LEFT #* 2
                else:
                    newdirection = RIGHT #* 2
            else:
                if me[0] > next_pos[0]:
                    newdirection = UP #* 2
                else:
                    newdirection = DOWN #* 2


            # displace = newdirection * ((GRID_SIZE - self.rect.width) / 2 + 1) #[i * ((GRID_SIZE - self.rect.width) / 2 + 1) for i in newdirection]
            if not self.willHitWall(newdirection):
                self.direction = newdirection
                self.speed = newdirection * (GHOST_SPEED * ghost.speed_scale)
            else:
                self.speed = oldspeed
        except:
            self.speed = oldspeed #STOP * 2
            pass

        if Agent.dead:
            self.speed = STOP
            
        # print(self.speed)
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.adjust()




class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position



def astar(maze, start, end, path):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    s_time = time.time()
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    l = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    # Loop until you find the end
    while len(open_list) > 0:
    # for k in range(2):

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        children = []
        # Found the goal
        k = time.time() - s_time
        if current_node == end_node or k > 0.011: # time.time() - s_time > 0.06:
            # path = []
            if k > 0.011: # time.time() - s_time > 0.07:
                # logging.info('\nStopping func, Time elapsed: {0}'.format(k))
                pass
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            # return path[::-1] # Return reversed path
            # e_time = time.time()
            # # logging.info('Time elapsed: {0}'.format(e_time - s_time))
            return
       
        # Generate children
        for new_position in l: #[(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 1:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)
        # print('children:   '+ str(children))
        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
        
    # return closed_list[1].position
