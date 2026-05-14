"""Tests for cimbuilder.object_builder.inverter.new_photo_voltaic_unit."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.inverter.new_photo_voltaic_unit import new_photo_voltaic_unit
from cimbuilder.object_builder.inverter.new_power_electronics_connection import (
    new_power_electronics_connection,
)


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    pec = new_power_electronics_connection(
        net, sub, "PEC", node=connectivity_nodes["node1"],
    )
    pv = new_photo_voltaic_unit(net, pec, "PV1", min_p_kW=0, max_p_kW=100)

    assert isinstance(pv, cim.PhotoVoltaicUnit)
    assert pv.name == "PV1"
    assert pv.PowerElectronicsConnection is pec
    assert pv in pec.PowerElectronicsUnit
    assert isinstance(pv.minP, cim.ActivePower)
    assert float(pv.minP) == 0.0
    assert isinstance(pv.maxP, cim.ActivePower)
    assert float(pv.maxP) == 100_000
