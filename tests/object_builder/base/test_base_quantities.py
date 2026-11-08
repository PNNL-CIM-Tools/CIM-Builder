from cimtables.units import Qty

from cimbuilder.object_builder.base import (
    BaseFrequencyBuilder,
    BasePowerBuilder,
    BaseVoltageBuilder,
)


def test_base_voltage_create(network, container):
    builder = BaseVoltageBuilder(network=network, container=container)
    bv = builder.create(mRID="bv_115kV", nominalVoltage=Qty(115, "kV"))
    assert float(bv.nominalVoltage.to("kV")) == 115


def test_base_frequency_create(network, container):
    builder = BaseFrequencyBuilder(network=network, container=container)
    freq = builder.create(mRID="freq_60", frequency=60)
    assert float(freq.frequency.to("Hz")) == 60


def test_base_power_create_sets_network_base_power(network, container):
    builder = BasePowerBuilder(network=network, container=container)
    base_power = builder.create(mRID="base_power_10", basePower=Qty(10, "MVA"))
    assert float(base_power.basePower.to("MVA")) == 10
    assert float(network.base_power.to("MVA")) == 10
