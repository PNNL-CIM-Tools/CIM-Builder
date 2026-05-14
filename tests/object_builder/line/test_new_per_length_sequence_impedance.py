"""Tests for cimbuilder.object_builder.line.new_per_length_sequence_impedance."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.line.new_per_length_sequence_impedance import (
    new_per_length_sequence_impedance,
)


def test_basic(simple_substation_network):
    cim = get_cim()
    net = simple_substation_network["network"]

    z = new_per_length_sequence_impedance(
        net, "Z1",
        r_ohm_per_km=0.1, x_ohm_per_km=0.4,
        bch_S_per_km=2e-6, gch_S_per_km=1e-7,
    )
    assert isinstance(z, cim.PerLengthSequenceImpedance)
    assert z.name == "Z1"
    assert isinstance(z.r, cim.ResistancePerLength)
    # base SI for ResistancePerLength is ohm/m, so 0.1 ohm/km == 1e-4 ohm/m
    assert abs(float(z.r) - 1e-4) < 1e-12
    assert isinstance(z.x, cim.ReactancePerLength)
    assert isinstance(z.bch, cim.SusceptancePerLength)
    assert isinstance(z.gch, cim.ConductancePerLength)
    assert z in net.graph.get(cim.PerLengthSequenceImpedance, {}).values()


def test_zero_sequence(simple_substation_network):
    cim = get_cim()
    net = simple_substation_network["network"]

    z = new_per_length_sequence_impedance(
        net, "Z2",
        r0_ohm_per_km=0.3, x0_ohm_per_km=1.2,
        b0ch_S_per_km=4e-6, g0ch_S_per_km=2e-7,
    )
    assert isinstance(z.r0, cim.ResistancePerLength)
    assert isinstance(z.x0, cim.ReactancePerLength)
    assert isinstance(z.b0ch, cim.SusceptancePerLength)
    assert isinstance(z.g0ch, cim.ConductancePerLength)
