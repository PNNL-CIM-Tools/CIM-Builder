import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.inverter import (
    BatteryUnitBuilder,
    ElectricalVehicleUnitBuilder,
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


def test_electrical_vehicle_unit(network, container):
    """replaces ChargingUnitBuilder, whose ChargingUnit class is not in cim18v17"""
    pec = _make_connection(network, container)
    builder = ElectricalVehicleUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="ev1")

    builder.add_electrical(
        unit,
        minP=Qty(-11, "kW"),
        maxP=Qty(11, "kW"),
        ratedE=Qty(75, "kWh"),
        chargingEfficiency=0.92,
        v2gCapable=True,
        PowerElectronicsConnection=pec.mRID,
    )
    assert type(unit).__name__ == "ElectricalVehicleUnit"
    assert unit.PowerElectronicsConnection is pec
    assert float(unit.ratedE.to("kWh")) == 75
    assert unit.v2gCapable is True


def test_electrical_vehicle_unit_has_no_ssh_part(network, container):
    builder = ElectricalVehicleUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="ev1")
    with pytest.raises(ValueError, match="ElectricalVehicleUnit"):
        builder.add_ssh(unit, p=Qty(-7, "kW"))


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


def test_battery_unit_add_ssh(network, container):
    """a BatteryUnit has no q in any profile part, its inverter carries the reactive power"""
    builder = BatteryUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="batt1")

    builder.add_ssh(
        unit, p=Qty(-50, "kW"), storedE=Qty(200, "kWh"), batteryState="discharging", inService=True
    )
    assert float(unit.p.to("kW")) == -50
    assert float(unit.storedE.to("kWh")) == 200
    assert unit.batteryState == network.cim.BatteryStateKind("discharging")
    with pytest.raises(TypeError, match="q"):
        builder.add_ssh(unit, q=Qty(-10, "kVAr"))
