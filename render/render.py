from math import pow, sqrt
from pygame import Surface, draw
from .math_functions import lerp, line_from_points, perpendicular, get_y_on_line
from .theme import *

class Render:
    def __init__(self, screen: Surface):
        self.screen: Surface = screen
        self.points = []

    def prerender_curve(self, t, lines):
        global constant_points
    
        new_points = []
        for index in range(0, len(lines)):
            if index + 1 >= len(lines): break
    
            line = [lines[index], lines[index+1]]
    
            lerp_x = round(lerp(t, line[0][0], line[1][0]), 0)
            lerp_y = round(lerp(t, line[0][1], line[1][1]), 0)
    
            new_points.append([lerp_x, lerp_y])
    
            yield lerp_x, lerp_y, line
    
        if len(new_points) > 1:
            for d in self.prerender_curve(t, new_points):
                yield d
        else:
            if not new_points[0] in self.points:
                self.points.append(new_points[0])
    
    def render_lines(self, t, lines, hide):
        global constant_points
    
        line = None
        rendered_point = None
        rendered_line = None

        for lerp_x, lerp_y, line in self.prerender_curve(t, lines):
            rendered_line = self.adjust_line_to_render(line)
            rendered_point = self.adjust_point_to_render([lerp_x, lerp_y])
    
            if not hide:
                draw.line(self.screen, LINE_COLOR, *rendered_line, 3)
                draw.circle(self.screen, POINT_COLOR, rendered_point, 5)
        
        if rendered_line is None or rendered_point is None: return

        draw.line(self.screen, (0, 255, 0), *rendered_line, 3)
        m, q = line_from_points(*rendered_line)
        x1, x2 = 0, 1000 #rendered_point[0]-100, rendered_point[0]+100 #0, 1000
        y1, y2 = get_y_on_line(m, q, x1), get_y_on_line(m, q, x2)
        draw.line(self.screen, (0, 0, 255), (x1, y1), (x2, y2), 5)

        pm = -1/m
        pq = rendered_point[1] - rendered_point[0] * pm

        x1, x2 = -1000, 1000 
        y1, y2 = get_y_on_line(pm, pq, x1), get_y_on_line(pm, pq, x2)

        draw.line(self.screen, (0, 255, 255), (x1, y1), (x2, y2), 5)

        draw.line(self.screen, (255, 0, 0), (x1, y1), (x2, y2), 2)

    def prerender_lines(self, lines, hide):
        for t_step in range(0, 1001):
            t = t_step / 1000
            for _ in self.prerender_curve(t, lines): pass # Pre-render the Bezier line
                                                  # Ignoring yields

            for index in range(0, len(lines)):
                if index + 1 >= len(lines): break
                if not hide:
                    line = self.adjust_line_to_render([lines[index], lines[index+1]])
                    draw.line(self.screen, LINE_COLOR, *line, 5)

    def adjust_point_to_render(self, point):
        point = point.copy()
        point[1] *= -1
        point[0] += 450
        point[1] += 250
        return point
    
    def return_point_to_normal(self, point):
        point = point.copy()
        point[1] -= 250
        point[0] -= 450
        point[1] *= -1
        return point
    
    def adjust_line_to_render(self, line):
        point1 = line[0].copy()
        point2 = line[1].copy()
    
        point1 = self.adjust_point_to_render(point1)
        point2 = self.adjust_point_to_render(point2)
    
        return [point1, point2]

    def distance(self, p0, p1):
        return sqrt(pow(p1[0] - p0[0], 2) + pow(p1[1] - p0[1], 2))

    def nearest_multiplier(self, number, base):
        distance = number % base
        if distance > base / 2:
            return number + base - distance
        else:
            return number - distance
