from deq import Deq
from r2point import R2Point


class Rectangle:
    """
    Обчный прямоугольник, общую площадь с которым нужно найти
    """

    # Вершины прямоугольника внутри которого ищется общая площадь с выпуклой оболочкой
    # Задаем по умолчанию хоть какое-то значение (квадарт, площадью 4.0)
    verts = [R2Point(-1.0, -1.0), R2Point(1.0, -1.0), R2Point(1.0, 1.0), R2Point(-1.0, 1.0)]

    def __init__(self, a=None, b=None):
        self.common_points = Deq()  # Общие точки прямоугольника и выпуклой оболочки (Дек)
        self._common_perimeter = 0  # Общий периметр (так уж за одно посчитаем)
        self._common_area = 0  # Общая площадь - то, что нужно найти в задаче!
        # Указываем вершины прямоугольника
        self.set_verts(a, b)

    def set_verts(self, a, b):
        """
        Назначаем противоположные вершины прямоугольника
        """
        # Если в конструкторе указаны противоположные точки, то размеры прямоугольника меняем:
        if a is not None:
            self.verts[0] = a
        if b is not None:
            self.verts[2] = b
        # Вычисляем противоположные вершины
        self.calc_other_vertex()
        return self.verts

    def calc_other_vertex(self):
        """
        Считаем противоположные вершины прямоугольника, если имеются две других противоположных
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
            #print("AddOK1")
        if crossing_points_right is not None:
            crossing_points.append(crossing_points_right[0])
            crossing_points.append(crossing_points_right[1])
            #print("AddOK2")
        if crossing_points_top is not None:
            crossing_points.append(crossing_points_top[0])
            crossing_points.append(crossing_points_top[1])
            #print("AddOK3")
        if crossing_points_left is not None:
            crossing_points.append(crossing_points_left[0])
            crossing_points.append(crossing_points_left[1])
            #print("AddOK4")
        # Оставляем только уникальные точки
        for point in crossing_points:
            #print('Checking point:', point)
            #print(self.add_common_point(point))
            self.add_common_point(point)
            #print('Rect Deque (crossing point):', self.common_points.size())
            #print('Common area (crossing point):', self.common_area())

    def add_inside(self, a, b, c):
        """
        Проверяем вершины прямоугольника, которые попали внутрь выпуклой оболочки и добавляем их в общие точки
        Этот метод нужен тогда, когда общих пересечений у выпуклой оболочки нет, но сами вершины прямоугольника
        являются точками, которые надо учитывать
        Передаются три новых точки выпуклой оболочки, которые дают нам новую площадь
        """
        for i in range(4):
            if self.verts[i].is_inside_of_triang(a, b, c):
                self.add_common_point(self.verts[i])
                #print('a:',a)
                #print('b:',b)
                #print('c:',c)
                #print('Rect Deque (inner point):', self.common_points.size())
                #print('Common area (inner point):', self.common_area())

    def add_outside(self, a):
        """
        Проверяем, является ли наш прямоугольник внешним по отношению к точке выпуклой оболочки
        Т.е. другими словами, лежит ли точка "a" внутри нашего прямоугольника.
        И если да, то добавляем ее в список общих точек
        """
        # метод R2Point для проверки лежит ли точка внутри правильного прямоугольника
        # аргументы - противопоолжные вершины этого прямоугольника
        if a.is_inside(self.verts[0], self.verts[2]):
            self.add_common_point(a)
            #print('Rect Deque (outer point):', self.common_points.size())
            #print('Common area (outer point):', self.common_area())

    def find_crossing_seg(self, a, b, q, p):
        """
        Находим пересечение двух отрезков [a,b] и [q, p].
        Возвращает общее пересечение - отрезок (если совпадает, то точка)
        """
        return R2Point.seg2seg(a, b, q, p)

    # добавление новой точки в массив точек общей площади
    def add_common_point(self, t):
        # Если такая точка уже есть, то ничего не делаем
        #print('Common Points Before:', self.common_points)
        if t in self.common_points:
            return self
        # Поначалу просто наберем хотя бы одну точку
        if self.common_points.size() == 0:
            self.common_points.push_first(t)
        # Потом добавляем в конец другую точку
        if self.common_points.size() == 1:
            self.common_points.push_last(t)
        # Если у нас есть две точки, то добавляя третью нам надо расширить отрезок, удалив серединную точку
        if self.common_points.size() == 2:
            # Если точки лежат на одной прямой
            if not R2Point.is_triangle(t, self.common_points.first(), self.common_points.last()):
                # Проверяем, находится ли точка начала дека внутри отрезка
                if self.common_points.first().is_inside(t, self.common_points.last()):
                    self.common_points.pop_first()
                    self.common_points.push_last(t)  # Если да, то заменяем на добавляемую точку
                # или если точка конца дека находится внутри отрезка
                elif self.common_points.last().is_inside(t, self.common_points.first()):
                    self.common_points.pop_last()
                    self.common_points.push_first(t)
        # Если же у нас уже накопилось более трех точек, то ищем площадь
        if self.common_points.size() >= 2:
            # поиск освещённого ребра
            for n in range(self.common_points.size()):
                if t.is_light(self.common_points.last(), self.common_points.first()):
                    break
                self.common_points.push_last(self.common_points.pop_first())

            # хотя бы одно освещённое ребро есть (если не внутри)
            if t.is_light(self.common_points.last(), self.common_points.first()):
                # учёт удаления ребра, соединяющего конец и начало дека
                self._common_perimeter -= self.common_points.first().dist(self.common_points.last())
                area = abs(R2Point.area(t,
                                                      self.common_points.last(),
                                                      self.common_points.first()))
                self._common_area += area
                # удаление освещённых рёбер из начала дека
                #print('OK1:',self.common_points)
                #print('OK1_first:',self.common_points.first())
                #print('OK1_last:',self.common_points.last())
                #print('OK1_size:',self.common_points.size())
                p = self.common_points.pop_first()
                #print('OK2:',self.common_points)
                #print('OK3:',p)
                #print('OK4:',self.common_points.array[0])
                while t.is_light(p, self.common_points.first()):
                    self._common_perimeter -= p.dist(self.common_points.first())
                    self._common_area += abs(R2Point.area(t, p, self.common_points.first()))
                    p = self.common_points.pop_first()
                    #print('OK5_p:', p)
                    #print('OK5_after_p:', self.common_points)
                self.common_points.push_first(p)

                # удаление освещённых рёбер из конца дека
                p = self.common_points.pop_last()
                while t.is_light(self.common_points.last(), p):
                    self._common_perimeter -= p.dist(self.common_points.last())
                    self._common_area += abs(R2Point.area(t, p, self.common_points.last()))
                    p = self.common_points.pop_last()
                self.common_points.push_last(p)

                # добавление двух новых рёбер
                self._common_perimeter += t.dist(self.common_points.first()) + \
                                          t.dist(self.common_points.last())
                self.common_points.push_first(t)
        #print('Common Points After:', self.common_points)
        return self
