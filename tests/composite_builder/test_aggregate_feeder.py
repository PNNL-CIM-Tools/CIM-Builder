"""Tests for cimbuilder.composite_builder.aggregate_feeder."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.composite_builder.aggregate_feeder import new_aggregate_feeder


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    bv = simple_substation_network["base_voltage"]

    feeder, load, breaker = new_aggregate_feeder(
        net, "Feeder1", "BRK_F1", sub,
        connectivity_nodes["node1"], bv,
        total_load_kw=1000.0, total_load_kvar=200.0,
        total_btm_pv_kw=100.0,
    )

    assert isinstance(feeder, cim.Feeder)
    assert isinstance(load, cim.EnergyConsumer)
    assert isinstance(breaker, cim.Breaker)


def test_feeder_linked_to_substation(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    bv = simple_substation_network["base_voltage"]

    feeder, _, _ = new_aggregate_feeder(
        net, "Feeder2", "BRK_F2", sub,
        connectivity_nodes["node1"], bv,
    )

    assert feeder.NormalEnergizingSubstation is sub


def test_normal_head_terminal(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    bv = simple_substation_network["base_voltage"]

    feeder, _, breaker = new_aggregate_feeder(
        net, "Feeder3", "BRK_F3", sub,
        connectivity_nodes["node1"], bv,
    )

    assert feeder.NormalHeadTerminal is breaker.Terminals[1]


def test_load_units(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    bv = simple_substation_network["base_voltage"]

    _, load, _ = new_aggregate_feeder(
        net, "Feeder4", "BRK_F4", sub,
        connectivity_nodes["node1"], bv,
        total_load_kw=5000.0, total_load_kvar=1000.0,
    )

    assert isinstance(load.p, cim.ActivePower)
    assert abs(load.p.to("kW") - 5000.0) < 1e-6
    assert isinstance(load.q, cim.ReactivePower)
    assert abs(load.q.to("kVAr") - 1000.0) < 1e-6


def test_der_objects_created(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    bv = simple_substation_network["base_voltage"]

    new_aggregate_feeder(
        net, "Feeder5", "BRK_F5", sub,
        connectivity_nodes["node1"], bv,
        total_btm_pv_kw=200.0,
        total_ftm_pv_kw=500.0,
    )

    pecs = list(net.graph.get(cim.PowerElectronicsConnection, {}).values())
    pv_units = list(net.graph.get(cim.PhotoVoltaicUnit, {}).values())

    # BTM PEC + FTM PEC = 2
    feeder_pecs = [p for p in pecs if p.name and "aggr" in p.name]
    assert len(feeder_pecs) == 2
    assert len(pv_units) >= 2


def test_wind_objects_created(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    bv = simple_substation_network["base_voltage"]

    new_aggregate_feeder(
        net, "Feeder6", "BRK_F6", sub,
        connectivity_nodes["node1"], bv,
        total_btm_wind_kw=50.0,
        total_ftm_wind_kw=100.0,
    )

    wind_units = list(net.graph.get(cim.PowerElectronicsWindUnit, {}).values())
    assert len(wind_units) >= 2


def test_distributed_flag(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    bv = simple_substation_network["base_voltage"]

    feeder, _, _ = new_aggregate_feeder(
        net, "Feeder7", "BRK_F7", sub,
        connectivity_nodes["node1"], bv,
        distributed=True,
    )

    assert feeder.SubSchedulingArea is not None
    assert isinstance(feeder.SubSchedulingArea, cim.ConnectivityArea)


def test_deprecation_shim(simple_substation_network, connectivity_nodes):
    """Old feeder_builder import path emits DeprecationWarning but still works."""
    import warnings
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    bv = simple_substation_network["base_voltage"]

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        from cimbuilder.feeder_builder.aggregate_feeder import new_aggregate_feeder as old_fn
        old_fn(
            net, "Feeder8", "BRK_F8", sub,
            connectivity_nodes["node1"], bv,
        )
    assert any(issubclass(warning.category, DeprecationWarning) for warning in w)
