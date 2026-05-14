"""Tests for cimbuilder.object_builder.load.new_energy_consumer."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.load.new_energy_consumer import new_energy_consumer


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    n1 = connectivity_nodes["node1"]

    load = new_energy_consumer(net, sub, "L1", node=n1, p_kW=500, q_kVAr=100)

    assert isinstance(load, cim.EnergyConsumer)
    assert load.name == "L1"
    assert load.EquipmentContainer is sub
    assert isinstance(load.p, cim.ActivePower)
    assert float(load.p) == 500_000  # kW → W
    assert isinstance(load.q, cim.ReactivePower)
    assert float(load.q) == 100_000  # kVAr → VAr
    assert load.grounded is False

    assert len(load.Terminals) == 1
    assert load.Terminals[0].sequenceNumber == 1
    assert load.Terminals[0].ConnectivityNode is n1


def test_node_by_name(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    load = new_energy_consumer(net, sub, "L2", node="node1", p_kW=10)
    assert load.Terminals[0].ConnectivityNode is connectivity_nodes["node1"]


def test_pfixed_qfixed(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    load = new_energy_consumer(
        net, sub, "L3", node=connectivity_nodes["node1"],
        pfixed_kW=200, qfixed_kVAr=50, customer_count=10,
    )
    assert isinstance(load.pfixed, cim.ActivePower)
    assert float(load.pfixed) == 200_000
    assert isinstance(load.qfixed, cim.ReactivePower)
    assert float(load.qfixed) == 50_000
    assert load.customerCount == 10


def test_added_to_graph(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    load = new_energy_consumer(net, sub, "L4", node=connectivity_nodes["node1"], p_kW=100)
    assert load in net.graph.get(cim.EnergyConsumer, {}).values()
