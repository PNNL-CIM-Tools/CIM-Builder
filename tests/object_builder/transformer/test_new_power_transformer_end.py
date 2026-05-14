"""Tests for cimbuilder.object_builder.transformer.new_power_transformer_end."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.transformer.new_power_transformer import new_power_transformer
from cimbuilder.object_builder.transformer.new_power_transformer_end import new_power_transformer_end


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    xfmr = new_power_transformer(net, sub, "T1")
    end = new_power_transformer_end(
        net, xfmr, "T1_end1", 1, connectivity_nodes["node1"],
        rated_S_MVA=10.0, rated_U_kV=69.0,
    )

    assert isinstance(end, cim.PowerTransformerEnd)
    assert end.name == "T1_end1"
    assert end.endNumber == 1
    assert end.PowerTransformer is xfmr
    assert end in xfmr.PowerTransformerEnd


def test_terminal_wired(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    xfmr = new_power_transformer(net, sub, "T2")
    end = new_power_transformer_end(
        net, xfmr, "T2_end1", 1, connectivity_nodes["node1"],
    )

    assert end.Terminal is not None
    assert end.Terminal.ConnectivityNode is connectivity_nodes["node1"]
    assert end.Terminal in xfmr.Terminals


def test_impedance_fields(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    xfmr = new_power_transformer(net, sub, "T3")
    end = new_power_transformer_end(
        net, xfmr, "T3_end1", 1, connectivity_nodes["node1"],
        r_ohm=1.5, x_ohm=10.0, b_S=1e-4, g_S=1e-5,
    )

    assert isinstance(end.r, cim.Resistance)
    assert float(end.r) == 1.5
    assert isinstance(end.x, cim.Reactance)
    assert float(end.x) == 10.0
    assert isinstance(end.b, cim.Susceptance)
    assert isinstance(end.g, cim.Conductance)


def test_two_ends(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    xfmr = new_power_transformer(net, sub, "T4")
    end1 = new_power_transformer_end(net, xfmr, "T4_end1", 1, connectivity_nodes["node1"], rated_U_kV=69.0)
    end2 = new_power_transformer_end(net, xfmr, "T4_end2", 2, connectivity_nodes["node2"], rated_U_kV=12.47)

    assert len(xfmr.PowerTransformerEnd) == 2
    assert len(xfmr.Terminals) == 2
    assert end1.endNumber == 1
    assert end2.endNumber == 2
