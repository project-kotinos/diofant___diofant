import pytest

from diofant import Float, I, Rational, Symbol, pi, sqrt
from diofant.geometry import Line, Line3D, Point, Point2D, Point3D
from diofant.matrices import Matrix


__all__ = ()

x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)
t = Symbol('t', real=True)
k = Symbol('k', real=True)
x1 = Symbol('x1', real=True)
x2 = Symbol('x2', real=True)
x3 = Symbol('x3', real=True)
y1 = Symbol('y1', real=True)
y2 = Symbol('y2', real=True)
y3 = Symbol('y3', real=True)
z1 = Symbol('z1', real=True)
z2 = Symbol('z2', real=True)
z3 = Symbol('z3', real=True)
half = Rational(1, 2)


def feq(a, b):
    """Test if two floating point values are 'equal'."""
    t = Float("1.0E-10")
    return -t < a - b < t


def test_point():
    p1 = Point(x1, x2)
    p2 = Point(y1, y2)
    p3 = Point(0, 0)
    p4 = Point(1, 1)
    p5 = Point(0, 1)

    assert p1.origin == p3
    assert p1.ambient_dimension == 2

    assert p1 in p1
    assert p1 not in p2
    assert p2.y == y2
    assert (p3 + p4) == p4
    assert (p2 - p1) == Point(y1 - x1, y2 - x2)
    assert p4*5 == Point(5, 5)
    assert -p2 == Point(-y1, -y2)
    pytest.raises(ValueError, lambda: Point(3, I))
    pytest.raises(ValueError, lambda: Point(2*I, I))
    pytest.raises(ValueError, lambda: Point(3 + I, I))

    assert Point(34.05, sqrt(3)) == Point(Rational(681, 20), sqrt(3))
    assert Point.midpoint(p3, p4) == Point(half, half)
    assert Point.midpoint(p1, p4) == Point(half + half*x1, half + half*x2)
    assert Point.midpoint(p2, p2) == p2
    assert p2.midpoint(p2) == p2

    assert Point.distance(p3, p4) == sqrt(2)
    assert Point.distance(p1, p1) == 0
    assert Point.distance(p3, p2) == sqrt(p2.x**2 + p2.y**2)

    p1_1 = Point(x1, x1)
    p1_2 = Point(y2, y2)
    p1_3 = Point(x1 + 1, x1)
    assert Point.is_collinear() is False
    assert Point.is_collinear(p3)
    assert Point.is_collinear(p3, p4)
    assert Point.is_collinear(p3, p4, p1_1, p1_2)
    assert Point.is_collinear(p3, p4, p1_1, p1_3) is False
    assert Point.is_collinear(p3, p3, p4, p5) is False
    line = Line(Point(1, 0), slope=1)
    pytest.raises(TypeError, lambda: Point.is_collinear(line))
    pytest.raises(TypeError, lambda: p1_1.is_collinear(line))

    assert p3.intersection(Point(0, 0)) == [p3]
    assert p3.intersection(p4) == []

    x_pos = Symbol('x', real=True, positive=True)
    p2_1 = Point(x_pos, 0)
    p2_2 = Point(0, x_pos)
    p2_3 = Point(-x_pos, 0)
    p2_4 = Point(0, -x_pos)
    p2_5 = Point(x_pos, 5)
    assert Point.is_concyclic(p2_1)
    assert Point.is_concyclic(p2_1, p2_2)
    assert Point.is_concyclic(p2_1, p2_2, p2_3, p2_4)
    assert Point.is_concyclic(p2_1, p2_2, p2_3, p2_5) is False
    assert Point.is_concyclic(p4, p4 * 2, p4 * 3) is False
    pytest.raises(TypeError, lambda: Point.is_concyclic(p2_1, "123"))

    assert p4.scale(2, 3) == Point(2, 3)
    assert p3.scale(2, 3) == p3

    assert p4.rotate(pi, Point(0.5, 0.5)) == p3
    assert p1.__radd__(p2) == p1.midpoint(p2).scale(2, 2)
    assert (-p3).__rsub__(p4) == p3.midpoint(p4).scale(2, 2)

    assert p4 * 5 == Point(5, 5)
    assert p4 / 5 == Point(0.2, 0.2)

    pytest.raises(ValueError, lambda: Point(0, 0) + 10)

    # Point differences should be simplified
    assert Point(x*(x - 1), y) - Point(x**2 - x, y + 1) == Point(0, -1)

    a, b = Rational(1, 2), Rational(1, 3)
    assert Point(a, b).evalf(2) == \
        Point(a.evalf(2), b.evalf(2))
    pytest.raises(ValueError, lambda: Point(1, 2) + 1)

    # test transformations
    p = Point(1, 0)
    assert p.rotate(pi/2) == Point(0, 1)
    assert p.rotate(pi/2, p) == p
    p = Point(1, 1)
    assert p.scale(2, 3) == Point(2, 3)
    assert p.translate(1, 2) == Point(2, 3)
    assert p.translate(1) == Point(2, 1)
    assert p.translate(y=1) == Point(1, 2)
    assert p.translate(*p.args) == Point(2, 2)

    # Check invalid input for transform
    pytest.raises(ValueError, lambda: p3.transform(p3))
    pytest.raises(ValueError, lambda: p.transform(Matrix([[1, 0], [0, 1]])))


