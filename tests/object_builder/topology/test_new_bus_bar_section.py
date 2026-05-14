"""Tests for cimbuilder.object_builder.topology.new_bus_bar_section."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.topology.new_bus_bar_section import new_bus_bar_section


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    n1 = connectivity_nodes["node1"]

    bus = new_bus_bar_section(net, sub, "BB1", node=n1)
    assert isinstance(bus, cim.BusbarSection)
    assert bus.name == "BB1"
    assert bus.EquipmentContainer is sub
    assert len(bus.Terminals) == 1
    assert bus.Terminals[0].sequenceNumber == 1
    assert bus.Terminals[0].ConnectivityNode is n1


def test_with_ip_max(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    bus = new_bus_bar_section(net, sub, "BB2", node=connectivity_nodes["node1"], ip_max_A=2000.0)
    assert isinstance(bus.ipMax, cim.CurrentFlow)
    assert float(bus.ipMax) == 2000.0


def test_added_to_graph(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    bus = new_bus_bar_section(net, sub, "BB3", node=connectivity_nodes["node1"])
    assert bus in net.graph.get(cim.BusbarSection, {}).values()
