"""Tests for cimbuilder.object_builder.switch.new_fuse."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch.new_fuse import new_fuse


def test_new_fuse_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    fuse = new_fuse(
        net, sub, "F1",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
    )
    assert isinstance(fuse, cim.Fuse)
    assert fuse.name == "F1"
    assert len(fuse.Terminals) == 2
    assert fuse.open is False


def test_new_fuse_with_rated_current(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    fuse = new_fuse(
        net, sub, "F2",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        rated_current_A=100.0,
    )
    assert isinstance(fuse.ratedCurrent, cim.CurrentFlow)
    assert float(fuse.ratedCurrent) == 100.0


def test_new_fuse_blown_state(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    fuse = new_fuse(
        net, sub, "F3",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        open=True,
    )
    assert fuse.open is True
