#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Figure, Void

print("Заданная точка")
Figure.fixed_point = R2Point(0.0, 0.0)

print("Задание #73 (Сальдиков): Вершина #1 многоугольника, параллельного осям координат")
Figure.vertex1 = R2Point(-1.0, -1.0)
print("Задание #73 (Сальдиков): Вершина #2 многоугольника, параллельного осям координат")
Figure.vertex2 = R2Point(1.0, 1.0)

print("\nТочки плоскости")
f = Void()
try:
    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}, g = {f.g()}, g73 = {f.g73()}")
        print()
except(EOFError, KeyboardInterrupt):
    print("\nStop")
