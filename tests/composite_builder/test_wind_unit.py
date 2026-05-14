"""Tests for cimbuilder.composite_builder.wind_unit."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.composite_builder.wind_unit import new_wind_unit


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_wind_unit(
        net, sub, "WIND1", connectivity_nodes["node1"],
        p_kW=200.0, max_p_kW=250.0,
    )

    assert isinstance(result["pec"], cim.PowerElectronicsConnection)
    assert isinstance(result["wind_unit"], cim.PowerElectronicsWindUnit)


def test_wind_linked_to_pec(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_wind_unit(
        net, sub, "WIND2", connectivity_nodes["node1"],
        p_kW=100.0,
    )

    pec = result["pec"]
    wind = result["wind_unit"]
    assert wind.PowerElectronicsConnection is pec
    assert wind in pec.PowerElectronicsUnit
