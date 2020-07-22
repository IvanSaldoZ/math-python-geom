from math import sqrt
from pytest import approx


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Представление при печате print-ом
    def __repr__(self):
        return f'R2Point: ({self.x}, {self.y})'

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False

    #####################################################################
    #
    #   Дополнительные методы экземпляра
    #
    #####################################################################

    # Сумма векторов
    def __add__(self, other):
        return R2Point(self.x + other.x, self.y + other.y)

    # Разность векторов
    def __sub__(self, other):
        return R2Point(self.x - other.x, self.y - other.y)

    # Умножение на число
    def __mul__(self, k):
        return R2Point(k * self.x, k * self.y)

    # Скалярное произведение
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Векторное произведение (z-координата векторного произведения
    # векторов с нулевыми z-координатами)
    def cross(self, other):
        return self.x * other.y - self.y * other.x

    # Совпадает ли *примерно* точка с другой? — для использования в тестах
    def approx(self, other):
        return self.x == approx(other.x) and self.y == approx(other.y)

    # «Ориентация» тройки точек (self, a, b)
    def orient(self, a, b):
        s = R2Point.area(a, b, self)
        if s == 0.0:
            return 0
        return 1 if s < 0.0 else 2

    # Расстояние до прямой ax + by +c = 0
    def dist2line(self, a, b, c):
        return abs(a*self.x + b*self.y + c) / sqrt(a*a + b*b)

    # Расстояние до отрезка (возможно вырожденного)
    def dist2segment(self, p, q):
        # Коэффициенты общего уравнения прямой
        a = p.y-q.y
        b = q.x-p.x
        # c = p.x*q.y-q.x*p.y

        # Точка в полосе?
        if (p - q).dot(self-q) > 0 and (q - p).dot(self - p) > 0:
            return abs(a*self.x+b*self.y+p.x*q.y-q.x*p.y)/sqrt(a*a+b*b)
        else:
            return min(self.dist(p), self.dist(q))

    # Расстояние от точки (self), рассматриваемой как вершина луча
    # с направляющим ненулевым вектором v (v != 0 ) до точки пересечения
    # этого луча с невырожденным отрезком [a, b] (а != b).
    # В случае отсутствия пересечения возвращается None
    #
    # Полезно (критически) посмотреть на результаты, возвращаемые Google
    # по запросу 'ray to segment distance'
    def dist_ray2segment(self, v, a, b):
        # Единичный направляющий вектор
        v = v * (1.0 / sqrt(v.dot(v)))
        v1 = a - self
        v2 = a - b
        v3 = R2Point(-v.y, v.x)

        dot = v2.dot(v3)
        # Вырожденный случай
        if dot == 0.0:
            # Направляющий вектор и отрезок параллельны
            if v.cross(v1) != 0.0:
                return None
            else:
                # Отрезок лежит на прямой луча
                t1 = v.dot(v1)
                t2 = v.dot(v1 - v2)
                if t1 * t2 <= 0.0:
                    return 0.0
                elif t1 < 0.0:
                    return None
                else:
                    return min(t1, t2)

        t1 = v1.cross(v2) / dot
        t2 = v1.dot(v3) / dot

        if t1 >= 0.0 and 0.0 <= t2 <= 1.0:
            return t1

        return None

    #####################################################################
    #
    #   Дополнительные статические методы
    #
    #####################################################################

    # Расстояние от (возможно вырожденного) отрезка [p, q]
    # до прямой ax + by + c = 0
    @staticmethod
    def dist_seg2line(p, q, a, b, c):
        if (a*p.x + b*p.y + c) * (a*q.x + b*q.y + c) <= 0.0:
            return 0.0
        else:
            return min(p.dist2line(a, b, c), q.dist2line(a, b, c))

    # Расстояние между двумя (возможно вырожденными) отрезками [p, q] и [r, s]
    #
    # Полезно (критически) посмотреть на результаты, возвращаемые Google
    # по запросу 'two line segments intersect'
    @staticmethod
    def dist_seg2seg(p, q, r, s):
        # Невырожденные oтрезки пересекаются (точнее имеют общую строго
        # внутреннюю для них обоих точку) тогда и только тогда, когда
        # каждый из них освещён ровно из одного конца другого!
        if r.is_light(p, q) != s.is_light(p, q) and \
           p.is_light(r, s) != q.is_light(r, s):
            return 0.0
        else:
            # В этом случае отрезки не обязательно не имеют общих точек —
            # они могуть «касаться» или оказаться вырожденными. Но во всех
            # этих случаях расстояние можно находить нижеуказанным способом
            return min(p.dist2segment(r, s), q.dist2segment(r, s),
                       r.dist2segment(p, q), s.dist2segment(p, q))

    # Расстояние от (возможно вырожденного) отрезка [p, q] до
    # заполненного заведомо невырожденного треугольника [a, b, c]
    @staticmethod
    def dist_seg2triangle(p, q, a, b, c):
        # Вспомогательный метод: лежит ли точка t внутри треугольника?
        def equal_lights(t):
            return t.is_light(a, b) == t.is_light(b, c) == t.is_light(c, a)

        if equal_lights(p) and equal_lights(q):
            # Отрезок целиком лежит внутри треугольника
            return 0.0
        else:
            return min(
                R2Point.dist_seg2seg(p, q, a, b),
                R2Point.dist_seg2seg(p, q, b, c),
                R2Point.dist_seg2seg(p, q, c, a)
            )

    # Отрезок пересечения двух (возможно вырожденных) отрезков [p, q] и [r, s]
    # Результат: None или кортеж двух концов отрезка пересечения,
    #            которые чаще всего совпадают (точка пересечения)
    #
    # Полезно (критически) посмотреть на результаты, возвращаемые Google
    # по запросу 'two line segments intersect'
    @staticmethod
    def seg2seg(p, q, r, s):
        ro, so = r.orient(p, q), s.orient(p, q)
        po, qo = p.orient(r, s), q.orient(r, s)

        # Общий случай
        if ro != so and po != qo:
            t = ((r.x-q.x)*(r.y-s.y) - (r.x-s.x)*(r.y-q.y)) / \
                ((p.x-q.x)*(r.y-s.y) - (p.y-q.y)*(r.x-s.x))
            z = R2Point(p.x*t+q.x*(1.0-t), p.y*t+q.y*(1.0-t))
            return (z, z)

        # Вырожденные отрезки
        if p == q:
            return (p, p) if po == 0 and p.is_inside(r, s) else None
        elif r == s:
            return (r, r) if ro == 0 and r.is_inside(p, q) else None

        # Невырожденные отрезки
        if ro == 0:
            # Оба отрезка на одной прямой
            if so == 0:
                if r.is_inside(p, q):
                    if s.is_inside(p, q):
                        return (r, s)
                    else:
                        return (r, q if q.is_inside(r, s) else p)
                else:
                    if s.is_inside(p, q):
                        return (s, q if q.is_inside(r, s) else p)
                if p.is_inside(r, s):
                    if q.is_inside(r, s):
                        return (p, q)
                    else:
                        return (p, s if s.is_inside(p, q) else r)
                else:
                    if q.is_inside(r, s):
                        return (q, s if s.is_inside(p, q) else r)
                    else:
                        return None
            # Только вершина r отрезка [r, s] лежит на прямой [p, q]
            else:
                return (r, r) if r.is_inside(p, q) else None
        elif so == 0:
            # Только вершина s отрезка [r, s] лежит на прямой [p, q]
            return (s, s) if s.is_inside(p, q) else None
        else:
            # Непересекающиеся отрезки
            return None

    # Отрезок пересечения (возможно вырожденного) ребра [p, q] с
    # заполненным заведомо невырожденным треугольником [a, b, c]
    # Результат: None или кортеж из двух концов отрезка пересечения
    @staticmethod
    def seg_in_triangle(p, q, a, b, c):
        # Список отрезков пересечения отрезка [p, q] со сторонами треугольника
        r = list(filter(None, (R2Point.seg2seg(p, q, *t)
                               for t in ((a, b), (b, c), (c, a)))))
        # Точка p внутри
        if p.is_light(a, b) == p.is_light(b, c) == p.is_light(c, a):
            # И точка q внутри
            if q.is_light(a, b) == q.is_light(b, c) == q.is_light(c, a):
                return (p, q)
            else:
                return (p, r[0][0])
        else:
            # Точка q внутри, а p — нет
            if q.is_light(a, b) == q.is_light(b, c) == q.is_light(c, a):
                return (q, r[0][0])
            # Обе точки вне треугольника
            else:
                return None if len(r) == 0 else (r[0][0], r[1][0])



if __name__ == "__main__":
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))