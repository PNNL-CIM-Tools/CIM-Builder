"""Tests for cimbuilder.composite_builder.battery_unit."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.composite_builder.battery_unit import new_battery_unit


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_battery_unit(
        net, sub, "BESS1", connectivity_nodes["node1"],
        p_kW=500.0, rated_S_kVA=500.0,
        rated_E_kWh=2000.0, stored_E_kWh=1000.0,
    )

    assert isinstance(result["pec"], cim.PowerElectronicsConnection)
    assert isinstance(result["battery"], cim.BatteryUnit)


def test_battery_linked_to_pec(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_battery_unit(
        net, sub, "BESS2", connectivity_nodes["node1"],
        rated_E_kWh=1000.0,
    )

    pec = result["pec"]
    batt = result["battery"]
    assert batt.PowerElectronicsConnection is pec
    assert batt in pec.PowerElectronicsUnit


def test_with_measurements(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_battery_unit(
        net, sub, "BESS3", connectivity_nodes["node1"],
        rated_E_kWh=500.0, add_measurements=True,
    )

    analogs = list(net.graph.get(cim.Analog, {}).values())
    pec = result["pec"]
    pec_analogs = [a for a in analogs if getattr(a, "PowerSystemResource", None) is pec]
    meas_types = {getattr(a, "measurementType", None) for a in pec_analogs}
    assert "VA" in meas_types
    assert "SoC" in meas_types
