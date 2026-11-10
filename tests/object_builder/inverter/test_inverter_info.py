from cimtables.units import Qty

from cimbuilder.object_builder.inverter import (
    BatteryInfoBuilder,
    GenerationInverterInfoBuilder,
    SolarPanelInfoBuilder,
    StorageInverterInfoBuilder,
)


def test_generation_inverter_info_add_asset_info(network, container):
    builder = GenerationInverterInfoBuilder(network=network, container=container)
    info = builder.create(mRID="inv_pv1", name="inv_pv1")

    builder.add_asset_info(
        info,
        phaseCount="threePhase",
        ratedCurrent=Qty(50, "A"),
        ratedVoltage=Qty(480, "V"),
        apparentPowerMaximum=Qty(50, "kVA"),
        ratedVoltageMax=Qty(528, "V"),
        ratedVoltageMin=Qty(432, "V"),
    )
    assert info.phaseCount.name == "threePhase"
    assert float(info.apparentPowerMaximum.to("kVA")) == 50


def test_storage_inverter_info_add_asset_info(network, container):
    builder = StorageInverterInfoBuilder(network=network, container=container)
    info = builder.create(mRID="inv_batt1", name="inv_batt1")

    builder.add_asset_info(
        info,
        phaseCount="singlePhase",
        apparentPowerMaximum=Qty(10, "kVA"),
        chargeRateActiveMax=Qty(5, "kW"),
        chargeRateReactiveMax=Qty(2, "kVAr"),
        storageCapacity=Qty(13.5, "kWh"),
    )
    assert info.phaseCount.name == "singlePhase"
    assert float(info.chargeRateActiveMax.to("kW")) == 5
    assert float(info.storageCapacity.to("kWh")) == 13.5


def test_battery_info_add_asset_info(network, container):
    builder = BatteryInfoBuilder(network=network, container=container)
    info = builder.create(mRID="batt_cat1", name="batt_cat1")

    builder.add_asset_info(info, ratedCapacity=Qty(13.5, "kWh"), usableCapacity=Qty(12, "kWh"))
    assert float(info.ratedCapacity.to("kWh")) == 13.5
    assert float(info.usableCapacity.to("kWh")) == 12


def test_solar_panel_info_add_asset_info(network, container):
    builder = SolarPanelInfoBuilder(network=network, container=container)
    info = builder.create(mRID="pv_panel1", name="pv_panel1")

    builder.add_asset_info(
        info, efficiency=18.5, referenceIrradiation=Qty(1, "kW/m^2"), referenceTemperature=Qty(25, "degC")
    )
    assert float(info.efficiency) == 18.5
