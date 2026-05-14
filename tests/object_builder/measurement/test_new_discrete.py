"""Tests for cimbuilder.object_builder.measurement.new_discrete."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.measurement.new_discrete import new_discrete
from cimbuilder.object_builder.switch.new_breaker import new_breaker


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    breaker = new_breaker(
        net, sub, "BR1",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
    )
    meas = new_discrete(net, breaker, breaker.Terminals[0], cim.PhaseCode.ABC, "Pos")
    assert isinstance(meas, cim.Discrete)
    assert meas.measurementType == "Pos"
    assert meas in breaker.Measurements


def test_duplicate_returns_existing(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    breaker = new_breaker(
        net, sub, "BR2",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
    )
    m1 = new_discrete(net, breaker, breaker.Terminals[0], cim.PhaseCode.ABC, "Pos")
    m2 = new_discrete(net, breaker, breaker.Terminals[0], cim.PhaseCode.ABC, "Pos")
    assert m1 is m2
