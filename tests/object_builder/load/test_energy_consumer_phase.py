import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.load import EnergyConsumerBuilder, EnergyConsumerPhaseBuilder


def test_energy_consumer_phase_add_connectivity_phase_wrapped_in_enum(network, container):
    load_builder = EnergyConsumerBuilder(network=network, container=container)
    load = load_builder.create(mRID="load1")

    phs_builder = EnergyConsumerPhaseBuilder(network=network, container=container)
    phs = phs_builder.create(mRID="load1_A")

    phs_builder.add_connectivity(phs, "A", load.mRID)

    assert phs.phase == network.cim.SinglePhaseKind("A")


def test_energy_consumer_phase_add_electrical(network, container):
    builder = EnergyConsumerPhaseBuilder(network=network, container=container)
    phs = builder.create(mRID="load1_A")

    builder.add_electrical(phs, pfixed=Qty(3, "kW"), qfixed=Qty(1, "kVAr"))
    assert float(phs.pfixed.to("kW")) == 3


def test_energy_consumer_phase_add_ssh(network, container):
    builder = EnergyConsumerPhaseBuilder(network=network, container=container)
    phs = builder.create(mRID="load1_A")

    builder.add_ssh(phs, p=Qty(3, "kW"), q=Qty(1, "kVAr"))
    assert float(phs.p.to("kW")) == 3
