#!/usr/bin/env -S python3 -B
from convex import Void
from r2point import R2Point


# print("Старое задание: Заданная точка")
# Figure.fixed_point = R2Point(0.0, 0.0)

print("Задание #73 (Сальдиков): Вершина #1 правильного прямоугольника")
#vertex1 = R2Point(-1.0, -1.0)
vertex1 = R2Point()

print("Задание #73 (Сальдиков): Вершина #2 (противоположная) правильного прямоугольника")
#vertex2 = R2Point(1.0, 1.0)
vertex2 = R2Point()


def add_pt(f, x=None, y=None):
    f = f.add(R2Point(x, y))
    print(f"S = {f.area()}, P = {f.perimeter()}, g73 = {f.g73()}\n")
    return f


print("\nТочки плоскости")
f = Void(vertex1, vertex2)
try:
    # f = add_pt(f, -4.0, 0.0)
    # f = add_pt(f, 0.0, 4.0)
    # f = add_pt(f, 4.0, 0.0)
    # f = add_pt(f, 0.0, -4.0)
    # print(f"S = {f.area()}, P = {f.perimeter()}, g73 = {f.g73()}\n")

    while True:
        f = add_pt(f)

except(EOFError, KeyboardInterrupt):
    print("\nStop")
