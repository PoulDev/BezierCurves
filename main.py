import pygame

WIDTH, HEIGHT = 500, 500

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
running = True

class Bezier:
    t = 0.5

    """
        Funzione Lerp
    """
    def lerp(self, p0, p1):
        return (1 - self.t) * p0 + self.t * p1

def render_lines(screen, lines):
    global constant_points

    new_points = []
    for index in range(0, len(lines)):
        if index + 1 >= len(lines): break

        line = [lines[index], lines[index+1]]

        lerp_x = bezier.lerp(line[0][0], line[1][0])
        lerp_y = bezier.lerp(line[0][1], line[1][1])

        rendered_line = adjust_line_to_render(line)
        rendered_point = adjust_point_to_render([lerp_x, lerp_y])

        new_points.append([lerp_x, lerp_y])

        pygame.draw.line(screen, (100, 100, 100), *rendered_line, 2)
        pygame.draw.circle(screen, (255, 0, 0), rendered_point, 3)

    if len(new_points) > 1:
        render_lines(screen, new_points)
    else:
        if not new_points[0] in constant_points:
            constant_points.append(new_points[0])

def adjust_point_to_render(point):
    point = point.copy()
    point[1] *= -1
    point[0] += 150
    point[1] += 250
    return point

def return_point_to_normal(point):
    point = point.copy()
    point[1] -= 250
    point[0] -= 150
    point[1] *= -1
    return point

def adjust_line_to_render(line):
    point1 = line[0].copy()
    point2 = line[1].copy()

    point1 = adjust_point_to_render(point1)
    point2 = adjust_point_to_render(point2)

    return [point1, point2]

bezier = Bezier()

d = 200
lines = [[0, 0], [0, d], [100, -50], [d, 0]]
constant_points = []
selected_point = None

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                lines[selected_point] = return_point_to_normal(list(event.pos))
                constant_points = []

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                selected_point = int(event.unicode) - 1

    render_lines(screen, lines)
    for point in constant_points:
        pygame.draw.circle(screen, (0, 255, 255), adjust_point_to_render(point), 1)
    
    if not selected_point is None:
        pygame.draw.circle(screen, (255, 255, 255), adjust_point_to_render(lines[selected_point]), 5)
    

    bezier.t += 0.001
    if bezier.t > 1:
        bezier.t = 0

    pygame.display.flip()
