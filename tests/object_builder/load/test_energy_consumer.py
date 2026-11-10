import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.load import EnergyConsumerBuilder


def test_energy_consumer_add_connectivity(network, container, base_voltage):
    builder = EnergyConsumerBuilder(network=network, container=container)
    load = builder.create(mRID="load1", name="load1")

    load, terminal, phases = builder.add_connectivity(
        load,
        node="bus1",
        phases="ABC",
        grounded=True,
        customerCount=5,
        BaseVoltage=base_voltage.mRID,
    )
    assert terminal.ConductingEquipment is load
    assert len(phases) == 3


def test_energy_consumer_add_connectivity_phaseConnection_wrapped_in_enum(
    network, container, base_voltage
):
    builder = EnergyConsumerBuilder(network=network, container=container)
    load = builder.create(mRID="load1", name="load1")

    builder.add_connectivity(
        load, node="bus1", phaseConnection="Y", BaseVoltage=base_voltage.mRID
    )

    assert load.phaseConnection == network.cim.PhaseShuntConnectionKind("Y")


def test_energy_consumer_add_electrical(network, container):
    builder = EnergyConsumerBuilder(network=network, container=container)
    load = builder.create(mRID="load1", name="load1")

    builder.add_electrical(load, minP=Qty(0, "kW"), maxP=Qty(10, "kW"), pfixed=Qty(8, "kW"))
    assert float(load.pfixed.to("kW")) == 8


def test_energy_consumer_add_ssh(network, container):
    builder = EnergyConsumerBuilder(network=network, container=container)
    load = builder.create(mRID="load1", name="load1")

    builder.add_ssh(load, p=Qty(8, "kW"), q=Qty(2, "kVAr"), inService=True)
    assert load.inService is True


def test_energy_consumer_add_connectivity_twice_keeps_its_terminal(network, container, base_voltage):
    """C5: a second call reuses the existing Terminal instead of raising UnboundLocalError"""
    builder = EnergyConsumerBuilder(network=network, container=container)
    load = builder.create(mRID="ld_671")
    _, terminal, _ = builder.add_connectivity(load, node="671", BaseVoltage=base_voltage.mRID)
    _, again, _ = builder.add_connectivity(load, node="671", BaseVoltage=base_voltage.mRID)
    assert again is terminal
    assert load.Terminals == [terminal]
