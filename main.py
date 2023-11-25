import pygame

WIDTH, HEIGHT = 1000, 750

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
running = True

BACKGROUND = (20, 20, 30)
LINE_COLOR = (70, 70, 70)
POINT_COLOR = (200, 0, 0)
MAIN_POINT_COLOR = (50, 150, 50)
BEZIER_CURVE_COLOR = (0, 200, 200)

class Bezier:
    t = 0.5

    """
        Funzione Lerp
    """
    def lerp(self, p0, p1):
        return (1 - self.t) * p0 + self.t * p1

def prerender_curve(lines):
    global constant_points

    new_points = []
    for index in range(0, len(lines)):
        if index + 1 >= len(lines): break

        line = [lines[index], lines[index+1]]

        lerp_x = bezier.lerp(line[0][0], line[1][0])
        lerp_y = bezier.lerp(line[0][1], line[1][1])

        new_points.append([lerp_x, lerp_y])

        yield lerp_x, lerp_y, line

    if len(new_points) > 1:
        for d in prerender_curve(new_points):
            yield d
    else:
        if not new_points[0] in constant_points:
            constant_points.append(new_points[0])

def render_lines(screen, lines):
    global constant_points

    for lerp_x, lerp_y, line in prerender_curve(lines):
        rendered_line = adjust_line_to_render(line)
        rendered_point = adjust_point_to_render([lerp_x, lerp_y])

        pygame.draw.line(screen, LINE_COLOR, *rendered_line, 5)
        pygame.draw.circle(screen, POINT_COLOR, rendered_point, 5)


def adjust_point_to_render(point):
    point = point.copy()
    point[1] *= -1
    point[0] += 450
    point[1] += 250
    return point

def return_point_to_normal(point):
    point = point.copy()
    point[1] -= 250
    point[0] -= 450
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
lines = [[0, 0], [0, d], [d, d]]
constant_points = []
selected_point = None
mouse_down = False
prerender = False
mouse_position = [WIDTH // 2, HEIGHT // 2]

print('''
----- COMANDI -----
(n) New Point 
(m) Delete point
(p) Switch PreRendering

Use the numpad to select a point
      ''')

while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                mouse_down = False


        elif event.type == pygame.MOUSEMOTION:
            mouse_position = list(event.pos)
            if mouse_down and not selected_point is None:
                lines[selected_point] = return_point_to_normal(list(event.pos))
                constant_points = []

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                selected_point = int(event.unicode) - 1
            elif event.key == pygame.K_n:
                lines.append([50, 50])
                constant_points = []
            elif event.key == pygame.K_m:
                if selected_point:
                    lines.pop(selected_point)
                else:
                    lines.pop(-1)
                constant_points = []
                selected_point = None
            elif event.key == pygame.K_p:
                prerender = not(prerender)
                constant_points = []

    if not prerender:
        render_lines(screen, lines)
    else:
        for t in range(0, 1001):
            bezier.t = t / 1000
            for _ in prerender_curve(lines): pass # Pre-render della linea di Bezier
                                                  # Ignorando le linee per la costruzione
                                                  # Di questa.

            for index in range(0, len(lines)):
                if index + 1 >= len(lines): break
                line = adjust_line_to_render([lines[index], lines[index+1]])
                pygame.draw.line(screen, LINE_COLOR, *line, 5)

    for point in constant_points:
        pygame.draw.circle(screen, BEZIER_CURVE_COLOR, adjust_point_to_render(point), 1)
    
    if not selected_point is None:
        pygame.draw.circle(screen, POINT_COLOR, adjust_point_to_render(lines[selected_point]), 7)
    

    bezier.t += 0.0008
    if bezier.t > 1:
        bezier.t = 0

    pygame.display.flip()
