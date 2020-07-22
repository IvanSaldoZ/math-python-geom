#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Figure, Void, Polygon, Point, Segment

#print("Заданная точка")
#Figure.fixed_point = R2Point(0.0, 0.0)
#print("Задание #73 (Сальдиков): Вершина #1 многоугольника, параллельного осям координат")
#Figure.vertex1 = R2Point(-1.0, -1.0)
#print("Задание #73 (Сальдиков): Вершина #2 многоугольника, параллельного осям координат")
#Figure.vertex2 = R2Point(1.0, 1.0)

def add_pt(f, x=None,y=None):
    f = f.add(R2Point(x,y))
    print(f"S = {f.area()}, P = {f.perimeter()}, g = {f.g()}, g73 = {f.g73()}\n")
    return f


print("\nТочки плоскости")
f = Void()
try:
    # f = add_pt(f, -4.0, 0.0)
    # f = add_pt(f, 0.0, 4.0)
    # f = add_pt(f, 4.0, 0.0)
    # f = add_pt(f, 0.0, -4.0)

    # Сначала делаем отрезок
    f = Point(R2Point(-1.0, -2.0))
    f = f.add(R2Point(1.0, -2.0))
    # Соединяем с третьей точкой -> Получаем треугольник
    f = f.add(R2Point(1.0, 2.0))
    # Соединяем с четвертой точкой -> Получаем вытянутый прямоугольник
    print('---------')
    f = f.add(R2Point(-1.0, 2.0))

    print(f"S = {f.area()}, P = {f.perimeter()}, g = {f.g()}, g73 = {f.g73()}\n")

    while True:
        f = add_pt(f)

except(EOFError, KeyboardInterrupt):
    print("\nStop")