def test_point3D():
    p1 = Point3D(x1, x2, x3)
    p2 = Point3D(y1, y2, y3)
    p3 = Point3D(0, 0, 0)
    p4 = Point3D(1, 1, 1)
    p5 = Point3D(0, 1, 2)

    assert p1 in p1
    assert p1 not in p2
    assert p2.y == y2
    assert (p3 + p4) == p4
    assert (p2 - p1) == Point3D(y1 - x1, y2 - x2, y3 - x3)
    assert p4*5 == Point3D(5, 5, 5)
    assert -p2 == Point3D(-y1, -y2, -y3)

    assert Point(34.05, sqrt(3)) == Point(Rational(681, 20), sqrt(3))
    assert Point3D.midpoint(p3, p4) == Point3D(half, half, half)
    assert Point3D.midpoint(p1, p4) == Point3D(half + half*x1, half + half*x2,
                                               half + half*x3)
    assert Point3D.midpoint(p2, p2) == p2
    assert p2.midpoint(p2) == p2

    assert Point3D.distance(p3, p4) == sqrt(3)
    assert Point3D.distance(p1, p1) == 0
    assert Point3D.distance(p3, p2) == sqrt(p2.x**2 + p2.y**2 + p2.z**2)

    p1_1 = Point3D(x1, x1, x1)
    p1_2 = Point3D(y2, y2, y2)
    p1_3 = Point3D(x1 + 1, x1, x1)
    # according to the description in the docs, points are collinear
    # if they like on a single line.  Thus a single point should always
    # be collinear
    assert Point3D.are_collinear(p3)
    assert Point3D.are_collinear(p3, p4)
    assert Point3D.are_collinear(p3, p4, p1_1, p1_2)
    assert Point3D.are_collinear(p3, p4, p1_1, p1_3) is False
    assert Point3D.are_collinear(p3, p3, p4, p5) is False

    assert p3.intersection(Point3D(0, 0, 0)) == [p3]
    assert p3.intersection(p4) == []

    assert p4 * 5 == Point3D(5, 5, 5)
    assert p4 / 5 == Point3D(0.2, 0.2, 0.2)

    pytest.raises(ValueError, lambda: Point3D(0, 0, 0) + 10)

    # Point differences should be simplified
    assert Point3D(x*(x - 1), y, 2) - Point3D(x**2 - x, y + 1, 1) == \
        Point3D(0, -1, 1)

    a, b = Rational(1, 2), Rational(1, 3)
    assert Point(a, b).evalf(2) == \
        Point(a.evalf(2), b.evalf(2))
    pytest.raises(ValueError, lambda: Point(1, 2) + 1)

    # test transformations
    p = Point3D(1, 1, 1)
    assert p.scale(2, 3) == Point3D(2, 3, 1)
    assert p.translate(1, 2) == Point3D(2, 3, 1)
    assert p.translate(1) == Point3D(2, 1, 1)
    assert p.translate(z=1) == Point3D(1, 1, 2)
    assert p.translate(*p.args) == Point3D(2, 2, 2)

    # Test __new__
    assert Point3D(Point3D(1, 2, 3), 4, 5, evaluate=False) == Point3D(1, 2, 3)

    # Test length property returns correctly
    assert p.length == 0
    assert p1_1.length == 0
    assert p1_2.length == 0

    # Test are_colinear type error
    pytest.raises(TypeError, lambda: Point3D.are_collinear(p, x))

    # Test are_coplanar
    planar2 = Point3D(1, -1, 1)
    planar3 = Point3D(-1, 1, 1)
    assert Point3D.are_coplanar(p, planar2, planar3) is True
    assert Point3D.are_coplanar(p, planar2, planar3, p3) is False
    pytest.raises(ValueError, lambda: Point3D.are_coplanar(p, planar2))
    planar2 = Point3D(1, 1, 2)
    planar3 = Point3D(1, 1, 3)
    pytest.raises(ValueError, lambda: Point3D.are_coplanar(p, planar2, planar3))

    # Test Intersection
    assert planar2.intersection(Line3D(p, planar3)) == [Point3D(1, 1, 2)]

    # Test Scale
    assert planar2.scale(1, 1, 1) == planar2
    assert planar2.scale(2, 2, 2, planar3) == Point3D(1, 1, 1)
    assert planar2.scale(1, 1, 1, p3) == planar2

    # Test Transform
    identity = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    assert p.transform(identity) == p
    trans = Matrix([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]])
    assert p.transform(trans) == Point3D(2, 2, 2)
    pytest.raises(ValueError, lambda: p.transform(p))
    pytest.raises(ValueError, lambda: p.transform(Matrix([[1, 0], [0, 1]])))

    # Test Equals
    assert p.equals(x1) is False

    # Test __sub__
    p_2d = Point(0, 0)
    pytest.raises(ValueError, lambda: (p - p_2d))


