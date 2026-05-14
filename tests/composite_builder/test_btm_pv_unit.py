"""Tests for cimbuilder.composite_builder.btm_pv_unit."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.composite_builder.btm_pv_unit import new_btm_pv_unit


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_btm_pv_unit(
        net, sub, "BTM1", connectivity_nodes["node1"],
        p_kW=100.0, max_p_kW=150.0,
    )

    assert isinstance(result["pec"], cim.PowerElectronicsConnection)
    assert isinstance(result["pv_unit"], cim.PhotoVoltaicUnit)


def test_pv_linked_to_pec(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_btm_pv_unit(
        net, sub, "BTM2", connectivity_nodes["node1"],
        p_kW=50.0,
    )

    pec = result["pec"]
    pv = result["pv_unit"]
    assert pv.PowerElectronicsConnection is pec
    assert pv in pec.PowerElectronicsUnit


def test_with_measurements(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    result = new_btm_pv_unit(
        net, sub, "BTM3", connectivity_nodes["node1"],
        p_kW=75.0, add_measurements=True,
    )

    analogs = list(net.graph.get(cim.Analog, {}).values())
    pec = result["pec"]
    pec_analogs = [a for a in analogs if getattr(a, "PowerSystemResource", None) is pec]
    assert len(pec_analogs) >= 1
