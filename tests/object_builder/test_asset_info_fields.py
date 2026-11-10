"""Every scalar attribute of each AssetInfo builder's class, set once with a real unit or enum string"""

import pytest
from cimtables.units import Qty

from cimbuilder import object_builder as OB


def test_overhead_wire_info_all_fields(network, container):
    builder = OB.OverheadWireInfoBuilder(network=network, container=container)
    wire = builder.create(mRID="wire_556500_26_7")
    builder.add_asset_info(
        wire,
        phaseCount="singlePhase",
        ratedCurrent=Qty(730, "A"),
        ratedFrequency=Qty(60, "Hz"),
        ratedVoltage=Qty(15, "kV"),
        purpose="phase",
        sizeDescription="556.5 kcmil 26/7",
        material="acsr",
        constructionKind="acsr",
        crossSection=Qty(282, "mm^2"),
        gmr=Qty(0.0313, "ft"),
        radius=Qty(0.927 / 2, "in"),
        coreRadius=Qty(0.1, "in"),
        strandCount=26,
        strandRadius=Qty(0.073, "in"),
        coreStrandCount=7,
        coreStrandRadius=Qty(0.057, "in"),
        rAC25=Qty(0.186, "ohm/mi"),
        rAC50=Qty(0.204, "ohm/mi"),
        rAC75=Qty(0.222, "ohm/mi"),
        rDC20=Qty(0.17, "ohm/mi"),
        insulated=False,
        insulationMaterial="other",
        insulationThickness=Qty(0, "in"),
        ratedStrength=Qty(22900, "lbf"),
    )
    assert wire.material.name == "acsr"
    assert wire.constructionKind.name == "acsr"
    assert float(wire.rAC75.to("ohm/mi")) == pytest.approx(0.222)
    assert wire.strandCount == 26
    assert float(wire.ratedFrequency.to("Hz")) == 60


def test_concentric_neutral_cable_info_all_fields(network, container):
    builder = OB.ConcentricNeutralCableInfoBuilder(network=network, container=container)
    cable = builder.create(mRID="cable_250_1_3")
    builder.add_asset_info(
        cable,
        phaseCount="singlePhase",
        ratedVoltage=Qty(15, "kV"),
        material="aluminum",
        constructionKind="compacted",
        insulationMaterial="crosslinkedPolyethylene",
        gmr=Qty(0.0171, "ft"),
        diameterOverCore=Qty(0.567, "in"),
        diameterOverInsulation=Qty(1.06, "in"),
        diameterOverScreen=Qty(1.1, "in"),
        diameterOverJacket=Qty(1.29, "in"),
        isStrandFill=True,
        sheathAsNeutral=False,
        nominalTemperature=Qty(90, "degC"),
        outerJacketKind="linearLowDensityPolyethylene",
        shieldMaterial="copper",
        diameterOverNeutral=Qty(1.2, "in"),
        neutralStrandCount=13,
        neutralStrandRadius=Qty(0.0641 / 2, "in"),
        neutralStrandGmr=Qty(0.00208, "ft"),
        neutralStrandRDC20=Qty(14.87, "ohm/mi"),
    )
    assert cable.constructionKind.name == "compacted"
    assert cable.outerJacketKind.name == "linearLowDensityPolyethylene"
    assert cable.shieldMaterial.name == "copper"
    assert cable.insulationMaterial.name == "crosslinkedPolyethylene"
    assert float(cable.diameterOverNeutral.to("in")) == pytest.approx(1.2)
    assert cable.neutralStrandCount == 13


def test_wire_info_unknown_kwarg_fails_fast(network, container):
    builder = OB.OverheadWireInfoBuilder(network=network, container=container)
    wire = builder.create(mRID="wire_x")
    with pytest.raises(TypeError, match="no_such_field"):
        builder.add_asset_info(wire, no_such_field=1)


def test_storage_inverter_info_all_fields(network, container):
    builder = OB.StorageInverterInfoBuilder(network=network, container=container)
    info = builder.create(mRID="inv_batt1")
    builder.add_asset_info(
        info,
        phaseCount="threePhase",
        ratedCurrent=Qty(60, "A"),
        ratedFrequency=Qty(60, "Hz"),
        ratedVoltage=Qty(480, "V"),
        apparentPowerMaximum=Qty(50, "kVA"),
        ratedVoltageMax=Qty(528, "V"),
        ratedVoltageMin=Qty(432, "V"),
        chargeRateActiveMax=Qty(50, "kW"),
        chargeRateReactiveMax=Qty(20, "kVAr"),
        storageCapacity=Qty(200, "kWh"),
    )
    assert float(info.ratedFrequency.to("Hz")) == 60
    assert float(info.ratedVoltageMin.to("V")) == 432


