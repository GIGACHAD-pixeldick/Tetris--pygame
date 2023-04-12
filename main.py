import pygame as pg
from copy import deepcopy
from random import choice, randrange

WEIGHT, HEIGHT = 10, 20
TILE = 45
GAME_RESOLUTION = WEIGHT * TILE, HEIGHT * TILE
RES = 750, 940 
FPS = 60

pg.init()
sc = pg.display.set_mode(RES)
game_sc = pg.Surface(GAME_RESOLUTION)
clock = pg.time.Clock()

grid = [pg.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WEIGHT) for y in range(HEIGHT)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]             

figures = [[pg.Rect(x + WEIGHT // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figures_rect = pg.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(WEIGHT)] for j in range(HEIGHT)]

animation_count, animation_speed, animation_limit = 0, 60, 2000
figure = deepcopy(choice(figures))

bg = pg.image.load('resources/bg.jpg').convert()
game_bg = pg.image.load('resources/gamebg.png').convert()

#main_font = pg.font.Font('resources/font.ttf').convert()

get_color = lambda: (randrange(30, 256), randrange(30,256), randrange(30, 256))
color = get_color()

def check_borders():
    if figure[i].x < 0 or figure[i].x > WEIGHT - 1:
        return False
    elif figure[i].y > HEIGHT - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

while True:
    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    # control
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                dx = -1
            elif event.key == pg.K_RIGHT:
                dx = 1
            elif event.key == pg.K_DOWN:
                animation_limit = 100
            elif event.key == pg.K_UP:
                rotate = True
    
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break

    # move y
    animation_count += animation_speed
    if animation_count > animation_limit:
        animation_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                color = get_color()
                figure = deepcopy(choice(figures))
                animation_limit = 2000
                break

    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

    # check lines
    line = HEIGHT - 1
    for row in range(HEIGHT - 1, -1, -1):
        count = 0
        for i in range(WEIGHT):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < WEIGHT:
            line -= 1

    # draw grid
    [pg.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    
    # draw figure 
    for i in range(4):
        figures_rect.x = figure[i].x * TILE
        figures_rect.y = figure[i].y * TILE
        pg.draw.rect(game_sc, color, figures_rect)

    # draw field
    for y, row in enumerate(field):
        for x, col in enumerate(row):
            if col:
                figures_rect.x, figures_rect.y = x * TILE, y * TILE
                pg.draw.rect(game_sc, col, figures_rect)

    pg.display.flip()
    clock.tick(FPS)