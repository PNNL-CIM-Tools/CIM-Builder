"""Tests for cimbuilder.object_builder.generator.new_synchronous_machine."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.generator.new_synchronous_machine import (
    new_synchronous_machine,
)


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    n1 = connectivity_nodes["node1"]

    gen = new_synchronous_machine(
        net, sub, "G1", node=n1,
        p_MW=50, q_MVAr=10, rated_S_MVA=75, rated_U_kV=13.8, rated_power_factor=0.85,
    )
    assert isinstance(gen, cim.SynchronousMachine)
    assert gen.name == "G1"
    assert isinstance(gen.p, cim.ActivePower)
    assert float(gen.p) == 50_000_000  # MW → W
    assert isinstance(gen.q, cim.ReactivePower)
    assert float(gen.q) == 10_000_000  # MVAr → VAr
    assert isinstance(gen.ratedS, cim.ApparentPower)
    assert float(gen.ratedS) == 75_000_000  # MVA → VA
    assert isinstance(gen.ratedU, cim.Voltage)
    assert float(gen.ratedU) == 13_800
    assert gen.ratedPowerFactor == 0.85

    assert len(gen.Terminals) == 1
    assert gen.Terminals[0].ConnectivityNode is n1


def test_q_limits(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    gen = new_synchronous_machine(
        net, sub, "G2", node=connectivity_nodes["node1"],
        min_q_MVAr=-20, max_q_MVAr=30,
    )
    assert isinstance(gen.minQ, cim.ReactivePower)
    assert float(gen.minQ) == -20_000_000
    assert isinstance(gen.maxQ, cim.ReactivePower)
    assert float(gen.maxQ) == 30_000_000


def test_added_to_graph(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    gen = new_synchronous_machine(net, sub, "G3", node=connectivity_nodes["node1"])
    assert gen in net.graph.get(cim.SynchronousMachine, {}).values()
