"""Phase 3 NameIndex tests (design: CIMTBL_DESIGN.md §5.5).

Scoped per-class name -> object lookup: .add() is idempotent for the same
object, raises on a different object claiming an already-used name, and
.get() is a plain O(1) dict lookup that returns None on a miss.
"""

import pytest

from cimbuilder.core.name_index import NameIndex


class _FakeObj:
    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier


class _OtherFakeObj(_FakeObj):
    pass


def test_get_on_empty_index_returns_none():
    index = NameIndex()
    assert index.get(_FakeObj, 'anything') is None


def test_add_then_get_round_trips():
    index = NameIndex()
    obj = _FakeObj('base_115', 1)
    index.add(obj)
    assert index.get(_FakeObj, 'base_115') is obj


def test_readding_same_object_is_a_no_op():
    index = NameIndex()
    obj = _FakeObj('base_115', 1)
    index.add(obj)
    index.add(obj)
    assert index.get(_FakeObj, 'base_115') is obj


def test_different_object_same_class_same_name_raises():
    index = NameIndex()
    index.add(_FakeObj('base_115', 1))
    with pytest.raises(ValueError, match=r"duplicate name 'base_115'"):
        index.add(_FakeObj('base_115', 2))


def test_same_name_different_classes_do_not_collide():
    index = NameIndex()
    a = _FakeObj('sw1', 1)
    b = _OtherFakeObj('sw1', 2)
    index.add(a)
    index.add(b)
    assert index.get(_FakeObj, 'sw1') is a
    assert index.get(_OtherFakeObj, 'sw1') is b
