from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon
from rectangle import Rectangle


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Void()
        self.f.rectangle = Rectangle()

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        assert isinstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь нульугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)

    # Площадь пересечения - нулевая
    def test_g73_area_segment(self):
        assert self.f.g73() == 0.0



class TestPoint:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0))
        Figure.fixed_point = R2Point(1.0, 0.0)

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь одноугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)

    # Функция `g` вычисляется корректно
    def test_g(self):
        assert self.f.g() == approx(1.0)

    # Площадь пересечения - нулевая
    def test_g73_area_point(self):
        assert self.f.g73() == 0.0




class TestSegment:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))
        Figure.fixed_point = R2Point(0.5, 0.0)

    # Двуугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    # Площадь двуугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # При добавлении точки двуугольник может превратиться в другой двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add3(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)

    # Функция `g` вычисляется корректно
    def test_g(self):
        assert self.f.g() == approx(1.0)

    # Площадь пересечения - нулевая
    def test_g73_area(self):
        assert self.f.g73() == 0.0



class TestPolygon:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        self.f = Polygon(
            R2Point(
                0.0, 0.0),
            R2Point(
                1.0, 0.0),
            R2Point(
                0.0, 1.0)
        )
        Figure.fixed_point = R2Point(0.0, 0.0)

    # Многоугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon(self):
        assert isinstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    #   изначально их три
    def test_vertexes1(self):
        assert self.f.points.size() == 3
    #   добавление точки внутрь многоугольника не меняет их количества

    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3
    #   добавление другой точки может изменить их количество

    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4
    #   изменения выпуклой оболочки могут и уменьшать их количество

    def test_vertexes4(self):
        assert self.f.add(
            R2Point(
                0.4,
                1.0)).add(
            R2Point(
                1.0,
                0.4)).add(
                    R2Point(
                        0.8,
                        0.9)).add(
                            R2Point(
                                0.9,
                                0.8)).points.size() == 7
        assert self.f.add(R2Point(2.0, 2.0)).points.size() == 4

    # Изменение периметра многоугольника
    #   изначально он равен сумме длин сторон
    def test_perimeter1(self):
        assert self.f.perimeter() == approx(2.0 + sqrt(2.0))
    #   добавление точки может его изменить

    def test_perimeter2(self):
        assert self.f.add(R2Point(1.0, 1.0)).perimeter() == approx(4.0)

    # Изменение площади многоугольника
    #   изначально она равна (неориентированной) площади треугольника
    def test_аrea1(self):
        assert self.f.area() == approx(0.5)
    #   добавление точки может увеличить площадь

    def test_area2(self):
        assert self.f.add(R2Point(1.0, 1.0)).area() == approx(1.0)

    # Функция `g` вычисляется корректно для треугольника
    def test_g1(self):
        t = Segment(R2Point(-1.0, 0.0), R2Point(1.0, 0.0))
        t = t.add(R2Point(0.0, 1.0))
        assert t.g() == approx(3.0)

    # Функция `g` вычисляется корректно для квадрата
    def test_g2(self):
        t = Segment(R2Point(-1.0, 0.0), R2Point(1.0, 0.0))
        t = t.add(R2Point(0.0, 1.0))
        t = t.add(R2Point(0.0, -1.0))
        assert t.g() == approx(4.0)

    # Функция `g` вычисляется корректно для трапеции
    def test_g3(self):
        t = Segment(R2Point(-1.0, 0.0), R2Point(1.0, 0.0))
        t = t.add(R2Point(0.0, 1.0))
        t = t.add(R2Point(0.0, -1.0))
        t = t.add(R2Point(1.0, 1.0))
        assert t.g() == approx(4.0 + sqrt(2.0))

    # Функция `g` вычисляется корректно для прямоугольника
    def test_g4(self):
        t = Segment(R2Point(-1.0, 0.0), R2Point(1.0, 0.0))
        t = t.add(R2Point(0.0, 1.0))
        t = t.add(R2Point(0.0, -1.0))
        t = t.add(R2Point(1.0, 1.0))
        t = t.add(R2Point(1.0, -1.0))
        t = t.add(R2Point(-1.0, 1.0))
        t = t.add(R2Point(-1.0, -1.0))
        assert t.g() == approx(4.0 * sqrt(2.0))

    # Функция `g` вычисляется корректно для большой трапеции
    def test_g5(self):
        t = Segment(R2Point(-1.0, 0.0), R2Point(1.0, 0.0))
        t = t.add(R2Point(0.0, 1.0))
        t = t.add(R2Point(0.0, -1.0))
        t = t.add(R2Point(1.0, 1.0))
        t = t.add(R2Point(1.0, -1.0))
        t = t.add(R2Point(-1.0, 1.0))
        t = t.add(R2Point(-1.0, -1.0))
        t = t.add(R2Point(3.0, -1.0))
        assert t.g() == approx(3.0 * sqrt(2.0) + sqrt(10.0))

    # Функция `g` вычисляется корректно для большого треугольника
    def test_g6(self):
        t = Segment(R2Point(-1.0, 0.0), R2Point(1.0, 0.0))
        t = t.add(R2Point(0.0, 1.0))
        t = t.add(R2Point(0.0, -1.0))
        t = t.add(R2Point(1.0, 1.0))
        t = t.add(R2Point(1.0, -1.0))
        t = t.add(R2Point(-1.0, 1.0))
        t = t.add(R2Point(-1.0, -1.0))
        t = t.add(R2Point(3.0, -1.0))
        t = t.add(R2Point(-1.0, 3.0))
        assert t.g() == approx(sqrt(2.0) + 2 * sqrt(10.0))




    # 0.а Функция `g73` вычисляется корректно для нулевой площади точки
    # (-1,-1,)
    def test_g73_zero(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        t = Point(R2Point(-1.0, -1.0))
        assert t.g73() == 0.0

    # 0.б Функция `g73` вычисляется корректно для нулевой площади отрезка
    # (-1,-1,), (1,1)
    def test_g73_zero_segment(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        t = Point(R2Point(-1.0, -1.0))
        t = t.add(R2Point(1.0, 1.0))
        assert t.g73() == 0.0

    # 1. Функция `g73` вычисляется корректно для обычного треугольника с тремя единичными вершинам (верхний треугольник)
    # (-1,-1,), (1,1), (-1,1)
    def test_g73_trian_upper(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        # Сначала делаем отрезок
        t = Polygon(
            R2Point(
                -1.0, -1.0),
            R2Point(
                1.0, 1.0),
            R2Point(
                -1.0, 1.0)
        )

        # t = Point(R2Point(-1.0, -1.0))
        # t = t.add(R2Point(1.0, 1.0))
        # t = t.add(R2Point(-1.0, 1.0))
        assert t.g73() == approx(2.0)

    # 2. Функция `g73` вычисляется корректно для обычного треугольника с тремя единичными вершинам (нижний треугольник)
    # (-1,-1,), (1,1), (1,-1)
    def test_g73_trian_lower(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        # Сначала делаем отрезок
        t = Segment(R2Point(-1.0, -1.0), R2Point(1.0, 1.0))
        # Соединяем с третьей точкой -> Получаем треугольник
        t = t.add(R2Point(1.0, -1.0))
        assert t.g73() == approx(2.0)

    # 3. Функция `g73` вычисляется корректно для той же формы, что и прямоугольник g73 (по факту - квадрат)
    # (-1,-1,), (1,-1), (1,1), (-1,1)
    def test_g73_the_same_square(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        # Сначала делаем отрезок
        t = Segment(R2Point(-1.0, -1.0), R2Point(1.0, -1.0))
        # Соединяем с третьей точкой -> Получаем треугольник
        t = t.add(R2Point(1.0, 1.0))
        # Соединяем с четвертой точкой -> Получаем квадрат (точки совпадают с вершинам "прямоугольника" по умолчанию)
        t = t.add(R2Point(-1.0, 1.0))
        assert t.g73() == approx(4.0)

    # 4. Функция `g73` вычисляется корректно для выпуклой оболочки - вытянутого вдоль оси y прямоугольника
    # (-1,-2,), (1,-2), (1,2), (-1,2)
    def test_g73_y_elongated(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        # Сначала делаем отрезок
        t = Point(R2Point(-1.0, -2.0))
        t = t.add(R2Point(1.0, -2.0))
        # Соединяем с третьей точкой -> Получаем треугольник
        t = t.add(R2Point(1.0, 2.0))
        # Соединяем с четвертой точкой -> Получаем вытянутый прямоугольник
        t = t.add(R2Point(-1.0, 2.0))
        # Но общая-то площадь измениться всё-равно не должна
        assert t.g73() == approx(4.0)

    # 5. Функция `g73` вычисляется корректно для выпуклой оболочки - вытянутого вдоль оси x прямоугольника
    # (-2,-1,), (2,-1), (2,1), (-2,1)
    def test_g73_x_elongated(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        # Сначала делаем отрезок
        t = Point(R2Point(-2.0, -1.0))
        t = t.add(R2Point(2.0, -1.0))
        # Соединяем с третьей точкой -> Получаем треугольник
        t = t.add(R2Point(2.0, 1.0))
        # Соединяем с четвертой точкой -> Получаем вытянутый прямоугольник
        t = t.add(R2Point(-2.0, 1.0))
        # Но общая-то площадь измениться всё-равно не должна
        assert t.g73() == approx(4.0)

    # 6. Функция `g73` вычисляется корректно для выпуклой оболочки - квадрата внутри квадрата
    # (-0.5,-0.5,), (0.5,-0.5), (0.5,0.5), (-0.5,0.5)
    def test_g73_small_square_in(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        # Сначала делаем отрезок
        t = Segment(R2Point(-0.5, -0.5), R2Point(0.5, -0.5))
        # Соединяем с третьей точкой -> Получаем треугольник
        t = t.add(R2Point(0.5, 0.5))
        # Соединяем с четвертой точкой -> Получаем маленький квадратик внутри нашего "прямоугольника"
        t = t.add(R2Point(-0.5, 0.5))
        # Общая площадь равна площади всей замкнутой оболочки, т.е. единицы (всего квадратика)
        assert t.g73() == approx(1.0)

    # 7. Функция `g73` вычисляется корректно для выпуклой оболочки - прямоугольника вверху нашего квадрата
    # (-1.0, 0.5), (1.0, 0.5), (1.0, 1.0), (-1.0, 1.0)
    def test_g73_line_up(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        # Сначала делаем отрезок
        t = Segment(R2Point(-1.0, 0.5), R2Point(1.0, 0.5))
        # Соединяем с третьей точкой -> Получаем треугольник
        t = t.add(R2Point(1.0, 1.0))
        # Соединяем с четвертой точкой -> Получаем полосочку вверху нашего квадрата
        t = t.add(R2Point(-1.0, 1.0))
        # Общая площадь равна площади полоски, т.е. тоже единица
        assert t.g73() == approx(1.0)

    # 8. Функция `g73` вычисляется корректно для выпуклой оболочки - не пересекающей вообще наш квадрат
    # (-1.0, 2.0), (1.0, 2.0), (1.0, 3.0), (-1.0, 3.0)
    def test_g73_not_crossing(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        # Сначала делаем отрезок
        t = Point(R2Point(-1.0, 2.0))
        t = t.add(R2Point(1.0, 2.0))
        # Соединяем с третьей точкой -> Получаем треугольник
        t = t.add(R2Point(1.0, 3.0))
        # Соединяем с четвертой точкой -> Получаем полосочку ВЫШЕ нашего квадрата и не пересекающего его
        t = t.add(R2Point(-1.0, 3.0))
        # Общая площадь равна площади полоски, т.е. тоже единица
        assert t.g73() == 0.0

    # 9. Функция `g73` вычисляется корректно для выпуклой оболочки - большого треугольника
    # (-2.0, -2.0), (2.0, 2.0), (-2.0, 2.0)
    def test_g73_trian_big_upper(self):
        Figure.rectangle = Rectangle()  # Сразу создаем прямоугольник
        # Сначала делаем отрезок
        t = Point(R2Point(-2.0, 2.0))
        t = t.add(R2Point(-2.0, -2.0))
        # Соединяем с третьей точкой -> Получаем большой треугольник
        t = t.add(R2Point(2.0, 2.0))
        # Общая площадь должна быть 2 (половина квадрата)
        assert t.g73() == approx(2.0)

