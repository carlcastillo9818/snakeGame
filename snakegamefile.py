import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(): # the cubes in the game
    rows = 20
    w = 500

    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)):
        self.pos = start # set start pos
        self.dirnx = 1 # set x coord
        self.dirny = 0 # set y coord
        self.color = color # set the color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx # adjust x and y directions
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) # adjust x and y pos in the tuple pos
    def draw(self, surface, eyes = False):
        distance = self.w // self.rows # space between x and y coords
        i = self.pos[0] # current row
        j = self.pos[1] # current column

        pygame.draw.rect(surface, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance -2)) # draw the cube and allows you to see white lines on the grid still
        if eyes: # aligns the snake eyes perfectly on the cube
            centre = distance // 2
            radius = 3
            circleMiddle = (i *distance + centre - radius, j * distance + 8)
            circleMiddle2 = (i * distance +distance - radius * 2, j * distance + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(): # The Snake of the game
    body = [] # LIST of cubes

    turns = {} # dictionary containing turns
    def __init__(self, color, pos):
        self.color = color # snake color
        self.head = cube(pos) # head of the snake at a given position
        self.body.append(self.head) # attach the head to the ordered list
        self.dirnx = 0 # x direction
        self.dirny = 1 # y direction

    def move(self):
        for event in pygame.event.get(): # check for events (like moving)
            if(event.type == pygame.QUIT):
                pygame.quit()
            keys = pygame.key.get_pressed() # dictionary of keys
            for key in keys: # for loop that checks for arrow keys pressed
                if (keys[pygame.K_LEFT]):
                    self.dirnx = -1 # move in the left direction (negative x)
                    self.dirny = 0 # y stays at 0, cant move in two directions at same time
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # we have a new turn at this position and our snake moved left

                elif (keys[pygame.K_RIGHT]):
                    self.dirnx = 1 # move in the right direction (pos x)
                    self.dirny = 0 # y stays at 0, cant move in two directions at same time
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # we have a new turn at this position and our snake moved right

                elif (keys[pygame.K_UP]):
                    self.dirnx = 0
                    self.dirny = -1 # move in the up direction (neg y)
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # we have a new turn at this position and our snake moved up

                elif (keys[pygame.K_DOWN]):
                    self.dirnx = 0
                    self.dirny = 1 # move in the down direction (pos y)
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # we have a new turn at this position and our snake moved down

        for i, c in enumerate(self.body): # look through list of positions we have to move cube
            p = c.pos[:] # makes a copy of the cubes pos and stores it in p
            if p in self.turns: # if p (position) is in the turns dictionary then we will turn
                turn = self.turns[p]
                c.move(turn[0], turn[1]) # give x and y positions
                if(i == len(self.body) -1): # if on the last cube, remove that turn, else you will auto change direction which is bad
                    self.turns.pop(p) # remove the turn
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: # if we are on the left edge of the screen
                    c.pos = (c.rows - 1, c.pos[1]) # change position so we go to right side
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1: # if moving right and edge of screen
                    c.pos = (0, c.pos[1]) # change so we go to left side
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1: # if we are going down and at the edge
                    c.pos = (c.pos[0], 0) # go to top of screen
                elif c.dirny == -1 and c.pos[1] <= 0: # if we are going up and hitting edge of screen
                    c.pos = (c.pos[0], c.rows - 1) # change so we go down
                else: # not going to any edges
                    c.move(c.dirnx, c.dirny) # move cube in whatever direction its going

    def reset(self, pos):
        pass

    def addCube(self):
        tail = self.body[-1] # last item in the list
        dx,dy = tail.dirnx, tail.dirny # set x and y directions

        ''' check which direction you are currently moving in, the tail of the cube.
         so that you can then make sure when you add cube, you know where to add it (above it, below it), 
         give it correct direction 
         '''
        if dx == 1 and dy == 0: # going right
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1]))) # add cube to the left side of snake body
        elif dx == -1 and dy == 0: # going left
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1]))) # add cube to the right side of snake body
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        # set direction for cube (so it moves somewhere)
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if(i == 0): # when drawing first snake obj, add eyes to it
                c.draw(surface,True) # draw eyes if its the first one in the list (the True parameter allows that)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface): # draws the grid for the game
    sizeBtwn = w // rows # the gap between each line (division calculation)
    x = 0
    y = 0
    for p in range(rows): # draws multiple WHITE lines
        x += sizeBtwn # updates the x coordinate
        y += sizeBtwn # updates the y coord
        pygame.draw.line(surface, (255,255,255), (x, 0), (x,w)) # draws vertical lines
        pygame.draw.line(surface, (255,255,255), (0, y), (w,y)) # draws horizontal lines


def redrawWindow(surface): # updates the window
    global rows, width, s, snack # makes the rows and width vars global so they can be used in any func
    surface.fill((0,0,0)) # make the window black
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface) # draws the grid on the surface with the provided width and rows
    pygame.display.update() # update the screen

def randomSnack(rows, item):
    positions = item.body

    while(True):
        x = random.randrange(rows)
        y = random.randrange(rows)
        if(len(list(filter(lambda z:z.pos == (x,y), positions))) > 0): # get list of filtered list and see if any positions are the same as current pos of snake
            # avoid putting snack on top of snake
            continue
        else:
            break

    return (x,y) # generates snack on random pos

def message_box(subject, content):
    pass

def main():


    global width, rows, s, snack
    width = 500 # width for the game window
    rows = 20 # number of rows that the snake can move in
    win = pygame.display.set_mode((width, width)) # GAME WINDOW
    gameTitle = pygame.display.set_caption("Snake Game!!!") # set title for the window
    s = snake((255, 0, 0), (10, 10)) # SNAKE OBJECT
    snack = cube(randomSnack(rows, s), color = (0,255,0))
    myFlag = True

    clock = pygame.time.Clock() # game clock object

    while(myFlag): # main game loop
        pygame.time.delay(50) # delay by 50 ms so program doesnt run super fast, the lower the faster
        clock.tick(10) # keeps game at 10 FPS so snake can move 10 blocks in a second, play around with this, the lower the slower
        s.move() # moves the snake

        if(s.body[0].pos == snack.pos): # if the snakes head is touching the snack
            s.addCube() # add cube to the snake (making it longer)
            snack = cube(randomSnack(rows, s), color = (0,255,0)) # generate new snack

        # START VIDEO AT 1:29:38
        # LAST WORKED ON 1/9/21
        # ALMOST DONE WITH THIS GAME


        redrawWindow(win) # call the redraw func

main()
