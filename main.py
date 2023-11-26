import pygame
from render.render import Render
from render.theme import *

t = 0
t_precision = 10000

print('''
------- COMMANDS -------
(n) New Point 
(m) Delete point
(p) Enable/Disable PreRendering

Select and move a point using the mouse
      ''')

WIDTH, HEIGHT = 1000, 750

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
render = Render(screen)

lines = [[0, 0], [0, 200], [200, 200]]
running = True
selected_point = None
mouse_down = False
prerender = False
mouse_active = False
mouse_position = [WIDTH // 2, HEIGHT // 2]
pointed_point = None
hide = False

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
                lines[selected_point] = render.return_point_to_normal(list(event.pos))
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
            elif event.key == pygame.K_p:
                prerender = not(prerender)
                render.points = []
            elif event.key == pygame.K_h:
                hide = not(hide)

    if not prerender:
        render.render_lines(t / t_precision, lines, hide)
    else:
        render.prerender_lines(lines, hide)

    mouse_active = False
    for index, point in enumerate(lines):
        point = render.adjust_point_to_render(point)
        if render.distance(mouse_position, point) < 10:
            mouse_active = True
            pointed_point = index

    for point in render.points:
        pygame.draw.circle(screen, BEZIER_CURVE_COLOR, render.adjust_point_to_render(point), 2)

    pygame.draw.circle(screen, MOUSE_DEFAULT, (mouse_position), 10 if not(mouse_active) else 4, 2)

    t += 5
    t %= t_precision + 1

    print(mouse_position)

    pygame.display.flip()
