"""Tests for cimbuilder.object_builder.transformer.new_ratio_tap_changer."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.transformer.new_power_transformer import new_power_transformer
from cimbuilder.object_builder.transformer.new_power_transformer_end import new_power_transformer_end
from cimbuilder.object_builder.transformer.new_ratio_tap_changer import new_ratio_tap_changer


def _make_end(net, sub, nodes, suffix=""):
    cim = get_cim()
    xfmr = new_power_transformer(net, sub, f"T{suffix}")
    end = new_power_transformer_end(net, xfmr, f"T{suffix}_end1", 1, nodes["node1"])
    return end


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    end = _make_end(net, sub, connectivity_nodes, "1")
    rtc = new_ratio_tap_changer(
        net, end, "RTC1",
        high_step=16, low_step=-16, neutral_step=0, normal_step=0,
    )

    assert isinstance(rtc, cim.RatioTapChanger)
    assert rtc.name == "RTC1"
    assert rtc.highStep == 16
    assert rtc.lowStep == -16
    assert rtc.neutralStep == 0
    assert rtc.normalStep == 0
    assert rtc.step == 0.0  # defaults to normal_step


def test_bidirectional_link(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    end = _make_end(net, sub, connectivity_nodes, "2")
    rtc = new_ratio_tap_changer(
        net, end, "RTC2",
        high_step=8, low_step=-8, neutral_step=0, normal_step=0,
    )

    assert rtc.TransformerEnd is end
    assert end.RatioTapChanger is rtc


def test_optional_fields(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    end = _make_end(net, sub, connectivity_nodes, "3")
    rtc = new_ratio_tap_changer(
        net, end, "RTC3",
        high_step=16, low_step=-16, neutral_step=0, normal_step=2,
        step=4.0,
        step_voltage_increment_pct=0.625,
        neutral_U_kV=69.0,
        initial_delay_s=30.0,
        subsequent_delay_s=5.0,
        ltc_flag=True,
    )

    assert rtc.step == 4.0
    assert isinstance(rtc.stepVoltageIncrement, cim.PerCent)
    assert isinstance(rtc.neutralU, cim.Voltage)
    assert isinstance(rtc.initialDelay, cim.Seconds)
    assert isinstance(rtc.subsequentDelay, cim.Seconds)
    assert rtc.ltcFlag is True


def test_control_wiring(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    from cimbuilder.object_builder.transformer.new_tap_changer_control import new_tap_changer_control
    tcc = new_tap_changer_control(net, "TCC1", target_value_kV=69.0)

    end = _make_end(net, sub, connectivity_nodes, "4")
    rtc = new_ratio_tap_changer(
        net, end, "RTC4",
        high_step=16, low_step=-16, neutral_step=0, normal_step=0,
        control=tcc,
    )

    assert rtc.TapChangerControl is tcc
    assert rtc in tcc.TapChanger


def test_added_to_graph(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    end = _make_end(net, sub, connectivity_nodes, "5")
    rtc = new_ratio_tap_changer(
        net, end, "RTC5",
        high_step=16, low_step=-16, neutral_step=0, normal_step=0,
    )
    assert rtc in net.graph.get(cim.RatioTapChanger, {}).values()
