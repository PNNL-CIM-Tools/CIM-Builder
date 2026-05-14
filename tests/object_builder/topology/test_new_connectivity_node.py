"""Tests for cimbuilder.object_builder.topology.new_connectivity_node."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.topology.new_connectivity_node import new_connectivity_node


def test_basic(simple_substation_network):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    node = new_connectivity_node(net, sub, "n_main")
    assert isinstance(node, cim.ConnectivityNode)
    assert node.name == "n_main"
    assert node.ConnectivityNodeContainer is sub
    assert node in net.graph.get(cim.ConnectivityNode, {}).values()


def test_with_base_voltage(simple_substation_network):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    bv = simple_substation_network["base_voltage"]

    node = new_connectivity_node(net, sub, "n2", base_voltage=bv)
    assert node.BaseVoltage is bv
