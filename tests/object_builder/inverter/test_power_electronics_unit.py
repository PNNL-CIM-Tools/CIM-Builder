import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.inverter import (
    BatteryUnitBuilder,
    ChargingUnitBuilder,
    PhotoVoltaicUnitBuilder,
    PowerElectronicsConnectionBuilder,
    PowerElectronicsUnitBuilder,
    PowerElectronicsWindUnitBuilder,
)


def _make_connection(network, container):
    pec_builder = PowerElectronicsConnectionBuilder(network=network, container=container)
    return pec_builder.create(mRID="pec1", name="pec1")


def test_power_electronics_unit_add_electrical_target_class_is_a_module_not_a_class(
    network, container
):
    """add_electrical calls
    graph_write.set_assc_from_mrid(..., target_class=el_bal, ...) where
    `el_bal` is the electrical_balanced MODULE itself (self.cim), not
    el_bal.PowerElectronicsConnection. resolve()'s isinstance(obj, cim_cls)
    check then raises TypeError (a module isn't a valid 2nd isinstance arg)
    for every call, regardless of what PowerElectronicsConnection mRID is
    passed. This affects every PowerElectronicsUnitBuilder subclass that
    doesn't override add_electrical (PhotoVoltaicUnit/Wind/Charging) and
    BatteryUnitBuilder too, since its override calls super().add_electrical."""
    pec = _make_connection(network, container)
    builder = PowerElectronicsUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="unit1")

    with pytest.raises(TypeError):
        builder.add_electrical(
            unit, minP=Qty(0, "kW"), maxP=Qty(500, "kW"), PowerElectronicsConnection=pec.mRID
        )


def test_power_electronics_unit_add_ssh(network, container):
    builder = PowerElectronicsUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="unit1")

    builder.add_ssh(unit, p=Qty(-400, "kW"), inService=True)
    assert unit.inService is True


def test_photovoltaic_unit_add_electrical_inherits_target_class_bug(network, container):
    pec = _make_connection(network, container)
    builder = PhotoVoltaicUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="pv1")

    with pytest.raises(TypeError):
        builder.add_electrical(
            unit, minP=Qty(0, "kW"), maxP=Qty(250, "kW"), PowerElectronicsConnection=pec.mRID
        )


def test_wind_unit_add_electrical_inherits_target_class_bug(network, container):
    pec = _make_connection(network, container)
    builder = PowerElectronicsWindUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="wind1")

    with pytest.raises(TypeError):
        builder.add_electrical(
            unit, minP=Qty(0, "kW"), maxP=Qty(1, "MW"), PowerElectronicsConnection=pec.mRID
        )


def test_charging_unit_cim_class_name_does_not_exist_in_profile(network, container):
    """ChargingUnitBuilder.cim_class_name = "ChargingUnit", but no such
    class exists anywhere in cimprofiles.cim18.cim18v17 (closest real
    classes: ElectricalVehicleUnit, PowerElectronicsUnit, BatteryUnit) -
    create() always fails before add_electrical is ever reached, since
    ObjectBuilder.create() looks the class up by this exact name."""
    builder = ChargingUnitBuilder(network=network, container=container)

    with pytest.raises(AttributeError, match="ChargingUnit"):
        builder.create(mRID="charger1")


def test_battery_unit_add_electrical_inherits_target_class_bug_via_super(network, container):
    """BatteryUnitBuilder.add_electrical calls super().add_electrical(...)
    first, which hits the same target_class=module TypeError before
    BatteryUnit's own ratedE/minimumE/idlingP/chargingEfficiency/
    dischargingEfficiency fields (all real on EL_BAL.BatteryUnit) are ever
    written."""
    pec = _make_connection(network, container)
    builder = BatteryUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="batt1")

    with pytest.raises(TypeError):
        builder.add_electrical(
            unit,
            minP=Qty(-100, "kW"),
            maxP=Qty(100, "kW"),
            ratedE=Qty(400, "kWh"),
            minimumE=Qty(40, "kWh"),
            idlingP=Qty(1, "kW"),
            chargingEfficiency=0.95,
            dischargingEfficiency=0.95,
            PowerElectronicsConnection=pec.mRID,
        )


def test_battery_unit_add_ssh_q_kwarg_not_accepted_by_parent(network, container):
    """BatteryUnitBuilder.add_ssh calls
    super().add_ssh(unit, p=p, q=q, inService=inService), but
    PowerElectronicsUnitBuilder.add_ssh's signature only accepts
    p/inService - it has no `q` parameter at all. This raises TypeError
    (unexpected keyword argument) for every call, independent of whatever
    value q holds."""
    builder = BatteryUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="batt1")

    with pytest.raises(TypeError, match="q"):
        builder.add_ssh(unit, p=Qty(-50, "kW"), q=Qty(-10, "kVAr"), inService=True)
