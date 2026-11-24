import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.generator import (
    AsynchronousMachineBuilder,
    SynchronousMachineBuilder,
)


def test_synchronous_machine_connectivity(network, container, base_voltage):
    builder = SynchronousMachineBuilder(network=network, container=container)
    machine = builder.create(mRID="gen1", name="gen1")
    machine, terminal = builder.add_connectivity(
        machine, node="gen1_bus", BaseVoltage=base_voltage.mRID
    )
    assert terminal.ConductingEquipment is machine


def test_synchronous_machine_add_electrical(network, container, base_voltage):
    """rating and limits only: the profile has no baseQ, which add_electrical used to write"""
    builder = SynchronousMachineBuilder(network=network, container=container)
    machine = builder.create(mRID="gen1", name="gen1")
    builder.add_connectivity(machine, node="gen1_bus", BaseVoltage=base_voltage.mRID)

    builder.add_electrical(
        machine,
        ratedS=Qty(2, "MVA"),
        minQ=Qty(-1, "MVAr"),
        maxQ=Qty(1.2, "MVAr"),
        minU=Qty(11.8, "kV"),
        maxU=Qty(13.1, "kV"),
    )
    assert float(machine.ratedS.to("MVA")) == 2
    assert float(machine.minQ.to("MVAr")) == -1
    assert float(machine.maxU.to("kV")) == pytest.approx(13.1)


def test_synchronous_machine_add_ssh(network, container, base_voltage):
    builder = SynchronousMachineBuilder(network=network, container=container)
    machine = builder.create(mRID="gen1", name="gen1")
    builder.add_connectivity(machine, node="gen1_bus", BaseVoltage=base_voltage.mRID)

    builder.add_ssh(machine, p=Qty(-1, "MW"), q=Qty(-0.2, "MVAr"), inService=True)
    assert machine.inService is True


def test_synchronous_machine_add_short_circuit(network, container, base_voltage):
    """SC.SynchronousMachine now has real ratedU/ratedPowerFactor fields
    (the cimprofiles sibling repo added them), so add_short_circuit's
    profile_part=SC calls are valid again - this used to raise, see git
    history of this test if it starts raising again."""
    builder = SynchronousMachineBuilder(network=network, container=container)
    machine = builder.create(mRID="gen1", name="gen1")
    builder.add_connectivity(machine, node="gen1_bus", BaseVoltage=base_voltage.mRID)

    builder.add_short_circuit(
        machine,
        ratedU=Qty(12, "kV"),
        ratedPowerFactor=0.9,
        r=0.01,
        r0=0.02,
        r2=0.02,
        x0=0.05,
        x2=0.05,
        earthing=True,
        earthingStarPointR=1.0,
        earthingStarPointX=1.0,
    )
    assert machine.earthing is True
    assert float(machine.ratedU.to("kV")) == 12


def test_asynchronous_machine_connectivity(network, container, base_voltage):
    builder = AsynchronousMachineBuilder(network=network, container=container)
    machine = builder.create(mRID="gen2", name="gen2")
    machine, terminal = builder.add_connectivity(
        machine, node="gen2_bus", BaseVoltage=base_voltage.mRID
    )
    assert terminal.ConductingEquipment is machine


def test_asynchronous_machine_add_electrical(network, container, base_voltage):
    builder = AsynchronousMachineBuilder(network=network, container=container)
    machine = builder.create(mRID="gen2", name="gen2")
    builder.add_connectivity(machine, node="gen2_bus", BaseVoltage=base_voltage.mRID)

    builder.add_electrical(
        machine, ratedS=Qty(500, "kVA"), efficiency=96.5, asynchronousMachineType="generator"
    )
    assert float(machine.ratedS.to("kVA")) == 500
    assert float(machine.efficiency) == 96.5
    assert machine.asynchronousMachineType == network.cim.AsynchronousMachineKind("generator")


def test_asynchronous_machine_add_ssh(network, container, base_voltage):
    builder = AsynchronousMachineBuilder(network=network, container=container)
    machine = builder.create(mRID="gen2", name="gen2")
    builder.add_connectivity(machine, node="gen2_bus", BaseVoltage=base_voltage.mRID)

    builder.add_ssh(machine, p=Qty(-0.4, "MW"), q=Qty(-0.1, "MVAr"), inService=True)
    assert machine.inService is True


def test_asynchronous_machine_add_short_circuit(network, container, base_voltage):
    """SC.AsynchronousMachine now has real ratedU/ratedPowerFactor fields
    (the cimprofiles sibling repo added them), same as the synchronous
    machine case above."""
    builder = AsynchronousMachineBuilder(network=network, container=container)
    machine = builder.create(mRID="gen2", name="gen2")
    builder.add_connectivity(machine, node="gen2_bus", BaseVoltage=base_voltage.mRID)

    builder.add_short_circuit(machine, ratedU=Qty(480, "V"), ratedPowerFactor=0.85)
    assert float(machine.ratedU.to("V")) == 480
