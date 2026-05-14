"""Tests for cimbuilder.object_builder.measurement.new_analog."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.measurement.new_analog import create_all_analog, new_analog
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
    meas = new_analog(
        net, breaker, breaker.Terminals[0], cim.PhaseCode.ABC, "VA",
    )
    assert isinstance(meas, cim.Analog)
    assert meas.measurementType == "VA"
    assert meas.phases == cim.PhaseCode.ABC
    assert meas.Terminal is breaker.Terminals[0]
    assert meas.PowerSystemResource is breaker
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
    meas1 = new_analog(net, breaker, breaker.Terminals[0], cim.PhaseCode.ABC, "VA")
    meas2 = new_analog(net, breaker, breaker.Terminals[0], cim.PhaseCode.ABC, "VA")
    assert meas1 is meas2


def test_create_all_analog(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    breaker = new_breaker(
        net, sub, "BR3",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
    )
    measurements = create_all_analog(net, breaker, "VA")
    assert len(measurements) == 2
    assert all(isinstance(m, cim.Analog) for m in measurements)
