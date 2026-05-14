"""Tests for cimbuilder.object_builder.switch.new_disconnector."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch.new_disconnector import new_disconnector


def test_new_disconnector_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    n1 = connectivity_nodes["node1"]
    n2 = connectivity_nodes["node2"]

    sw = new_disconnector(net, sub, "DS1", node1=n1, node2=n2)

    assert isinstance(sw, cim.Disconnector)
    assert sw.name == "DS1"
    assert sw.EquipmentContainer is sub
    assert sw.open is False
    assert sw.normalOpen is False
    assert sw.retained is False
    assert len(sw.Terminals) == 2
    assert sw.Terminals[0].ConnectivityNode is n1
    assert sw.Terminals[1].ConnectivityNode is n2


def test_new_disconnector_open_state(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    sw = new_disconnector(
        net, sub, "DS2",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        open=True, normal_open=True, retained=True,
    )
    assert sw.open is True
    assert sw.normalOpen is True
    assert sw.retained is True


def test_new_disconnector_node_by_name(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    sw = new_disconnector(net, sub, "DS3", node1="node1", node2="node2")
    assert sw.Terminals[0].ConnectivityNode is connectivity_nodes["node1"]
    assert sw.Terminals[1].ConnectivityNode is connectivity_nodes["node2"]


def test_new_disconnector_added_to_graph(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    sw = new_disconnector(
        net, sub, "DS4",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
    )
    assert sw in net.graph.get(cim.Disconnector, {}).values()