def test_battery_info_all_fields(network, container):
    builder = OB.BatteryInfoBuilder(network=network, container=container)
    info = builder.create(mRID="batt_cat1")
    builder.add_asset_info(
        info,
        batteryType="lithiumIronPhosphate",
        cellChemistry="LFP",
        numberOfCells=192,
        ratedCapacity=Qty(13.5, "kWh"),
        usableCapacity=Qty(12, "kWh"),
    )
    assert info.batteryType.name == "lithiumIronPhosphate"
    assert info.cellChemistry == "LFP"
    assert info.numberOfCells == 192


def test_solar_panel_info_all_fields(network, container):
    builder = OB.SolarPanelInfoBuilder(network=network, container=container)
    info = builder.create(mRID="pv_panel1")
    builder.add_asset_info(
        info,
        efficiency=20.1,
        openCircuitVoltage=Qty(49.5, "V"),
        shortCircuitCurrent=Qty(10.2, "A"),
        referenceIrradiation=Qty(1000, "W/m^2"),
        referenceTemperature=Qty(25, "degC"),
    )
    assert float(info.openCircuitVoltage.to("V")) == pytest.approx(49.5)
    assert float(info.shortCircuitCurrent.to("A")) == pytest.approx(10.2)


def test_series_reactor_info_all_fields(network, container):
    builder = OB.SeriesReactorInfoBuilder(network=network, container=container)
    info = builder.create(mRID="reac_cat1")
    builder.add_asset_info(
        info,
        phaseCount="threePhase",
        ratedCurrent=Qty(600, "A"),
        ratedFrequency=Qty(60, "Hz"),
        ratedVoltage=Qty(13.8, "kV"),
        ratedInductance=0.0013,
        ratedReactivePower=Qty(1, "MVAr"),
        maxPowerLoss=Qty(5, "kVA"),
        ratedImpulseWithstandVoltage=Qty(110, "kV"),
        ratedMechanicalCurrent=25000.0,
        ratedThermalCurrent=10000.0,
        coreType="air",
        insulationMedium="oil",
        circulationAndCoolingType="oilNaturalAirNatural",
        temperatureClass="F",
        temperatureRise=65.0,
        oilType="mineral",
        oilPreservationType="conservator",
        volumeOfOil=1.5,
        oilWeight=1300.0,
        coreCoilsWeight=2000.0,
        tankAndFittingsWeight=900.0,
    )
    assert info.coreType.name == "air"
    assert info.insulationMedium.name == "oil"
    assert info.circulationAndCoolingType.name == "oilNaturalAirNatural"
    assert info.oilPreservationType.name == "conservator"
    assert float(info.ratedReactivePower.to("MVAr")) == 1
    assert info.tankAndFittingsWeight == 900.0


def test_switch_info_all_fields(network, container):
    builder = OB.SwitchInfoBuilder(network=network, container=container)
    info = builder.create(mRID="sw_info_cat1")
    builder.add_asset_info(
        info,
        phaseCount="threePhase",
        ratedCurrent=Qty(1200, "A"),
        ratedFrequency=Qty(60, "Hz"),
        ratedVoltage=Qty(15.5, "kV"),
        breakingCapacity=Qty(25, "kA"),
        ratedInterruptingTime=Qty(50, "ms"),
        ratedImpulseWithstandVoltage=Qty(110, "kV"),
        isSinglePhase=False,
        isUnganged=False,
        lowPressureAlarm=Qty(70, "psi"),
        lowPressureLockOut=Qty(60, "psi"),
        oilVolumePerTank=Qty(30, "gallon"),
    )
    assert float(info.ratedInterruptingTime.to("s")) == pytest.approx(0.05)
    assert float(info.lowPressureAlarm.to("psi")) == pytest.approx(70)
    assert float(info.oilVolumePerTank.to("gallon")) == pytest.approx(30)
    assert info.isUnganged is False


def test_tap_changer_info_all_fields(network, container):
    builder = OB.TapChangerInfoBuilder(network=network, container=container)
    info = builder.create(mRID="tci_reg1")
    builder.add_asset_info(
        info,
        phaseCount="singlePhase",
        ratedCurrent=Qty(219, "A"),
        ratedFrequency=Qty(60, "Hz"),
        ratedVoltage=Qty(7.62, "kV"),
        ratedApparentPower=Qty(167, "kVA"),
        neutralU=Qty(7.62, "kV"),
        bil=Qty(95, "kV"),
        frequency=Qty(60, "Hz"),
        ctRating=Qty(250, "A"),
        ctRatio=1250.0,
        ptRatio=63.5,
        isTcul=True,
        highStep=16,
        lowStep=-16,
        neutralStep=0,
        stepVoltageIncrement=0.625,
        stepPhaseIncrement=Qty(0, "deg"),
        stepReactiveIncrement=0.0,
    )
    assert info.isTcul is True
    assert float(info.bil.to("kV")) == 95
    assert float(info.ratedFrequency.to("Hz")) == 60
    assert float(info.stepReactiveIncrement) == 0.0
