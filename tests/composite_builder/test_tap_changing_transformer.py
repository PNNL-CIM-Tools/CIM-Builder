"""Tests for cimbuilder.composite_builder.tap_changing_transformer."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.composite_builder.tap_changing_transformer import new_tap_changing_transformer


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_tap_changing_transformer(
        net, sub, "T1",
        connectivity_nodes["node1"], connectivity_nodes["node2"],
        rated_U1_kV=69.0, rated_U2_kV=12.47,
        rated_S_MVA=10.0,
    )

    assert isinstance(result["transformer"], cim.PowerTransformer)
    assert isinstance(result["end1"], cim.PowerTransformerEnd)
    assert isinstance(result["end2"], cim.PowerTransformerEnd)
    assert isinstance(result["tap_changer"], cim.RatioTapChanger)
    assert isinstance(result["control"], cim.TapChangerControl)


def test_two_ends_correct(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_tap_changing_transformer(
        net, sub, "T2",
        connectivity_nodes["node1"], connectivity_nodes["node2"],
        rated_U1_kV=115.0, rated_U2_kV=12.47,
    )

    xfmr = result["transformer"]
    assert len(xfmr.PowerTransformerEnd) == 2
    assert len(xfmr.Terminals) == 2
    assert result["end1"].endNumber == 1
    assert result["end2"].endNumber == 2


def test_tap_changer_linked_to_end1(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_tap_changing_transformer(
        net, sub, "T3",
        connectivity_nodes["node1"], connectivity_nodes["node2"],
    )

    rtc = result["tap_changer"]
    end1 = result["end1"]
    assert rtc.TransformerEnd is end1
    assert end1.RatioTapChanger is rtc


def test_control_wired(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_tap_changing_transformer(
        net, sub, "T4",
        connectivity_nodes["node1"], connectivity_nodes["node2"],
        target_value_kV=12.47,
    )

    rtc = result["tap_changer"]
    ctrl = result["control"]
    assert rtc.TapChangerControl is ctrl
    assert rtc in ctrl.TapChanger


def test_no_control(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_tap_changing_transformer(
        net, sub, "T5",
        connectivity_nodes["node1"], connectivity_nodes["node2"],
        add_control=False,
    )

    assert result["control"] is None
    assert result["tap_changer"].TapChangerControl is None


def test_template_no_op(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    fake = cim.PowerTransformerInfo(name="HVMV_69_12")
    result = new_tap_changing_transformer(
        net, sub, "T6",
        connectivity_nodes["node1"], connectivity_nodes["node2"],
        template=fake,
    )
    assert isinstance(result["transformer"], cim.PowerTransformer)