def test_Point2D():
    p1 = Point2D(1, 5)
    p2 = Point2D(4, 2.5)
    p3 = Point2D(6.1, 3.5)
    assert p1.distance(p2) == sqrt(61)/2
    assert p2.distance(p3) == sqrt(541)/10


def test_sympyissue_9214():
    p1 = Point3D(4, -2, 6)
    p2 = Point3D(1, 2, 3)
    p3 = Point3D(7, 2, 3)

    assert Point3D.are_collinear(p1, p2, p3) is False


def test_direction_cosine():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(1, 1, 1)

    assert p1.direction_cosine(Point3D(1, 0, 0)) == [1, 0, 0]
    assert p1.direction_cosine(Point3D(0, 1, 0)) == [0, 1, 0]
    assert p1.direction_cosine(Point3D(0, 0, pi)) == [0, 0, 1]

    assert p1.direction_cosine(Point3D(5, 0, 0)) == [1, 0, 0]
    assert p1.direction_cosine(Point3D(0, sqrt(3), 0)) == [0, 1, 0]
    assert p1.direction_cosine(Point3D(0, 0, 5)) == [0, 0, 1]

    assert p1.direction_cosine(Point3D(2.4, 2.4, 0)) == [sqrt(2)/2, sqrt(2)/2, 0]
    assert p1.direction_cosine(Point3D(1, 1, 1)) == [sqrt(3)/3, sqrt(3)/3, sqrt(3)/3]
    assert p1.direction_cosine(Point3D(-12, 0, -15)) == [-4*sqrt(41)/41, 0, -5*sqrt(41)/41]

    assert p2.direction_cosine(Point3D(0, 0, 0)) == [-sqrt(3)/3, -sqrt(3)/3, -sqrt(3)/3]
    assert p2.direction_cosine(Point3D(1, 1, 12)) == [0, 0, 1]
    assert p2.direction_cosine(Point3D(12, 1, 12)) == [sqrt(2)/2, 0, sqrt(2)/2]
