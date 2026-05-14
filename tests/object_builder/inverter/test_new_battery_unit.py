"""Tests for cimbuilder.object_builder.inverter.new_battery_unit."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.inverter.new_battery_unit import new_battery_unit
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
    bess = new_battery_unit(
        net, pec, "B1",
        min_p_kW=-50, max_p_kW=50,
        rated_E_kWh=200, stored_E_kWh=100, minimum_E_kWh=20,
        charging_efficiency_pct=95, discharging_efficiency_pct=93,
    )

    assert isinstance(bess, cim.BatteryUnit)
    assert bess.name == "B1"
    assert bess.PowerElectronicsConnection is pec
    assert bess in pec.PowerElectronicsUnit

    assert isinstance(bess.minP, cim.ActivePower)
    assert float(bess.minP) == -50_000
    assert isinstance(bess.maxP, cim.ActivePower)
    assert float(bess.maxP) == 50_000
    assert isinstance(bess.ratedE, cim.RealEnergy)
    assert isinstance(bess.storedE, cim.RealEnergy)
    assert isinstance(bess.minimumE, cim.RealEnergy)
    assert isinstance(bess.chargingEfficiency, cim.PerCent)
    assert isinstance(bess.dischargingEfficiency, cim.PerCent)
