from cimtables.units import Qty

from cimbuilder.object_builder.load import (
    EnergyConsumerBuilder,
    LoadResponseCharacteristicBuilder,
)


def test_zip_load(network, container, base_voltage):
    builder = LoadResponseCharacteristicBuilder(network=network, container=container)
    response = builder.create(mRID="zip_constant_z")
    builder.add_electrical(
        response,
        exponentModel=False,
        pConstantImpedance=1.0,
        pConstantCurrent=0.0,
        pConstantPower=0.0,
        qConstantImpedance=1.0,
        qConstantCurrent=0.0,
        qConstantPower=0.0,
    )
    load_builder = EnergyConsumerBuilder(network=network, container=container)
    load = load_builder.create(mRID="ld_611")
    load_builder.add_electrical(load, LoadResponse=response.mRID)

    assert response.exponentModel is False
    assert response.pConstantImpedance == 1.0
    assert load.LoadResponse is response
    assert load in response.EnergyConsumer
