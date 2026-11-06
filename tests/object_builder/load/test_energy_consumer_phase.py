import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.load import EnergyConsumerBuilder, EnergyConsumerPhaseBuilder


def test_energy_consumer_phase_add_connectivity_phase_not_wrapped_in_enum(network, container):
    """add_connectivity calls
    graph_write.set_attr(load_phs, CN, "phase", phase) with the raw
    string, instead of wrapping it as cn.SinglePhaseKind(phase). Same
    recurring bug as ac_line_segment_phase.py/
    power_electronics_connection_phase.py/
    linear_shunt_compensator_phase.py - raises for every call since
    phase isn't optional."""
    load_builder = EnergyConsumerBuilder(network=network, container=container)
    load = load_builder.create(mRID="load1")

    phs_builder = EnergyConsumerPhaseBuilder(network=network, container=container)
    phs = phs_builder.create(mRID="load1_A")

    with pytest.raises(TypeError, match="SinglePhaseKind"):
        phs_builder.add_connectivity(phs, "A", load.mRID)


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
