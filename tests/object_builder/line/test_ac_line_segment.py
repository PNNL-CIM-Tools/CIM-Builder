import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.line import ACLineSegmentBuilder


def test_ac_line_segment_add_connectivity(network, container, base_voltage):
    builder = ACLineSegmentBuilder(network=network, container=container)
    line = builder.create(mRID="line1", name="line1")

    line, terminals, phases = builder.add_connectivity(
        line,
        node1="bus1",
        node2="bus2",
        phases="ABC",
        length=Qty(500, "ft"),
        BaseVoltage=base_voltage.mRID,
    )
    assert len(terminals) == 2
    assert len(phases) == 3


def test_ac_line_segment_add_electrical(network, container, base_voltage):
    builder = ACLineSegmentBuilder(network=network, container=container)
    line = builder.create(mRID="line1", name="line1")
    builder.add_connectivity(line, node1="bus1", node2="bus2", BaseVoltage=base_voltage.mRID)

    builder.add_electrical(line, r=5, x=Qty(0.05, "ohm"), bch=Qty(0.05, "S"))
    assert float(line.r.to("ohm")) == 5


def test_ac_line_segment_add_short_circuit(network, container, base_voltage):
    builder = ACLineSegmentBuilder(network=network, container=container)
    line = builder.create(mRID="line1", name="line1")
    builder.add_connectivity(line, node1="bus1", node2="bus2", BaseVoltage=base_voltage.mRID)

    builder.add_short_circuit(line, r0=5, x0=Qty(0.05, "pu"))
    assert float(line.r0.to("ohm")) == 5


def test_ac_line_segment_add_per_length_impedance_requires_existing_target(
    network, container, base_voltage
):
    """add_per_length_impedance resolves PerLengthImpedance by mRID via
    set_assc_from_mrid - raises ValueError when no object with that mRID
    exists in the graph yet (the documented resolve() contract)."""
    builder = ACLineSegmentBuilder(network=network, container=container)
    line = builder.create(mRID="line1", name="line1")
    builder.add_connectivity(line, node1="bus1", node2="bus2", BaseVoltage=base_voltage.mRID)

    with pytest.raises(ValueError):
        builder.add_per_length_impedance(line, PerLengthImpedance="does_not_exist")


def test_ac_line_segment_add_wire_configuration_requires_existing_target(
    network, container, base_voltage
):
    builder = ACLineSegmentBuilder(network=network, container=container)
    line = builder.create(mRID="line1", name="line1")
    builder.add_connectivity(line, node1="bus1", node2="bus2", BaseVoltage=base_voltage.mRID)

    with pytest.raises(ValueError):
        builder.add_wire_configuration(line, WireConfiguration="does_not_exist")


def test_ac_line_segment_add_multi_circuit_group_requires_existing_target(
    network, container, base_voltage
):
    builder = ACLineSegmentBuilder(network=network, container=container)
    line = builder.create(mRID="line1", name="line1")
    builder.add_connectivity(line, node1="bus1", node2="bus2", BaseVoltage=base_voltage.mRID)

    with pytest.raises(ValueError):
        builder.add_multi_circuit_group(line, circuitNumber=1, MultiCircuitGroup="does_not_exist")


def test_ac_line_segment_add_ssh_is_not_a_method(network, container, base_voltage):
    """add_ssh in ac_line_segment.py is defined at MODULE level (outside
    the class body, dedented), not as an ACLineSegmentBuilder method -
    builder.add_ssh does not exist."""
    builder = ACLineSegmentBuilder(network=network, container=container)
    line = builder.create(mRID="line1", name="line1")

    assert not hasattr(builder, "add_ssh")
