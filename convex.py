from deq import Deq
from r2point import R2Point
from rectangle import Rectangle


class Figure:
    """ Абстрактная фигура """

    fixed_point = R2Point(0.0, 0.0)
    rectangle = Rectangle()

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def g(self):
        return None

    def g73(self):
        """
        По умолчанию площадь пересечения равна нулю
        """
        return 0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        if self.p == q:
            return self
        else:
            self.rectangle.add_crossing(self.p, q)  # Проверяем, пересекает ли отрезок какую-либо из граней
            return Segment(self.p, q)

    def g(self):
        return self.p.dist(self.fixed_point)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            self.rectangle.add_crossing(self.p, r)  # Проверяем, пересекает ли отрезок какую-либо из граней
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            self.rectangle.add_crossing(r, self.q)  # Проверяем, пересекает ли отрезок какую-либо из граней
            return Segment(r, self.q)
        else:
            return self

    def g(self):
        return self.fixed_point.dist(self.p) + self.fixed_point.dist(self.q)

    def g73(self):
        """
        Возвращаем общую площадь прямоугольника и выпуклой оболочки
        """
        return self.rectangle.common_area()


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
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

        self.rectangle.add_crossing(b, c)  # Проверяем, пересекает ли отрезок какую-либо из граней
        self.rectangle.add_crossing(b, a)  # Проверяем, пересекает ли отрезок какую-либо из граней
        # Добавляем в Дек вершины прямоугольника, которые находятся внутри выпуклой оболочки,
        # чтобы корректно считать площадь, если НЕТ пересечения
        self.rectangle.add_inside(a, b, c)

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def g(self):
        return self._g
    
    def g73(self):
        """
        Возвращаем общую площадь прямоугольника и выпуклой оболочки
        """
        return self.rectangle.common_area()

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
            self.rectangle.add_crossing(self.points.first(), t)  # Проверяем, пересекает ли отрезок какую-либо из граней
            self.rectangle.add_crossing(self.points.last(), t)  # Проверяем, пересекает ли отрезок какую-либо из граней
            # Добавляем в Дек вершины прямоугольника, которые находятся внутри выпуклой оболочки,
            # чтобы корректно считать площадь, если НЕТ пересечения
            self.rectangle.add_inside(self.points.first(), self.points.last(), t)

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

            self.rectangle.add_crossing(self.points.first(), t)  # Проверяем, пересекает ли отрезок какую-либо из граней
            self.rectangle.add_crossing(self.points.last(), t)  # Проверяем, пересекает ли отрезок какую-либо из граней
            # Добавляем в Дек вершины прямоугольника, которые находятся внутри выпуклой оболочки,
            # чтобы корректно считать площадь, если НЕТ пересечения
            self.rectangle.add_inside(self.points.first(), self.points.last(), t)

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
