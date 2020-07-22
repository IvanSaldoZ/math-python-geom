from pytest import approx
from math import sqrt
from r2point import R2Point


class TestAddR2Point:

    ##########################################################################
    #
    # Тесты на метод нахождения расстояния от точки до прямой
    #
    ##########################################################################

    def test_dist2line1(self):
        a, b, c = 0.0, 1.0, 0.0
        assert R2Point(0.0, 0.0).dist2line(a, b, c) == approx(0.0)

    def test_dist2line2(self):
        a, b, c = 0.0, 1.0, 0.0
        assert R2Point(-1.0, 0.0).dist2line(a, b, c) == approx(0.0)

    def test_dist2line3(self):
        a, b, c = 0.0, 1.0, 0.0
        assert R2Point(0.0, 1.0).dist2line(a, b, c) == approx(1.0)

    def test_dist2line4(self):
        a, b, c = 0.0, 1.0, 0.0
        assert R2Point(0.0, -1.0).dist2line(a, b, c) == approx(1.0)

    def test_dist2line5(self):
        a, b, c = 1.0, 1.0, -1.0
        assert R2Point(0.0, 0.0).dist2line(a, b, c) == approx(sqrt(2.0)/2.0)

    def test_dist2line6(self):
        a, b, c = 1.0, 1.0, -1.0
        assert R2Point(-1.0, 2.0).dist2line(a, b, c) == approx(0.0)

    def test_dist2line7(self):
        a, b, c = 1.0, 1.0, -1.0
        assert R2Point(3.0, 0.0).dist2line(a, b, c) == approx(sqrt(2.0))

    ##########################################################################
    #
    # Тесты на метод нахождения расстояния от точки до отрезка
    #
    ##########################################################################

    # Точка находится на невырожденном отрезке
    def test_dist2segment01(self):
        a = R2Point(1.0, 0.0)
        p, q = R2Point(0.0, 0.0), R2Point(2.0, 0.0)
        assert a.dist2segment(p, q) == approx(0.0)

    # Точка на одной линии с невырожденным отрезком вне его
    def test_dist2segment02(self):
        a = R2Point(-1.0, 0.0)
        p, q = R2Point(0.0, 0.0), R2Point(2.0, 0.0)
        assert a.dist2segment(p, q) == approx(1.0)

    # Точка в полосе над невырожденным отрезком
    def test_dist2segment03(self):
        a = R2Point(1.0, 1.0)
        p, q = R2Point(0.0, 0.0), R2Point(2.0, 0.0)
        assert a.dist2segment(p, q) == approx(1.0)

    # Точка вне полосы
    def test_dist2segment04(self):
        a = R2Point(-1.0, 1.0)
        p, q = R2Point(0.0, 0.0), R2Point(2.0, 0.0)
        assert a.dist2segment(p, q) == approx(sqrt(2.0))

    # Точка совпадает с одним из концов невырожденного отрезка
    def test_dist2segment05(self):
        a = R2Point(0.0, 0.0)
        p, q = R2Point(0.0, 0.0), R2Point(2.0, 0.0)
        assert a.dist2segment(p, q) == approx(0.0)

    # Точка находится на наклонном невырожденным отрезке
    def test_dist2segment06(self):
        a = R2Point(0.5, 0.5)
        p, q = R2Point(1.0, 0.0), R2Point(0.0, 1.0)
        assert a.dist2segment(p, q) == approx(0.0)

    # Точка на одной линии с наклонным невырожденным отрезком вне его
    def test_dist2segment07(self):
        a = R2Point(2.0, -1.0)
        p, q = R2Point(1.0, 0.0), R2Point(0.0, 1.0)
        assert a.dist2segment(p, q) == approx(sqrt(2.0))

    # Точка в полосе
    def test_dist2segment08(self):
        a = R2Point(0.0, 0.0)
        p, q = R2Point(1.0, 0.0), R2Point(0.0, 1.0)
        assert a.dist2segment(p, q) == approx(sqrt(2.0)/2.0)

    # Точка все полосы
    def test_dist2segment09(self):
        a = R2Point(2.0, 0.0)
        p, q = R2Point(1.0, 0.0), R2Point(0.0, 1.0)
        assert a.dist2segment(p, q) == approx(1.0)

    # Точка совпадает с одним из концов невырожденного отрезка
    def test_dist2segment10(self):
        a = R2Point(1.0, 0.0)
        p, q = R2Point(1.0, 0.0), R2Point(0.0, 1.0)
        assert a.dist2segment(p, q) == approx(0.0)

    # Отрезок вырожден и точка с ним совпадает
    def test_dist2segment11(self):
        a = R2Point(1.0, 0.0)
        p, q = R2Point(1.0, 0.0), R2Point(1.0, 0.0)
        assert a.dist2segment(p, q) == approx(0.0)

    # Отрезок вырожден, а точка с ним не совпадает
    def test_dist2segment12(self):
        a = R2Point(0.0, 0.0)
        p, q = R2Point(1.0, 1.0), R2Point(1.0, 1.0)
        assert a.dist2segment(p, q) == approx(sqrt(2.0))

    ##########################################################################
    #
    # Тесты на метод нахождения расстояния от точки, рассматриваемой как
    # вершина луча с направляющим ненулевым вектором v (v != 0 ) до точки
    # пересечения этого луча с невырожденным отрезком [a, b] (а != b).
    # В случае отсутствия пересечения возвращается None
    #
    ##########################################################################

    # Отрезок параллелен лучу
    def test_dist_ray2segment1(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 0.0)
        a = R2Point(0.0, -1.0)
        b = R2Point(1.0, -1.0)
        assert x.dist_ray2segment(v, a, b) is None

    # Отрезок перпрендикулярен лучу, но они не пересекаются
    def test_dist_ray2segment2(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 0.0)
        a = R2Point(0.0, -1.0)
        b = R2Point(0.0, -2.0)
        assert x.dist_ray2segment(v, a, b) is None

    # Отрезок пересекает луч
    def test_dist_ray2segment3(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 0.0)
        a = R2Point(1.0, 0.0)
        b = R2Point(1.0, 1.0)
        assert x.dist_ray2segment(v, a, b) == approx(1.0)

    # Отрезок пересекает только продолжение луча
    def test_dist_ray2segment4(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(-1.0, 0.0)
        a = R2Point(1.0, 0.0)
        b = R2Point(1.0, 1.0)
        assert x.dist_ray2segment(v, a, b) is None

    # Отрезок пересекает луч
    def test_dist_ray2segment5(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 1.0)
        a = R2Point(2.0, 0.0)
        b = R2Point(0.0, 2.0)
        assert x.dist_ray2segment(v, a, b) == approx(sqrt(2.0))

    # Отрезок пересекает только продолжение луча
    def test_dist_ray2segment6(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, -1.0)
        a = R2Point(-1.0, 0.0)
        b = R2Point(0.0, 1.0)
        assert x.dist_ray2segment(v, a, b) is None

    # Отрезок пересекает луч
    def test_dist_ray2segment7(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, -1.0)
        a = R2Point(2.0, 0.0)
        b = R2Point(0.0, -4.0)
        assert x.dist_ray2segment(v, a, b) == approx(4.0 * sqrt(2.0) / 3.0)

    # Отрезок лежит на продолжении луча и его не пересекает
    def test_dist_ray2segment8(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 1.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(-2.0, -2.0)
        assert x.dist_ray2segment(v, a, b) is None

    # Отрезок лежит на продолжении луча и его не пересекает
    def test_dist_ray2segment9(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 1.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(-2.0, -2.0)
        assert x.dist_ray2segment(v, b, a) is None

    # Отрезок лежит на продолжении луча и его касается
    def test_dist_ray2segment10(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 1.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(0.0, 0.0)
        assert x.dist_ray2segment(v, a, b) == approx(0.0)

    # Отрезок лежит на продолжении луча и его касается
    def test_dist_ray2segment11(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 1.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(0.0, 0.0)
        assert x.dist_ray2segment(v, b, a) == approx(0.0)

    # Отрезок полностью лежит на луче, расстояние нулевое
    def test_dist_ray2segment12(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 1.0)
        a = R2Point(2.0, 2.0)
        b = R2Point(0.0, 0.0)
        assert x.dist_ray2segment(v, a, b) == approx(0.0)

    # Отрезок полностью лежит на луче, расстояние нулевое
    def test_dist_ray2segment13(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 1.0)
        a = R2Point(2.0, 2.0)
        b = R2Point(0.0, 0.0)
        assert x.dist_ray2segment(v, b, a) == approx(0.0)

    # Отрезок полностью лежит на луче, расстояние положительное
    def test_dist_ray2segment14(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 1.0)
        a = R2Point(2.0, 2.0)
        b = R2Point(3.0, 3.0)
        assert x.dist_ray2segment(v, a, b) == approx(2.0 * sqrt(2.0))

    # Отрезок полностью лежит на луче, расстояние положительное
    def test_dist_ray2segment15(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(1.0, 1.0)
        a = R2Point(2.0, 2.0)
        b = R2Point(3.0, 3.0)
        assert x.dist_ray2segment(v, b, a) == approx(2.0 * sqrt(2.0))

    # Отрезок полностью лежит на луче, расстояние положительное
    def test_dist_ray2segment16(self):
        x = R2Point(0.0, 0.0)
        v = R2Point(10.0, 10.0)
        a = R2Point(2.0, 2.0)
        b = R2Point(3.0, 3.0)
        assert x.dist_ray2segment(v, b, a) == approx(2.0 * sqrt(2.0))

    ##########################################################################
    #
    # Тесты на метод нахождения расстояния от (возможно вырожденного)
    # отрезка [p, q] до прямой ax + by + c = 0
    #
    ##########################################################################

    # Невырожденный отрезок лежит на прямой
    def test_dist_seg2line1(self):
        a, b, c = 0.0, 1.0, 0.0
        p, q = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point.dist_seg2line(p, q, a, b, c) == approx(0.0)

    # Невырожденный отрезок параллелен прямой
    def test_dist_seg2line2(self):
        a, b, c = 0.0, 1.0, 0.0
        p, q = R2Point(0.0, -1.0), R2Point(1.0, -1.0)
        assert R2Point.dist_seg2line(p, q, a, b, c) == approx(1.0)

    # Невырожденный отрезок не параллелен прямой и не пересекает её
    def test_dist_seg2line3(self):
        a, b, c = 0.0, 1.0, 0.0
        p, q = R2Point(0.0, 1.0), R2Point(1.0, 2.0)
        assert R2Point.dist_seg2line(p, q, a, b, c) == approx(1.0)

    # Невырожденный отрезок перпендикулярен прямой и касается её
    def test_dist_seg2line4(self):
        a, b, c = 0.0, 1.0, 0.0
        p, q = R2Point(-1.0, -1.0), R2Point(-1.0, 0.0)
        assert R2Point.dist_seg2line(p, q, a, b, c) == approx(0.0)

    # Невырожденный отрезок пересекает прямую
    def test_dist_seg2line5(self):
        a, b, c = 0.0, 1.0, 0.0
        p, q = R2Point(-3.0, -1.0), R2Point(-1.0, 2.0)
        assert R2Point.dist_seg2line(p, q, a, b, c) == approx(0.0)

    # Невырожденный отрезок касается прямой
    def test_dist_seg2line6(self):
        a, b, c = 1.0, 1.0, -1.0
        p, q = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point.dist_seg2line(p, q, a, b, c) == approx(0.0)

    # Невырожденный отрезок пересекает прямую
    def test_dist_seg2line7(self):
        a, b, c = 1.0, 1.0, -1.0
        p, q = R2Point(0.0, 0.0), R2Point(0.0, 2.0)
        assert R2Point.dist_seg2line(p, q, a, b, c) == approx(0.0)

    # Невырожденный отрезок не пересекает прямую
    def test_dist_seg2line8(self):
        a, b, c = 1.0, 1.0, -1.0
        p, q = R2Point(0.0, 0.0), R2Point(-1.0, 0.0)
        assert R2Point.dist_seg2line(p, q, a, b, c) == approx(sqrt(2.0)/2.0)

    # Вырожденный отрезок (точка) не лежит на прямой
    def test_dist_seg2line9(self):
        a, b, c = 1.0, 1.0, -1.0
        p, q = R2Point(0.0, 0.0), R2Point(0.0, 0.0)
        assert R2Point.dist_seg2line(p, q, a, b, c) == approx(sqrt(2.0)/2.0)

    # Вырожденный отрезок (точка) лежит на прямой
    def test_dist_seg2line10(self):
        a, b, c = 1.0, 1.0, -1.0
        p, q = R2Point(1.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point.dist_seg2line(p, q, a, b, c) == approx(0.0)

    ##########################################################################
    #
    # Тесты на метод нахождения расстояниямежду двумя
    # (возможно вырожденными) отрезками [p, q] и [r, s]
    #
    ##########################################################################

    # Оба отрезка вырождены и совпадают
    def test_dist_seg2seg01(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        r = R2Point(0.0, 0.0)
        s = R2Point(0.0, 0.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(0.0)

    # Оба отрезка вырождены и различны
    def test_dist_seg2seg02(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        r = R2Point(1.0, 1.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(sqrt(2.0))

    # Один из отрезков вырожден; точка — конец отрезка
    def test_dist_seg2seg03(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        r = R2Point(0.0, 0.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(0.0)

    # Один из отрезков вырожден; точка — середина отрезка
    def test_dist_seg2seg04(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(0.0)

    # Один из отрезков вырожден; точка лежит на линии отрезка
    def test_dist_seg2seg05(self):
        p = R2Point(2.0, 2.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(sqrt(2.0))

    # Один из отрезков вырожден; точка в «полосе» отрезка
    def test_dist_seg2seg06(self):
        p = R2Point(-1.0, 1.0)
        q = R2Point(-1.0, 1.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(sqrt(2.0))

    # Один из отрезков вырожден; точка вне «полосы» отрезка
    def test_dist_seg2seg07(self):
        p = R2Point(3.0, 0.0)
        q = R2Point(3.0, 0.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(sqrt(5.0))

    # Отрезки не вырождены; лежат на одной прямой и касаются друг друга
    def test_dist_seg2seg08(self):
        p = R2Point(1.0, 1.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(0.0)

    # Отрезки не вырождены; лежат на одной прямой и перекрываются
    def test_dist_seg2seg09(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(0.0)

    # Отрезки не вырождены; лежат на одной прямой и один внутри другого
    def test_dist_seg2seg10(self):
        p = R2Point(-2.0, -2.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(0.0)

    # Отрезки не вырождены; лежат на одной прямой и не пересекаются
    def test_dist_seg2seg11(self):
        p = R2Point(3.0, 3.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(sqrt(2.0))

    # Отрезки не вырождены и не лежат на одной прямой,
    # при этом они параллельны; расстояние — длина перпендикуляра
    def test_dist_seg2seg12(self):
        p = R2Point(1.0, 2.0)
        q = R2Point(0.0, 1.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(sqrt(2.0)/2.0)

    # Отрезки не вырождены и не лежат на одной прямой
    # при этом они параллельны; расстояние — не длина перпендикуляра
    def test_dist_seg2seg13(self):
        p = R2Point(1.0, 2.0)
        q = R2Point(2.0, 3.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(1.0)

    # Отрезки не вырождены и не параллельны; расстояние — длина перпендикуляра
    def test_dist_seg2seg14(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(1.0, 1.0)
        s = R2Point(3.0, 3.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(1.0)

    # Отрезки не вырождены и не параллельны;
    # расстояние — не длина перпендикуляра
    def test_dist_seg2seg15(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(4.0, 4.0)
        s = R2Point(3.0, 3.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(sqrt(10.0))

    # Отрезки не вырождены и не параллельны,
    # при этом конец одного лежит на продолжении другого
    def test_dist_seg2seg16(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(4.0, 4.0)
        s = R2Point(3.0, 0.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(1.0)

    # Отрезки не вырождены и не параллельны; имеют общую вершину
    def test_dist_seg2seg17(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(0.0, 0.0)
        s = R2Point(3.0, 0.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(0.0)

    # Отрезки не вырождены и не параллельны; один начинается в середине другого
    def test_dist_seg2seg18(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(1.0, 0.0)
        s = R2Point(1.0, 3.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(0.0)

    # Отрезки не вырождены и не параллельны; просто пересекаются
    def test_dist_seg2seg19(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(1.0, -1.0)
        s = R2Point(1.0, 3.0)
        assert R2Point.dist_seg2seg(p, q, r, s) == approx(0.0)

    ##########################################################################
    #
    # Тесты на метод нахождения расстояния от (возможно вырожденного) отрезка
    # [p, q] до заполненного заведомо невырожденного треугольника [a, b, c]
    #
    ##########################################################################

    # Отрезок вырожден и лежит внутри треугольника
    def test_dist_seg2triangle01(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(0.0)

    # Отрезок невырожден и лежит внутри треугольника
    def test_dist_seg2triangle02(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.1, 0.1)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(0.0)

    # Отрезок вырожден и (точка) лежит на одной из сторон треугольника
    def test_dist_seg2triangle03(self):
        p = R2Point(0.5, 0.0)
        q = R2Point(0.5, 0.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(0.0)

    # Отрезок невырожден и весь лежит на одной из сторон треугольника
    def test_dist_seg2triangle04(self):
        p = R2Point(0.5, 0.0)
        q = R2Point(0.7, 0.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(0.0)

    # Отрезок невырожден и чaстично лежит на одной из сторон треугольника
    def test_dist_seg2triangle05(self):
        p = R2Point(0.5, 0.0)
        q = R2Point(2.0, 0.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(0.0)

    # Отрезок невырожден и «касается» треугольника
    def test_dist_seg2triangle06(self):
        p = R2Point(1.0, 0.0)
        q = R2Point(2.0, 0.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(0.0)

    # Отрезок невырожден; один из концов внутри треугольника;
    # отрезок пересекает одну из сторон треугольника
    def test_dist_seg2triangle07(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(10.0, 10.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(0.0)

    # Отрезок невырожден; один из концов внутри треугольника;
    # отрезок проходит через вершину треугольника
    def test_dist_seg2triangle08(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(-10.0, -10.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, -1.0)
        c = R2Point(0.0, -1.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(0.0)

    # Отрезок невырожден; оба конца расположены вне треугольника;
    # отрезок пересекает две стороны треугольника
    def test_dist_seg2triangle09(self):
        p = R2Point(-1.0, 1.0)
        q = R2Point(1.0, -1.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(0.0)

    # Отрезок невырожден; оба конца расположены вне треугольника;
    # отрезок проходит через одну из вершин треугольника
    def test_dist_seg2triangle10(self):
        p = R2Point(1.0, -1.0)
        q = R2Point(1.0, 1.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(0.0)

    # Отрезок невырожден; оба конца расположены вне треугольника;
    # отрезок проходит через одну из вершин треугольника и пересекает
    # противоположную сторону
    def test_dist_seg2triangle11(self):
        p = R2Point(-10.0, -10.0)
        q = R2Point(10.0, 10.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(0.0)

    # Отрезок вырожден и (точка) находится вне треугольника
    def test_dist_seg2triangle12(self):
        p = R2Point(0.5, -1.0)
        q = R2Point(0.5, -1.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(0.0, 1.0)
        c = R2Point(1.0, 0.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(1.0)

    # Отрезок вырожден и (точка) находится вне треугольника
    def test_dist_seg2triangle13(self):
        p = R2Point(-1.0, -1.0)
        q = R2Point(-1.0, -1.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(0.0, 1.0)
        c = R2Point(1.0, 0.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(sqrt(2.0))

    # Отрезок невырожден и полностью лежит вне треугольника
    def test_dist_seg2triangle14(self):
        p = R2Point(-1.0, -1.0)
        q = R2Point(3.0, -1.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(0.0, 1.0)
        c = R2Point(1.0, 0.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(1.0)

    # Отрезок невырожден и полностью лежит вне треугольника
    def test_dist_seg2triangle15(self):
        p = R2Point(0.0, -2.0)
        q = R2Point(-2.0, 0.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(0.0, 1.0)
        c = R2Point(1.0, 0.0)
        assert R2Point.dist_seg2triangle(p, q, a, b, c) == approx(sqrt(2.0))

    ##########################################################################
    #
    # Тесты на метод нахождения пересечения двух (возможно вырожденных)
    # отрезков [p, q] и [r, s]
    #
    ##########################################################################

    # Оба отрезка вырождены и совпадают
    def test_seg2seg01(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        r = R2Point(0.0, 0.0)
        s = R2Point(0.0, 0.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res[0] == res[1] == p

    # Оба отрезка вырождены и различны
    def test_seg2seg02(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        r = R2Point(1.0, 1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res is None

    # Оба отрезка вырождены и различны
    def test_seg2seg03(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        r = R2Point(1.0, 1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res is None

    # Один из отрезков вырожден; он (точка) — конец второго отрезка
    def test_seg2seg04(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        r = R2Point(0.0, 0.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res[0] == res[1] == p

    # Один из отрезков вырожден; он (точка) — конец второго отрезка
    def test_seg2seg05(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        r = R2Point(0.0, 0.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res[0] == res[1] == p

    # Один из отрезков вырожден; он (точка) — середина второго отрезка
    def test_seg2seg06(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res[0] == res[1] == p

    # Один из отрезков вырожден; он (точка) — середина второго отрезка
    def test_seg2seg07(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res[0] == res[1] == p

    # Один из отрезков вырожден; он (точка) лежит на линии второго отрезка
    def test_seg2seg08(self):
        p = R2Point(2.0, 2.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res is None

    # Один из отрезков вырожден; он (точка) лежит на линии второго отрезка
    def test_seg2seg09(self):
        p = R2Point(2.0, 2.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res is None

    # Один из отрезков вырожден; он (точка) лежит в «полосе» второго отрезка
    def test_seg2seg10(self):
        p = R2Point(-1.0, 1.0)
        q = R2Point(-1.0, 1.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res is None

    # Один из отрезков вырожден; он (точка) лежит в «полосе» второго отрезка
    def test_seg2seg11(self):
        p = R2Point(-1.0, 1.0)
        q = R2Point(-1.0, 1.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res is None

    # Один из отрезков вырожден; он (точка) лежит вне «полосы» второго отрезка
    def test_seg2seg12(self):
        p = R2Point(3.0, 0.0)
        q = R2Point(3.0, 0.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res is None

    # Один из отрезков вырожден; он (точка) лежит вне «полосы» второго отрезка
    def test_seg2seg13(self):
        p = R2Point(3.0, 0.0)
        q = R2Point(3.0, 0.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res is None

    # Отрезки не вырождены; лежат на одной прямой и касаются друг друга
    def test_seg2seg14(self):
        p = R2Point(1.0, 1.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res[0].approx(p) and res[1].approx(p)

    # Отрезки не вырождены; лежат на одной прямой и касаются друг друга
    def test_seg2seg15(self):
        p = R2Point(1.0, 1.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res[0].approx(p) and res[1].approx(p)

    # Отрезки не вырождены; лежат на одной прямой и перекрываются
    def test_seg2seg16(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert (res[0].approx(p) and res[1].approx(s)) or \
            (res[0].approx(s) and res[1].approx(p))

    # Отрезки не вырождены; лежат на одной прямой и перекрываются
    def test_seg2seg17(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert (res[0].approx(p) and res[1].approx(s)) or \
            (res[0].approx(s) and res[1].approx(p))

    # Отрезки не вырождены; лежат на одной прямой и один внутри другого
    def test_seg2seg18(self):
        p = R2Point(-2.0, -2.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert (res[0] == r and res[1] == s) or \
            (res[0] == s and res[1] == r)

    # Отрезки не вырождены; лежат на одной прямой и один внутри другого
    def test_seg2seg19(self):
        p = R2Point(-2.0, -2.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert (res[0] == r and res[1] == s) or \
            (res[0] == s and res[1] == r)

    # Отрезки не вырождены; лежат на одной прямой и не пересекаются
    def test_seg2seg20(self):
        p = R2Point(3.0, 3.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res is None

    # Отрезки не вырождены; лежат на одной прямой и не пересекаются
    def test_seg2seg21(self):
        p = R2Point(3.0, 3.0)
        q = R2Point(2.0, 2.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res is None

    # Отрезки не вырождены и не лежат на одной прямой;
    # они параллельны, расстояние — перпендикуляр
    def test_seg2seg22(self):
        p = R2Point(1.0, 2.0)
        q = R2Point(0.0, 1.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res is None

    # Отрезки не вырождены и не лежат на одной прямой;
    # они параллельны, расстояние — перпендикуляр
    def test_seg2seg23(self):
        p = R2Point(1.0, 2.0)
        q = R2Point(0.0, 1.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res is None

    # Отрезки не вырождены и не лежат на одной прямой;
    # они параллельны, расстояние — не перпендикуляр
    def test_seg2seg24(self):
        p = R2Point(1.0, 2.0)
        q = R2Point(2.0, 3.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res is None

    # Отрезки не вырождены и не лежат на одной прямой;
    # они параллельны, расстояние — не перпендикуляр
    def test_seg2seg25(self):
        p = R2Point(1.0, 2.0)
        q = R2Point(2.0, 3.0)
        r = R2Point(-1.0, -1.0)
        s = R2Point(1.0, 1.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res is None

    # Отрезки не вырождены и не параллельны; расстояние — перпендикуляр
    def test_seg2seg26(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(1.0, 1.0)
        s = R2Point(3.0, 3.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res is None

    # Отрезки не вырождены и не параллельны; расстояние — перпендикуляр
    def test_seg2seg27(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(1.0, 1.0)
        s = R2Point(3.0, 3.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res is None

    # Отрезки не вырождены и не параллельны; расстояние — не перпендикуляр
    def test_seg2seg28(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(4.0, 4.0)
        s = R2Point(3.0, 3.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res is None

    # Отрезки не вырождены и не параллельны; расстояние — не перпендикуляр
    def test_seg2seg29(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(4.0, 4.0)
        s = R2Point(3.0, 3.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res is None

    # Отрезки не вырождены и не параллельны;
    # конец одного расположен на продолжении другого
    def test_seg2seg30(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(4.0, 4.0)
        s = R2Point(3.0, 0.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res is None

    # Отрезки не вырождены и не параллельны;
    # конец одного расположен на продолжении другого
    def test_seg2seg31(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(4.0, 4.0)
        s = R2Point(3.0, 0.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res is None

    # Отрезки не вырождены и не параллельны; они имеют общую вершину
    def test_seg2seg32(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(0.0, 0.0)
        s = R2Point(0.0, 3.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res[0] == res[1] == p

    # Отрезки не вырождены и не параллельны; они имеют общую вершину
    def test_seg2seg33(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(0.0, 0.0)
        s = R2Point(0.0, 3.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res[0] == res[1] == p

    # Отрезки не вырождены и не параллельны; один начинается в середине другого
    def test_seg2seg34(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(1.0, 0.0)
        s = R2Point(1.0, 3.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res[0] == res[1] == r

    # Отрезки не вырождены и не параллельны; один начинается в середине другого
    def test_seg2seg35(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(1.0, 0.0)
        s = R2Point(1.0, 3.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res[0] == res[1] == r

    # Отрезки не вырождены и не параллельны; просто пересекаются
    def test_seg2seg36(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(1.0, -1.0)
        s = R2Point(1.0, 3.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res[0] == res[1] == R2Point(1.0, 0.0)

    # Отрезки не вырождены и не параллельны; просто пересекаются
    def test_seg2seg37(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(1.0, -1.0)
        s = R2Point(1.0, 3.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res[0] == res[1] == R2Point(1.0, 0.0)

    # Отрезки не вырождены и не параллельны; просто пересекаются
    def test_seg2seg38(self):
        p = R2Point(-1.0, -1.0)
        q = R2Point(1.0, 1.0)
        r = R2Point(0.0, 1.0)
        s = R2Point(1.0, 0.0)
        res = R2Point.seg2seg(p, q, r, s)
        assert res[0] == res[1] == R2Point(0.5, 0.5)

    # Отрезки не вырождены и не параллельны; просто пересекаются
    def test_seg2seg39(self):
        p = R2Point(-1.0, -1.0)
        q = R2Point(1.0, 1.0)
        r = R2Point(0.0, 1.0)
        s = R2Point(1.0, 0.0)
        res = R2Point.seg2seg(r, s, p, q)
        assert res[0] == res[1] == R2Point(0.5, 0.5)

    ##########################################################################
    #
    # Тесты на метод нахождения пересечения (возможно вырожденного) отрезка
    # [p, q] с заполненным заведомо невырожденным треугольником [a, b, c]
    #
    ##########################################################################

    # Отрезок вырожден и лежит внутри треугольника
    def test_seg_in_triangle01(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.0, 0.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res[0].approx(p) and res[1].approx(p)

    # Отрезок невырожден и лежит внутри треугольника
    def test_seg_in_triangle02(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(0.1, 0.1)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res[0].approx(p) and res[1].approx(q) or \
            res[0].approx(q) and res[1].approx(p)

    # Отрезок вырожден и (точка) лежит на одной из сторон треугольника
    def test_seg_in_triangle03(self):
        p = R2Point(0.5, 0.0)
        q = R2Point(0.5, 0.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res[0].approx(p) and res[1].approx(p)

    # Отрезок невырожден и весь лежит на одной из сторон треугольника
    def test_seg_in_triangle04(self):
        p = R2Point(0.5, 0.0)
        q = R2Point(0.7, 0.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res[0].approx(p) and res[1].approx(q) or \
            res[0].approx(q) and res[1].approx(p)

    # Отрезок невырожден и чaстично лежит на одной из сторон треугольника
    def test_seg_in_triangle05(self):
        p = R2Point(0.5, 0.0)
        q = R2Point(2.0, 0.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res[0].approx(p) and res[1].approx(b) or \
            res[0].approx(b) and res[1].approx(p)

    # Отрезок невырожден и «касается» треугольника
    def test_seg_in_triangle06(self):
        p = R2Point(1.0, 0.0)
        q = R2Point(2.0, 0.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res[0].approx(p) and res[1].approx(p)

    # Отрезок невырожден; один из концов внутри треугольника;
    # отрезок пересекает одну из сторон треугольника
    def test_seg_in_triangle07(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(10.0, 10.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res[0].approx(p) and res[1].approx(R2Point(0.5, 0.5)) or \
            res[0].approx(R2Point(0.5, 0.5)) and res[1].approx(p)

    # Отрезок невырожден; один из концов внутри треугольника;
    # отрезок проходит через вершину треугольника
    def test_seg_in_triangle08(self):
        p = R2Point(0.0, 0.0)
        q = R2Point(-10.0, -10.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        print(res[0].__dict__, res[1].__dict__)
        assert res[0].approx(p) and res[1].approx(a) or \
            res[0].approx(a) and res[1].approx(p)

    # Отрезок невырожден; оба конца расположены вне треугольника;
    # отрезок пересекает две стороны треугольника
    def test_seg_in_triangle09(self):
        p = R2Point(-1.0, 1.0)
        q = R2Point(1.0, -1.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        d = R2Point(1.0/3.0, -1.0/3.0)
        e = R2Point(-1.0/3.0, 1.0/3.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res[0].approx(d) and res[1].approx(e) or \
            res[0].approx(e) and res[1].approx(d)

    # Отрезок невырожден; оба конца расположены вне треугольника;
    # отрезок проходит через одну из вершин треугольника
    def test_seg_in_triangle10(self):
        p = R2Point(1.0, -1.0)
        q = R2Point(1.0, 1.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res[0].approx(b) and res[1].approx(b)

    # Отрезок невырожден; оба конца расположены вне треугольника;
    # отрезок проходит через одну из вершин треугольника и пересекает
    # противоположную сторону
    def test_seg_in_triangle11(self):
        p = R2Point(-10.0, -10.0)
        q = R2Point(10.0, 10.0)
        a = R2Point(-1.0, -1.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        d = R2Point(0.5, 0.5)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res[0].approx(a) and res[1].approx(d) or \
            res[0].approx(d) and res[1].approx(a)

    # Отрезок вырожден и (точка) находится вне треугольника
    def test_seg_in_triangle12(self):
        p = R2Point(0.5, -1.0)
        q = R2Point(0.5, -1.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(0.0, 1.0)
        c = R2Point(1.0, 0.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res is None

    # Отрезок вырожден и (точка) находится вне треугольника
    def test_seg_in_triangle13(self):
        p = R2Point(-1.0, -1.0)
        q = R2Point(-1.0, -1.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(0.0, 1.0)
        c = R2Point(1.0, 0.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res is None

    # Отрезок невырожден и полностью лежит вне треугольника
    def test_seg_in_triangle14(self):
        p = R2Point(-1.0, -1.0)
        q = R2Point(3.0, -1.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(0.0, 1.0)
        c = R2Point(1.0, 0.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res is None

    # Отрезок невырожден и полностью лежит вне треугольника
    def test_seg_in_triangle15(self):
        p = R2Point(0.0, -2.0)
        q = R2Point(-2.0, 0.0)
        a = R2Point(0.0, 0.0)
        b = R2Point(0.0, 1.0)
        c = R2Point(1.0, 0.0)
        res = R2Point.seg_in_triangle(p, q, a, b, c)
        assert res is None
