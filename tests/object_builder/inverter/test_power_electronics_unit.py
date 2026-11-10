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


@pytest.mark.parametrize(
    "builder_cls",
    [PowerElectronicsUnitBuilder, PhotoVoltaicUnitBuilder, PowerElectronicsWindUnitBuilder],
)
def test_power_electronics_unit_add_electrical(network, container, builder_cls):
    pec = _make_connection(network, container)
    builder = builder_cls(network=network, container=container)
    unit = builder.create(mRID="pec1_unit")

    builder.add_electrical(
        unit, minP=Qty(0, "kW"), maxP=Qty(500, "kW"), PowerElectronicsConnection=pec.mRID
    )
    assert unit.PowerElectronicsConnection is pec
    assert unit in pec.PowerElectronicsUnit
    assert float(unit.maxP.to("kW")) == 500


def test_power_electronics_unit_add_ssh(network, container):
    builder = PowerElectronicsUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="unit1")

    builder.add_ssh(unit, p=Qty(-400, "kW"), inService=True)
    assert unit.inService is True


def test_charging_unit_cim_class_name_does_not_exist_in_profile(network, container):
    """ChargingUnitBuilder.cim_class_name = "ChargingUnit", but no such
    class exists anywhere in cimprofiles.cim18.cim18v17 (closest real
    classes: ElectricalVehicleUnit, PowerElectronicsUnit, BatteryUnit) -
    create() always fails before add_electrical is ever reached, since
    ObjectBuilder.create() looks the class up by this exact name."""
    builder = ChargingUnitBuilder(network=network, container=container)

    with pytest.raises(AttributeError, match="ChargingUnit"):
        builder.create(mRID="charger1")


def test_battery_unit_add_electrical(network, container):
    pec = _make_connection(network, container)
    builder = BatteryUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="pec1_unit")

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
    assert unit.PowerElectronicsConnection is pec
    assert float(unit.ratedE.to("kWh")) == 400


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
