import pytest

from cimbuilder.object_builder.line import ACLineSegmentBuilder, ACLineSegmentPhaseBuilder


def test_ac_line_segment_phase_add_connectivity_phase_not_wrapped_in_enum(
    network, container, base_voltage
):
    """add_connectivity calls
    graph_write.set_attr(line_phs, CN, "phase", phase) with the raw
    `phase` string, instead of wrapping it as cn.SinglePhaseKind(phase)
    the way switch_phase.py's add_connectivity does for phaseSide1/2.
    CN.ACLineSegmentPhase.phase is SinglePhaseKind-typed and `phase` isn't
    optional, so this raises for every call. Same recurring bug as
    power_electronics_connection_phase.py, energy_consumer_phase.py and
    linear_shunt_compensator_phase.py."""
    line_builder = ACLineSegmentBuilder(network=network, container=container)
    line = line_builder.create(mRID="line1")
    line_builder.add_connectivity(line, node1="bus1", node2="bus2", BaseVoltage=base_voltage.mRID)

    phs_builder = ACLineSegmentPhaseBuilder(network=network, container=container)
    phs = phs_builder.create(mRID="line1_A")

    with pytest.raises(TypeError, match="SinglePhaseKind"):
        phs_builder.add_connectivity(phs, 1, "A", line.mRID)


def test_ac_line_segment_phase_add_asset_deployment_requires_existing_target(
    network, container
):
    phs_builder = ACLineSegmentPhaseBuilder(network=network, container=container)
    phs = phs_builder.create(mRID="line1_A")

    with pytest.raises(ValueError):
        phs_builder.add_asset_deployment(phs, WireInfo="does_not_exist")
