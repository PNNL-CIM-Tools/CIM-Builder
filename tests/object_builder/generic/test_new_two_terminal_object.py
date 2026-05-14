"""Tests for cimbuilder.object_builder.generic.new_two_terminal_object."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.generic.new_two_terminal_object import new_two_terminal_object


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    obj = new_two_terminal_object(
        net, sub, "BR1",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        class_type=cim.Breaker,
    )
    assert isinstance(obj, cim.Breaker)
    assert obj.name == "BR1"
    assert len(obj.Terminals) == 2
    assert obj.Terminals[0].ConnectivityNode is connectivity_nodes["node1"]
    assert obj.Terminals[1].ConnectivityNode is connectivity_nodes["node2"]
