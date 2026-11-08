import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.inverter import PowerElectronicsConnectionBuilder


def test_power_electronics_connection_add_connectivity_phaseConnection_wrapped_in_enum(
    network, container, base_voltage
):
    builder = PowerElectronicsConnectionBuilder(network=network, container=container)
    inverter = builder.create(mRID="pec1", name="pec1")

    builder.add_connectivity(
        inverter, node="pec1_bus", phaseConnection="Y", BaseVoltage=base_voltage.mRID
    )

    assert inverter.phaseConnection == network.cim.PhaseShuntConnectionKind("Y")


def test_power_electronics_connection_add_connectivity(network, container, base_voltage):
    builder = PowerElectronicsConnectionBuilder(network=network, container=container)
    inverter = builder.create(mRID="pec1", name="pec1")

    inverter, terminal, phases = builder.add_connectivity(
        inverter, node="pec1_bus", phases="ABC", BaseVoltage=base_voltage.mRID
    )
    assert terminal.ConductingEquipment is inverter
    assert len(phases) == 3


def test_power_electronics_connection_add_electrical(network, container, base_voltage):
    builder = PowerElectronicsConnectionBuilder(network=network, container=container)
    inverter = builder.create(mRID="pec1", name="pec1")

    builder.add_electrical(
        inverter,
        ratedS=Qty(500, "kVA"),
        ratedU=Qty(480, "V"),
        minQ=Qty(-100, "kVAr"),
        maxQ=Qty(100, "kVAr"),
    )
    assert float(inverter.ratedS.to("kVA")) == 500


def test_power_electronics_connection_add_ssh(network, container, base_voltage):
    builder = PowerElectronicsConnectionBuilder(network=network, container=container)
    inverter = builder.create(mRID="pec1", name="pec1")

    builder.add_ssh(inverter, p=Qty(-300, "kW"), q=Qty(-50, "kVAr"), inService=True)
    assert inverter.inService is True
