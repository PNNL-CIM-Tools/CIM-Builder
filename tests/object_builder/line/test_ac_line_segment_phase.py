import pytest

from cimbuilder.object_builder.line import ACLineSegmentBuilder, ACLineSegmentPhaseBuilder


def test_ac_line_segment_phase_add_connectivity_phase_wrapped_in_enum(
    network, container, base_voltage
):
    line_builder = ACLineSegmentBuilder(network=network, container=container)
    line = line_builder.create(mRID="line1")
    line_builder.add_connectivity(line, node1="bus1", node2="bus2", BaseVoltage=base_voltage.mRID)

    phs_builder = ACLineSegmentPhaseBuilder(network=network, container=container)
    phs = phs_builder.create(mRID="line1_A")

    phs_builder.add_connectivity(phs, 1, "A", line.mRID)

    assert phs.phase == network.cim.SinglePhaseKind("A")


def test_ac_line_segment_phase_add_asset_deployment_requires_existing_target(
    network, container
):
    phs_builder = ACLineSegmentPhaseBuilder(network=network, container=container)
    phs = phs_builder.create(mRID="line1_A")

    with pytest.raises(ValueError):
        phs_builder.add_asset_deployment(phs, WireInfo="does_not_exist")
