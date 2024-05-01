from numpy import random
import pygame
from render.render import Render
from render.theme import *
import time
from render.math_functions import line_from_points, perpendicular, get_y_on_line

t = 0
running = True

print('''
------- COMMANDS -------
(n) New Point 
(m) Delete point
(i) Enable/Disable Instant Rendering
(h) Hide/Show construction lines
(g) Enable/Disable grid

Select and move a point using the mouse
      ''')

# Base Configuration
t_precision = 10000
lines = [[-100, -100], [100, 200], [300, -100]]
WIDTH, HEIGHT = 1000, 750
GRID_SIZE = 25

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
render = Render(screen)

# Options
grid = False
hide = False
prerender = False

# Mouse Stuff
selected_point = None
mouse_down = False
mouse_active = False
mouse_position = [WIDTH // 2, HEIGHT // 2]
pointed_point = None

while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mouse_down = True
                if pointed_point is not None:
                    selected_point = pointed_point
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                mouse_down = False
                pointed_point = None
                selected_point = None

        elif event.type == pygame.MOUSEMOTION:
            mouse_position = list(event.pos)
            if mouse_down and not selected_point is None:
                pos = [
                    render.nearest_multiplier(event.pos[0], GRID_SIZE),
                    render.nearest_multiplier(event.pos[1], GRID_SIZE)
                ] if grid else list(event.pos)
                lines[selected_point] = render.return_point_to_normal(pos)
                render.points = []

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_n:
                lines.append(render.return_point_to_normal(mouse_position))
                render.points = []
                t = 0

            elif event.key == pygame.K_m:
                if selected_point:
                    lines.pop(selected_point)
                else:
                    lines.pop(-1)
                render.points = []
                selected_point = None
                t = 0
            elif event.key == pygame.K_i:
                prerender = not(prerender)
                render.points = []
            elif event.key == pygame.K_h:
                hide = not(hide)
            elif event.key == pygame.K_g:
                grid = not(grid)

    # Grid

    if grid:
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (10, 10, 10), (1, x), (WIDTH, x), 2)
            pygame.draw.line(screen, (10, 10, 10), (x, 1), (x, WIDTH), 2)

    if prerender: # Render the Bezier Curve in a single frame
        render.prerender_lines(lines, hide)
    else:
        render.render_lines(t / t_precision, lines, hide)

    # Find the nearest point to the mouse
    mouse_active = False
    for index, point in enumerate(lines):
        point = render.adjust_point_to_render(point)
        if render.distance(mouse_position, point) < 10:
            mouse_active = True
            pointed_point = index
        elif pointed_point is not None and index == pointed_point:
            pointed_point = None

    # Render the Bezier Curve
    for index, point in enumerate(render.points):
        pygame.draw.circle(screen, BEZIER_CURVE_COLOR, render.adjust_point_to_render(point), 2)

    '''
    print('finished rendering', point)
    previous_point = render.points[index-1]
    m, q = line_from_points(point, previous_point)
    #perp_m, perp_q = perpendicular(derivate_m, derivate_q)
    x1, x2 = -50, 50
    y1 = get_y_on_line(m, q, x1)
    y2 = get_y_on_line(m, q, x2)
    pygame.draw.line(screen, (255, 0, 0), render.adjust_point_to_render([x1, y1]), render.adjust_point_to_render([x2, y2]), 2)
    '''


    pygame.draw.circle(screen, MOUSE_DEFAULT, (mouse_position), 10 if not(mouse_active) else 4, 2)

    t += 5
    t %= t_precision + 1

    pygame.display.flip()
