"""Tests for cimbuilder.object_builder.generic.new_one_terminal_object."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.generic.new_one_terminal_object import new_one_terminal_object


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    obj = new_one_terminal_object(
        net, sub, "EC1",
        node=connectivity_nodes["node1"],
        class_type=cim.EnergyConsumer,
    )
    assert isinstance(obj, cim.EnergyConsumer)
    assert obj.name == "EC1"
    assert obj.EquipmentContainer is sub
    assert len(obj.Terminals) == 1
    assert obj.Terminals[0].ConnectivityNode is connectivity_nodes["node1"]
