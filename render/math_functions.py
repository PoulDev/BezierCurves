from numpy import ones,vstack
from numpy.linalg import lstsq

def lerp(t, p0, p1):
    return (1 - t) * p0 + t * p1

def line_from_points(p1, p2):
    x_coords, y_coords = zip(p1, p2)
    A = vstack([x_coords,ones(len(x_coords))]).T
    return lstsq(A, y_coords)[0]

def perpendicular(m, q):
    return (-1/m, q)

def get_y_on_line(m, q, x):
    # y = mx + q
    return m * x + q

m, q = line_from_points((0, 1), (-0.5, 0))
print(m, q)
print(perpendicular(m, q))
