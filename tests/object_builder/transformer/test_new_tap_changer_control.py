"""Tests for cimbuilder.object_builder.transformer.new_tap_changer_control."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.transformer.new_tap_changer_control import new_tap_changer_control


def test_basic(simple_substation_network):
    cim = get_cim()
    net = simple_substation_network["network"]

    tcc = new_tap_changer_control(net, "TCC1")
    assert isinstance(tcc, cim.TapChangerControl)
    assert tcc.name == "TCC1"


def test_optional_fields(simple_substation_network):
    cim = get_cim()
    net = simple_substation_network["network"]

    tcc = new_tap_changer_control(
        net, "TCC2",
        target_value_kV=69.0,
        target_deadband_kV=0.5,
        enabled=True,
        discrete=True,
    )

    assert isinstance(tcc.targetValue, cim.Voltage)
    assert isinstance(tcc.targetDeadband, cim.Voltage)
    assert tcc.enabled is True
    assert tcc.discrete is True


def test_added_to_graph(simple_substation_network):
    cim = get_cim()
    net = simple_substation_network["network"]

    tcc = new_tap_changer_control(net, "TCC3")
    assert tcc in net.graph.get(cim.TapChangerControl, {}).values()
