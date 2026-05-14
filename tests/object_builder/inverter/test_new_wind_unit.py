"""Tests for cimbuilder.object_builder.inverter.new_wind_unit."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.inverter.new_power_electronics_connection import (
    new_power_electronics_connection,
)
from cimbuilder.object_builder.inverter.new_wind_unit import new_wind_unit


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    pec = new_power_electronics_connection(
        net, sub, "PEC", node=connectivity_nodes["node1"],
    )
    wind = new_wind_unit(net, pec, "W1", min_p_kW=0, max_p_kW=2500)

    assert isinstance(wind, cim.PowerElectronicsWindUnit)
    assert wind.name == "W1"
    assert wind.PowerElectronicsConnection is pec
    assert wind in pec.PowerElectronicsUnit
    assert float(wind.maxP) == 2_500_000
