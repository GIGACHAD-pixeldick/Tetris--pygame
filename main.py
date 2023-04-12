import pygame as pg
from copy import deepcopy
from random import choice, randrange

WEIGHT, HEIGHT = 10, 20
TILE = 45
RESOLUTION = WEIGHT * TILE, HEIGHT * TILE
FPS = 60

pg.init()
game_sc = pg.display.set_mode(RESOLUTION)
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

def check_borders():
    if figure[i].x < 0 or figure[i].x > WEIGHT - 1:
        return False
    elif figure[i].y > HEIGHT - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

while True:
    dx = 0
    game_sc.fill(pg.Color('black'))
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
        figure_old = deepcopy(choice(figures))
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = pg.Color('white')
                figure = deepcopy(choice(figures))
                animation_limit = 2000
                break

    # draw grid
    [pg.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    
    # draw figure 
    for i in range(4):
        figures_rect.x = figure[i].x * TILE
        figures_rect.y = figure[i].y * TILE
        pg.draw.rect(game_sc, pg.Color('white'), figures_rect)

    # draw field
    for y, row in enumerate(field):
        for x, col in enumerate(row):
            if col:
                figures_rect.x, figures_rect.y = x * TILE, y * TILE
                pg.draw.rect(game_sc, col, figure_rect)

    pg.display.flip()
    clock.tick(FPS)