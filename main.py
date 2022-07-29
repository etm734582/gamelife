import pygame as pg
import numpy as np
import random
import requests


# vars
pg.init()
CELLSIZE = 10
GRIDSIZE = 50
WIDTH = CELLSIZE * GRIDSIZE
HEIGHT = CELLSIZE * GRIDSIZE
FPS = 30
sc = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

isplacingcells = False
iskillingcells = False
ischeckingcells = False

# grid
grid = np.array([0 for i in range(GRIDSIZE ** 2)]).reshape(GRIDSIZE, GRIDSIZE)

# functions
def checkcells():
    global grid

    setalive = []
    setdie = []

    for row in range(GRIDSIZE):
        for col in range(GRIDSIZE):
            borderingcells = 0
            isalive = False
            if grid[row][col] == 1:
                isalive = True

            # if row>0 and col > 0 and row<GRIDSIZE and col<GRIDSIZE:
            #     print(row,col)
            #     print(grid[row-1][col])
            #     print(grid[row][col+1])
            #     print(grid[row+1][col])
            #     print(grid[row][col-1])
            #     print(grid[row-1][col-1])
            #     print(grid[row-1][col+1])
            #     print(grid[row+1][col+1])
            #     print(grid[row+1][col-1])
            #     print('===================')

            if row - 1 > -1:
                if grid[row - 1][col] == 1:
                    borderingcells += 1
            if col + 1 < GRIDSIZE:
                if grid[row][col + 1] == 1:
                    borderingcells += 1
            if row + 1 < GRIDSIZE:
                if grid[row + 1][col] == 1:
                    borderingcells += 1
            if col - 1 > -1:
                if grid[row][col - 1] == 1:
                    borderingcells += 1

            if row - 1 > -1 and col - 1 > -1:
                if grid[row - 1][col - 1] == 1:
                    borderingcells += 1
            if row - 1 > -1 and col + 1 < GRIDSIZE:
                if grid[row - 1][col + 1] == 1:
                    borderingcells += 1
            if row + 1 < GRIDSIZE and col + 1 < GRIDSIZE:
                if grid[row + 1][col + 1] == 1:
                    borderingcells += 1
            if row + 1 < GRIDSIZE and col - 1 > -1:
                if grid[row + 1][col - 1] == 1:
                    borderingcells += 1


            if isalive == False and 4 > borderingcells > 2:
                setalive.append((row,col))

            if isalive and (3 < borderingcells or 2 > borderingcells):
                setdie.append((row,col))

    for cell in setalive:
        grid[cell] = 1

    for cell in setdie:
        grid[cell] = 0

def setcellsalive():
    global grid
    global mouse_pos

    mouse_pos = pg.mouse.get_pos()
    mouse_pos_x = mouse_pos[0]
    mouse_pos_y = mouse_pos[1]
    cords = (mouse_pos_y//CELLSIZE, mouse_pos_x//CELLSIZE)

    if grid[cords] == 0:
        grid[cords] = 1

def setcellsempty():
    global grid
    global mouse_pos

    mouse_pos = pg.mouse.get_pos()
    mouse_pos_x = mouse_pos[0]
    mouse_pos_y = mouse_pos[1]
    cords = (mouse_pos_y//CELLSIZE, mouse_pos_x//CELLSIZE)

    if grid[cords] == 1:
        grid[cords] = 0


# mainloop
while True:
    sc.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                isplacingcells = True
            if event.button == 3:
                iskillingcells = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                ischeckingcells = False
            if event.key == pg.K_UP:
                ischeckingcells = True

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                isplacingcells = False
            if event.button == 3:
                iskillingcells = False

    for col in range(GRIDSIZE):
        for row in range(GRIDSIZE):
            if grid[col][row] == 1:
                pg.draw.rect(sc, (0, 0, 0), ((row) * CELLSIZE, (col) * CELLSIZE, CELLSIZE, CELLSIZE))
                pg.draw.rect(sc, (0, 150, 150), ((row) * CELLSIZE+1, (col) * CELLSIZE+1, CELLSIZE-1, CELLSIZE-1))

    if ischeckingcells:
        checkcells()
    if isplacingcells:
        setcellsalive()
    if iskillingcells:
        setcellsempty()

    print(ischeckingcells)

    pg.display.update()
    clock.tick(FPS)
