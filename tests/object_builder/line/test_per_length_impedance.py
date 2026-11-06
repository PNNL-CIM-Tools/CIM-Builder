import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.line import (
    PerLengthPhaseImpedanceBuilder,
    PerLengthSequenceImpedanceBuilder,
    WireConfigurationBuilder,
)


def test_per_length_sequence_impedance_add_electrical(network, container):
    builder = PerLengthSequenceImpedanceBuilder(network=network, container=container)
    impedance = builder.create(mRID="plz1")

    builder.add_electrical(
        impedance,
        r=Qty(0.1, "ohm/mi"),
        x=Qty(0.2, "ohm/mi"),
        bch=Qty(1e-6, "S/mi"),
        isTemplate=True,
        calculatedFrequency=Qty(60, "Hz"),
        calculatedTemperature=None,
    )
    assert impedance.isTemplate is True


def test_per_length_sequence_impedance_add_short_circuit(network, container):
    builder = PerLengthSequenceImpedanceBuilder(network=network, container=container)
    impedance = builder.create(mRID="plz1")

    builder.add_short_circuit(impedance, r0=Qty(0.3, "ohm/mi"), x0=Qty(0.4, "ohm/mi"))
    assert float(impedance.r0.to("ohm/mi")) == 0.3


def test_per_length_sequence_impedance_add_electrical_earthing(network, container):
    builder = PerLengthSequenceImpedanceBuilder(network=network, container=container)
    impedance = builder.create(mRID="plz1")

    builder.add_electrical_earthing(impedance, rg=Qty(0.05, "ohm/mi"), xg=Qty(0.05, "ohm/mi"))
    assert float(impedance.rg.to("ohm/mi")) == pytest.approx(0.05)


def test_per_length_sequence_impedance_add_wire_configuration(network, container):
    wc_builder = WireConfigurationBuilder(network=network, container=container)
    config = wc_builder.create(mRID="wc1")

    builder = PerLengthSequenceImpedanceBuilder(network=network, container=container)
    impedance = builder.create(mRID="plz1")

    builder.add_wire_configuration(impedance, WireConfiguration=config.mRID)
    assert impedance.WireConfiguration is config


def test_per_length_phase_impedance_add_electrical(network, container):
    builder = PerLengthPhaseImpedanceBuilder(network=network, container=container)
    matrix = builder.create(mRID="plp1")

    builder.add_electrical(
        matrix,
        conductorCount=3,
        isTemplate=True,
        calculatedFrequency=Qty(60, "Hz"),
        calculatedTemperature=None,
    )
    assert matrix.conductorCount == 3


def test_per_length_phase_impedance_add_phase_impedance_data_row_phase_not_wrapped_in_enum(
    network, container
):
    """add_phase_impedance_data_row calls
    graph_write.set_attr(data, EL_UNBAL, "fromPhase", fromPhase) and
    "toPhase" with the raw strings, instead of wrapping them as
    cn.SinglePhaseKind(...). Both fields are SinglePhaseKind-typed and
    neither is optional, so this raises for every call - same recurring
    bug pattern as ac_line_segment_phase.py's add_connectivity."""
    builder = PerLengthPhaseImpedanceBuilder(network=network, container=container)
    matrix = builder.create(mRID="plp1")

    with pytest.raises(TypeError, match="SinglePhaseKind"):
        builder.add_phase_impedance_data_row(
            matrix,
            row=1,
            column=1,
            r=Qty(0.1, "ohm/mi"),
            x=Qty(0.2, "ohm/mi"),
            b=None,
            g=None,
            fromPhase="A",
            toPhase="A",
        )


def test_per_length_phase_impedance_add_electrical_earthing(network, container):
    builder = PerLengthPhaseImpedanceBuilder(network=network, container=container)
    matrix = builder.create(mRID="plp1")

    builder.add_electrical_earthing(matrix, rg=Qty(0.05, "ohm/mi"), xg=Qty(0.05, "ohm/mi"))
    assert float(matrix.rg.to("ohm/mi")) == pytest.approx(0.05)
