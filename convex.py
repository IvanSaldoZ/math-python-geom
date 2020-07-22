from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    # Значения противоположных вершин прямоугольника внутри которого ищется общая площадь с выпуклой оболочкой
    vertex1 = R2Point(-1.0, -1.0)
    vertex2 = R2Point(1.0, 1.0)
    # Остальные вершины - это просто зеркальные координаты, чтобы получился прямоугольник
    vertex3 = R2Point(vertex1.x, vertex2.y)
    vertex4 = R2Point(vertex2.x, vertex1.y)

    def __init__(self):
        pass

    # def vertex1(self):
    #     return self._vertex1
    #
    # def vertex2(self):
    #     return self._vertex2
    #
    # def vertex3(self):
    #     return self._vertex3
    #
    # def vertex4(self):
    #     return self._vertex4

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def g(self):
        return None

    def g73(self):
        """По умолчанию возвращается общая площадь 0"""
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        super().__init__()
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)

    def g(self):
        return self.p.dist(self.fixed_point)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        super().__init__()
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return self

    def g(self):
        return self.fixed_point.dist(self.p) + self.fixed_point.dist(self.q)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        super().__init__()
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self._g = a.dist(self.fixed_point) + b.dist(self.fixed_point) + \
            c.dist(self.fixed_point)
        self._g73 = self.find_common_area3(a,b,c)


    def find_common_area3(self, a, b, c):
        """
        Находим добавочную площадь для нашего прямоугольника и трех точек (первоначально)
        """
        # Если все три точки внутри нашего прямоугольника, то площадь просто равно площади выпуклой фигуры
        print('OK1')
        print(a.x,a.y)
        print(b.x,b.y)
        print(self.vertex1.x, self.vertex1.y, )
        print(self.vertex4.x, self.vertex4.y, )
        print(self.find_crossing(a, b, self.vertex1, self.vertex4))
        print(self.find_crossing(a, b, self.vertex4, self.vertex2))
        print(self.find_crossing(a, b, self.vertex2, self.vertex3))
        print(self.find_crossing(a, b, self.vertex3, self.vertex1))
        if a.is_inside(self.vertex1, self.vertex2) \
        and b.is_inside(self.vertex1, self.vertex2)  \
        and c.is_inside(self.vertex1, self.vertex2):
            return self.area()

    def find_crossing(self, a, b, q, p):
        """
        Находим пересечение точек от ребер с каким-либо отрезком прямоугольника
        """
        print('---------')
        print('---------')
        return R2Point.seg2seg(a, b, q, p)





    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def g(self):
        return self._g

    def g73(self):
        return self._g73

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                self._g -= p.dist(self.fixed_point)
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                self._g -= p.dist(self.fixed_point)
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            self.points.push_first(t)
            self._g += t.dist(self.fixed_point)

        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
