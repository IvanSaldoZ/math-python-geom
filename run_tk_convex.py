#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())



setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)


#print("Старое задание: Заданная точка")
#Figure.fixed_point = R2Point(0.0, 0.0)


#print("Задание #73 (Сальдиков): Вершина #1 многоугольника, параллельного осям координат")
#Figure.vertex1 = R2Point(-1.0, -1.0)


#print("Задание #73 (Сальдиков): Вершина #2 многоугольника, параллельного осям координат")
#Figure.vertex2 = R2Point(1.0, 1.0)


tk = TkDrawer()
f = Void()
tk.clean()

def add_pt_and_draw(f, tk, x=None,y=None):
    f = f.add(R2Point(x,y))
    tk.clean()
    f.draw(tk)
    print(f"S = {f.area()}, P = {f.perimeter()}, g = {f.g()}, g73 = {f.g73()}\n")
    return f

print("\nТочки плоскости")
try:
    f = add_pt_and_draw(f, tk, -4.0, 0.0)
    f = add_pt_and_draw(f, tk, 0.0, 4.0)
    f = add_pt_and_draw(f, tk, 4.0, 0.0)
    f = add_pt_and_draw(f, tk, 0.0, -4.0)

    # f = add_pt_and_draw(f, tk, -1.0, -1.0)
    # f = add_pt_and_draw(f, tk, 1.0, 1.0)
    # f = add_pt_and_draw(f, tk, -1.0, 1.0)
#    f = add_pt_and_draw(f, tk, 0.0, -4.0)


    while True:
        f = add_pt_and_draw(f, tk)

except(EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
