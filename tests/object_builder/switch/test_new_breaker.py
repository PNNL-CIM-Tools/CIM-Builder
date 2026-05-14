"""Tests for cimbuilder.object_builder.switch.new_breaker."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch.new_breaker import new_breaker


def test_new_breaker_basic(simple_substation_network, connectivity_nodes):
    """Create a Breaker between two ConnectivityNodes and verify the graph."""
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    n1 = connectivity_nodes["node1"]
    n2 = connectivity_nodes["node2"]

    breaker = new_breaker(net, sub, "BR1", node1=n1, node2=n2)

    assert isinstance(breaker, cim.Breaker)
    assert breaker.name == "BR1"
    assert breaker.EquipmentContainer is sub
    assert breaker.open is False
    assert breaker.normalOpen is False
    assert breaker.retained is True
    assert breaker.BaseVoltage is None

    assert len(breaker.Terminals) == 2
    t1, t2 = breaker.Terminals
    assert t1.sequenceNumber == 1
    assert t2.sequenceNumber == 2
    assert t1.ConductingEquipment is breaker
    assert t2.ConductingEquipment is breaker
    assert t1.ConnectivityNode is n1
    assert t2.ConnectivityNode is n2



def test_new_breaker_with_base_voltage(simple_substation_network, connectivity_nodes):
    """Explicit base_voltage kwarg is respected."""
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    bv = simple_substation_network["base_voltage"]

    breaker = new_breaker(
        net, sub, "BR2",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        base_voltage=bv,
    )
    assert breaker.BaseVoltage is bv


def test_new_breaker_open_and_normal_open(simple_substation_network, connectivity_nodes):
    """open/normal_open/retained flags pass through."""
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    breaker = new_breaker(
        net, sub, "BR3",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        open=True,
        normal_open=True,
        retained=False,
    )
    assert breaker.open is True
    assert breaker.normalOpen is True
    assert breaker.retained is False


def test_new_breaker_node_by_name(simple_substation_network, connectivity_nodes):
    """Passing node names (str) instead of objects resolves via terminal_to_node."""
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    breaker = new_breaker(net, sub, "BR4", node1="node1", node2="node2")

    t1, t2 = breaker.Terminals
    assert t1.ConnectivityNode is connectivity_nodes["node1"]
    assert t2.ConnectivityNode is connectivity_nodes["node2"]


def test_new_breaker_added_to_graph(simple_substation_network, connectivity_nodes):
    """Breaker and both terminals are present in the GraphModel."""
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    breaker = new_breaker(
        net, sub, "BR5",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
    )

    net.get_all_edges(cim.Breaker)
    net.get_all_edges(cim.Terminal)

    breakers_in_graph = list(net.graph.get(cim.Breaker, {}).values())
    assert breaker in breakers_in_graph

    terminals_in_graph = list(net.graph.get(cim.Terminal, {}).values())
    assert breaker.Terminals[0] in terminals_in_graph
    assert breaker.Terminals[1] in terminals_in_graph


def test_new_breaker_deterministic_uuid(simple_substation_network, connectivity_nodes):
    """Same name + same node pair yields the same UUID across two independent creations."""
    from cimgraph.databases import XMLFile
    from cimgraph.models import DistributedArea
    cim = get_cim()

    # Second independent network with identical structure
    net2_conn = XMLFile(filename=str(simple_substation_network["path"].parent / "second.xml"))
    sub2 = cim.Substation(name="test_sub")
    sub2.uuid(name="test_sub")
    net2 = DistributedArea(connection=net2_conn, container=sub2, distributed=False)
    net2.add_to_graph(sub2)

    n1b = cim.ConnectivityNode(name="node1")
    n1b.uuid(name="node1")
    n1b.ConnectivityNodeContainer = sub2
    net2.add_to_graph(n1b)
    n2b = cim.ConnectivityNode(name="node2")
    n2b.uuid(name="node2")
    n2b.ConnectivityNodeContainer = sub2
    net2.add_to_graph(n2b)

    b1 = new_breaker(
        simple_substation_network["network"],
        simple_substation_network["substation"],
        "BR_DET",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
    )
    b2 = new_breaker(net2, sub2, "BR_DET", node1=n1b, node2=n2b)

    assert b1.mRID == b2.mRID
