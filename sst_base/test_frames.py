import pytest

from .frames import *

@pytest.fixture
def unit_frame():
    p1 = vec(1, 0, 0)
    p2 = vec(1, 0, 1)
    p3 = vec(1, 1, 0)
    unit_frame = Frame(p1, p2, p3)
    return unit_frame

@pytest.fixture
def unit_frame90():
    p1 = vec(1, 1, 0)
    p2 = vec(1, 1, 1)
    p3 = vec(0, 1, 0)
    unit_frame90 = Frame(p1, p2, p3)
    return unit_frame90

@pytest.fixture
def compound_frame():
    pp1 = vec(1, 1, 0)
    pp2 = vec(1, 1, 1)
    pp3 = vec(1, 2, 0)
    parent = Frame(pp1, pp2, pp3)
    
    p1 = vec(0, 0, 0)
    p2 = vec(0, 1, 0)
    p3 = vec(0, 0, -1)
    compound_frame = Frame(p1, p2, p3, parent=parent)
    return compound_frame

def test_unit_frame_roffset(unit_frame, unit_frame90):
    assert unit_frame.r0 == 0
    assert unit_frame90.r0 == 90
    
def test_frame_to_global(unit_frame):
    v_f = vec(0, 0, 0)
    v_g = vec(1, 0, 0)
    assert np.all(unit_frame.frame_to_global(v_f, rotation="global") == v_g)

    v_f1 = vec(1, 0, 0)
    v_g1 = vec(1, 1, 0)
    assert np.all(unit_frame.frame_to_global(v_f1, rotation="global") == v_g1)

    v_g2 = vec(0, 1, 0)
    assert np.all(np.isclose(unit_frame.frame_to_global(v_f, r=90, rotation="frame"), v_g2))

def test_compound_frame(unit_frame90, compound_frame):
    v1 = vec(0, 0, 0)
    vu1 = unit_frame90.frame_to_global(v1, rotation='global')
    vc1 = compound_frame.frame_to_global(v1, rotation='global')
    assert np.all(np.isclose(vu1, vc1))
    
    v2 = vec(*np.random.rand(3))
    vu2 = unit_frame90.frame_to_global(v2, rotation='global')
    vc2 = compound_frame.frame_to_global(v2, rotation='global')
    assert np.all(np.isclose(vu2, vc2))

    r = 90*np.random.rand()
    vu3 = unit_frame90.frame_to_global(v2, r=r, rotation='frame')
    vc3 = compound_frame.frame_to_global(v2, r=r, rotation='frame')
    assert np.all(np.isclose(vu3, vc3))

    vu4 = unit_frame90.global_to_frame(v2, r=r)
    vc4 = compound_frame.global_to_frame(v2, r=r)
    assert np.all(np.isclose(vu4, vc4))

    manip = vec(*np.random.rand())
    vu5 =   unit_frame90.global_to_frame(v2, manip=manip, r=r)
    vc5 = compound_frame.global_to_frame(v2, manip=manip, r=r)
    assert np.all(np.isclose(vu5, vc5))

@pytest.fixture
def unit_bar():
    p1 = vec(0.5, 0, 0)
    p2 = vec(0.5, 0, 1)
    p3 = vec(0.5, 0.5, 0)
    
    bar = Bar(p1, p2, p3, width=1, height=10, nsides=4)
    return bar

def test_bar_edge_distances(unit_bar):
    assert unit_bar.distance_to_beam(-0.5, 0, -1, 0) == 0
    assert unit_bar.distance_to_beam(-0.5, -0.5, -1, 0) == 0
    assert unit_bar.distance_to_beam(0.5, 0, -1, 0) == 0
    assert unit_bar.distance_to_beam(0, 0, -2, 0) == 0.5

def test_bar_subframe(unit_bar):
    x1, y1, x2, y2 = (1, 1, 2, 2)
    unit_bar.load_subframe(x1, y1, x2, y2, side=1)
