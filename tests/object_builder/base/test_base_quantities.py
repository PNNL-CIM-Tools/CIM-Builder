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


def test_base_power_add_connectivity(network, container):
    builder = BasePowerBuilder(network=network, container=container)
    base_power = builder.create(mRID="base_power_100")
    builder.add_connectivity(base_power, basePower=Qty(100, "MVA"))
    assert float(base_power.basePower.to("MVA")) == 100
