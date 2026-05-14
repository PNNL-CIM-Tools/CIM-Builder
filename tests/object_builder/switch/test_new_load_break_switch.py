"""Tests for cimbuilder.object_builder.switch.new_load_break_switch."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch.new_load_break_switch import new_load_break_switch


def test_new_load_break_switch_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    sw = new_load_break_switch(
        net, sub, "LBS1",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
    )
    assert isinstance(sw, cim.LoadBreakSwitch)
    assert sw.name == "LBS1"
    assert len(sw.Terminals) == 2


def test_new_load_break_switch_with_breaking_capacity(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    sw = new_load_break_switch(
        net, sub, "LBS2",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        breaking_capacity_A=600.0,
    )
    assert isinstance(sw.breakingCapacity, cim.CurrentFlow)
    assert float(sw.breakingCapacity) == 600.0
