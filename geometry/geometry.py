from math import sqrt


class Point:
    def __init__(self, x=0., y=0.):
        self.x = x
        self.y = y

    def mag(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

class Line:
    def __init__(self, pt_a, pt_b):
        self.pt_a = pt_a
        self.pt_b = pt_b

class Triangle:
    def __init__(self, vertices):
        self.vertices = vertices

    def centroid(self):
        return sum(self.vertices) / 3.

    def area(self):
        pass


def dot(u, v):
    return u.x * v.x + u.y * v.y


def cross(u, v):
    return u.x * v.y - u.y * v.x
