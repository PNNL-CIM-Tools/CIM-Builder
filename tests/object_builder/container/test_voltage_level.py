import pytest

from cimbuilder.object_builder.container import (
    BayBuilder,
    SubstationBuilder,
    VoltageLevelBuilder,
)


def test_voltage_level_in_substation(network, container, base_voltage):
    substation = SubstationBuilder(network=network, container=container).create(mRID="sub_1")

    builder = VoltageLevelBuilder(network=network, container=container)
    voltage_level = builder.create(mRID="vl_1")
    builder.add_connectivity(voltage_level, Substation="sub_1", BaseVoltage=base_voltage.mRID)

    assert voltage_level.Substation is substation
    assert voltage_level in substation.VoltageLevels
    assert voltage_level.BaseVoltage is base_voltage


def test_voltage_level_unknown_substation(network, container, base_voltage):
    builder = VoltageLevelBuilder(network=network, container=container)
    voltage_level = builder.create(mRID="vl_1")
    with pytest.raises(ValueError, match="Substation"):
        builder.add_connectivity(
            voltage_level, Substation="sub_missing", BaseVoltage=base_voltage.mRID
        )


def test_bay_in_voltage_level(network, container, base_voltage):
    SubstationBuilder(network=network, container=container).create(mRID="sub_1")
    vl_builder = VoltageLevelBuilder(network=network, container=container)
    voltage_level = vl_builder.create(mRID="vl_1")
    vl_builder.add_connectivity(voltage_level, Substation="sub_1", BaseVoltage=base_voltage.mRID)

    builder = BayBuilder(network=network, container=container)
    bay = builder.create(mRID="bay_1")
    builder.add_connectivity(
        bay,
        VoltageLevel="vl_1",
        breakerConfiguration="breakerAndAHalf",
        busBarConfiguration="doubleBus",
    )

    assert bay.VoltageLevel is voltage_level
    assert bay in voltage_level.Bays
    assert bay.breakerConfiguration.value == "breakerAndAHalf"
    assert bay.busBarConfiguration.value == "doubleBus"
