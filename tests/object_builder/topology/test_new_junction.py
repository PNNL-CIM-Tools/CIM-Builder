"""Tests for cimbuilder.object_builder.topology.new_junction."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.topology.new_junction import new_junction


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    n1 = connectivity_nodes["node1"]

    junction = new_junction(net, sub, "J1", node=n1)
    assert isinstance(junction, cim.Junction)
    assert junction.name == "J1"
    assert junction.EquipmentContainer is sub
    assert len(junction.Terminals) == 1
    assert junction.Terminals[0].sequenceNumber == 1
    assert junction.Terminals[0].ConnectivityNode is n1
    assert junction in net.graph.get(cim.Junction, {}).values()


def test_node_by_name(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    junction = new_junction(net, sub, "J2", node="node2")
    assert junction.Terminals[0].ConnectivityNode is connectivity_nodes["node2"]
