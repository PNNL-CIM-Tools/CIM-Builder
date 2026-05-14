"""Tests for cimbuilder.composite_builder.feeder_head_breaker."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.composite_builder.feeder_head_breaker import new_feeder_head_breaker


def _make_feeder(net, sub):
    cim = get_cim()
    feeder = cim.Feeder(name="F1")
    feeder.uuid(name="F1")
    feeder.NormalEnergizingSubstation = sub
    net.add_to_graph(feeder)
    return feeder


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    feeder = _make_feeder(net, sub)
    result = new_feeder_head_breaker(
        net, feeder, "BRK1", connectivity_nodes["node1"],
        distributed=False, add_measurements=False,
    )

    assert isinstance(result["breaker"], cim.Breaker)
    assert isinstance(result["feeder_node"], cim.ConnectivityNode)
    assert result["feeder_area"] is None


def test_normal_head_terminal_set(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    feeder = _make_feeder(net, sub)
    result = new_feeder_head_breaker(
        net, feeder, "BRK2", connectivity_nodes["node1"],
        distributed=False, add_measurements=False,
    )

    breaker = result["breaker"]
    assert feeder.NormalHeadTerminal is breaker.Terminals[1]


def test_distributed_creates_feeder_area(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    feeder = _make_feeder(net, sub)
    result = new_feeder_head_breaker(
        net, feeder, "BRK3", connectivity_nodes["node1"],
        distributed=True, add_measurements=False,
    )

    assert result["feeder_area"] is not None
    assert isinstance(result["feeder_area"], cim.ConnectivityArea)
    assert feeder.SubSchedulingArea is result["feeder_area"]


def test_measurements_created(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    feeder = _make_feeder(net, sub)
    result = new_feeder_head_breaker(
        net, feeder, "BRK4", connectivity_nodes["node1"],
        distributed=False, add_measurements=True,
    )

    analogs = list(net.graph.get(cim.Analog, {}).values())
    discretes = list(net.graph.get(cim.Discrete, {}).values())
    breaker = result["breaker"]
    brk_analogs = [a for a in analogs if getattr(a, "PowerSystemResource", None) is breaker]
    brk_discretes = [d for d in discretes if getattr(d, "PowerSystemResource", None) is breaker]

    assert len(brk_analogs) == 3   # NetLoad, ExcessGen, TotalGen
    assert len(brk_discretes) == 1  # Pos
