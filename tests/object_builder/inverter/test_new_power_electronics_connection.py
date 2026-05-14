"""Tests for cimbuilder.object_builder.inverter.new_power_electronics_connection."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.inverter.new_power_electronics_connection import (
    new_power_electronics_connection,
)


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    n1 = connectivity_nodes["node1"]

    pec = new_power_electronics_connection(
        net, sub, "PEC1", node=n1,
        p_kW=100, q_kVAr=10, rated_S_kVA=125, rated_U_V=480,
    )
    assert isinstance(pec, cim.PowerElectronicsConnection)
    assert pec.name == "PEC1"
    assert isinstance(pec.p, cim.ActivePower)
    assert float(pec.p) == 100_000  # kW → W
    assert isinstance(pec.q, cim.ReactivePower)
    assert float(pec.q) == 10_000
    assert isinstance(pec.ratedS, cim.ApparentPower)
    assert float(pec.ratedS) == 125_000
    assert isinstance(pec.ratedU, cim.Voltage)
    assert float(pec.ratedU) == 480
    assert len(pec.Terminals) == 1
    assert pec.Terminals[0].ConnectivityNode is n1


def test_grid_forming_flag(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    pec = new_power_electronics_connection(
        net, sub, "PEC2", node=connectivity_nodes["node1"], is_grid_forming=True,
    )
    assert pec.isGridForming is True
