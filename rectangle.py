from r2point import R2Point
from deq import Deq

class Rectangle:
    """
    Обчный прямоугольник, общую площадь с которым нужно найти
    """

    # Вершины прямоугольника внутри которого ищется общая площадь с выпуклой оболочкой
    # Задаем по умолчанию хоть какое-то значение
    verts = [R2Point(-1.0, -1.0), R2Point(1.0, -1.0), R2Point(1.0, 1.0), R2Point(-1.0, 1.0)]

    def __init__(self, a=None, b=None):
        self.common_points = Deq()  # Общие точки прямоугольника и выпуклой оболочки (Дек)
        self._common_perimeter = 0  # Общий периметр (так уж за одно посчитаем)
        self._common_area = 0  # Общая площадь - то, что нужно найти в задаче!
        # Если в конструкторе указаны противоположные точки, то размеры прямоугольника меняем:
        if a is not None:
            self.verts[0] = a
        if b is not None:
            self.verts[2] = b
        # Вычисляем противоположные вершины
        self.calc_other_vertex()

    def calc_other_vertex(self):
        """
        Считаем противоположные вершины прямоугольника
        """
        self.verts[1].x = self.verts[2].x
        self.verts[1].y = self.verts[0].y
        self.verts[3].x = self.verts[0].x
        self.verts[3].y = self.verts[2].y
        return self.verts

    def common_area(self):
        """
        Возвращаем общую площадь
        """
        return self._common_area

    def common_perimeter(self):
        """
        Возвращаем общие периметр
        """
        return self._common_perimeter

    def add_crossing(self, a, b):
        """
        Найти пересекающиеся точки с нашим прямоугольником и ребром, образованным точками [a, b]
        """
        # Добавляем точки конца отрезка в список общих точек, если они внутри
        self.add_outside(a)
        self.add_outside(b)

        crossing_points = []
        crossing_points_bottom = self.find_crossing_seg(a, b, self.verts[0], self.verts[1])
        crossing_points_right = self.find_crossing_seg(a, b, self.verts[1], self.verts[2])
        crossing_points_top = self.find_crossing_seg(a, b, self.verts[2], self.verts[3])
        crossing_points_left = self.find_crossing_seg(a, b, self.verts[3], self.verts[0])
        if crossing_points_bottom is not None:
            crossing_points.append(crossing_points_bottom[0])
            crossing_points.append(crossing_points_bottom[1])
        if crossing_points_right is not None:
            crossing_points.append(crossing_points_right[0])
            crossing_points.append(crossing_points_right[1])
        if crossing_points_top is not None:
            crossing_points.append(crossing_points_top[0])
            crossing_points.append(crossing_points_top[1])
        if crossing_points_left is not None:
            crossing_points.append(crossing_points_left[0])
            crossing_points.append(crossing_points_left[1])
        # Оставляем только уникальные точки
        # crossing_points = self.uniq(crossing_points)
        for point in crossing_points:
            print('Checking point:',point)
            #print(self.add_common_point(point))
            self.add_common_point(point)
        print('Rect Deque:',self.common_points.size())
        print('Common area:',self.common_area())

    def add_inside(self, a,b,c):
        """
        Проверяем вершины прямоугольника, которые попали внутрь выпуклой оболочки и добавляем их в общие точки
        Этот метод нужен тогда, когда общих пересечений у выпуклой оболочки нет, но сами вершины прямоугольника
        являются точками, которые надо учитывать
        Передаются три новых точки выпуклой оболочки, которые дают нам новую площадь
        """
        for i in range(4):
            if self.verts[i].is_inside_of_triang(a,b,c):
                self.add_common_point(self.verts[i])
                print('Rect Deque (inner point):', self.common_points.size())
                print('Common area (inner point):', self.common_area())

    def add_outside(self, a):
        """
        Проверяем, является ли наш прямоугольник внешним по отношению к точке выпуклой оболочки
        Т.е. другим словами, лежит ли точка "a" внутри нашего прямоугольника.
        И если да, то добавляем ее в список общих точек
        """
        # метод R2Point для проверки лежит ли точка внутри правильного прямоугольника
        # аргументы - противопоолжные вершины этого прямоугольника
        if a.is_inside(self.verts[0], self.verts[2]):
            self.add_common_point(a)
            print('Rect Deque (outer point):', self.common_points.size())
            print('Common area (outer point):', self.common_area())

    # Оставляем только уникальные значения в списк
    def uniq(self, lst):
        tmp = []
        for t in lst:
            if t not in tmp:
                tmp.append(t)
        return tmp

    def find_crossing_seg(self, a, b, q, p):
        """
        Находим пересечение двух отрезков [a,b] и [q, p].
        Возвращает общее пересечение - отрезок (если совпадает, то точка)
        """
        return R2Point.seg2seg(a, b, q, p)

    # добавление новой точки в массив точек общей площади
    def add_common_point(self, t):
        # Если такая точка уже есть, то ничего не делаем
        if t in self.common_points:
            return self
        # Поначалу просто наберем хотя бы одну точку
        if self.common_points.size() <= 1:
            self.common_points.push_first(t)
        else:
            # поиск освещённого ребра
            for n in range(self.common_points.size()):
                if t.is_light(self.common_points.last(), self.common_points.first()):
                    break
                self.common_points.push_last(self.common_points.pop_first())

            # хотя бы одно освещённое ребро есть (если не внутри)
            if t.is_light(self.common_points.last(), self.common_points.first()):

                # учёт удаления ребра, соединяющего конец и начало дека
                self._common_perimeter -= self.common_points.first().dist(self.common_points.last())
                self._common_area += abs(R2Point.area(t,
                                               self.common_points.last(),
                                               self.common_points.first()))

                # удаление освещённых рёбер из начала дека
                p = self.common_points.pop_first()
                while t.is_light(p, self.common_points.first()):
                    self._common_perimeter -= p.dist(self.common_points.first())
                    self._common_area += abs(R2Point.area(t, p, self.common_points.first()))
                    p = self.common_points.pop_first()
                self.common_points.push_first(p)

                # удаление освещённых рёбер из конца дека
                p = self.common_points.pop_last()
                while t.is_light(self.common_points.last(), p):
                    self._common_perimeter -= p.dist(self.common_points.last())
                    self._common_area += abs(R2Point.area(t, p, self.common_points.last()))
                    p = self.common_points.pop_last()
                self.common_points.push_last(p)

                # добавление двух новых рёбер
                self._common_perimeter +=  t.dist(self.common_points.first()) + \
                                        t.dist(self.common_points.last())
                self.common_points.push_first(t)
        #print('Common Points:', self.common_points)
        return self
