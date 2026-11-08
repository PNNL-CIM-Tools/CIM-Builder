from cimtables.units import Qty

from cimbuilder.object_builder.line import ConductorDistanceSpacingBuilder


def test_conductor_distance_spacing_add_construction(network, container):
    builder = ConductorDistanceSpacingBuilder(network=network, container=container)
    spacing = builder.create(mRID="spacing1")
    builder.add_construction(spacing, isTemplate=True)
    assert spacing.isTemplate is True


def test_conductor_distance_spacing_add_conductor_distance_row(network, container):
    builder = ConductorDistanceSpacingBuilder(network=network, container=container)
    spacing = builder.create(mRID="spacing1")

    spacing, row = builder.add_conductor_distance_row(
        spacing,
        sequenceNumber1=1,
        sequenceNumber2=2,
        distance=Qty(1, "ft"),
        conductorKind1="phase",
        conductorKind2="phase",
    )
    assert row.ConductorDistanceSpacing is spacing


def test_conductor_distance_spacing_add_conductor_distance_row_to_earth(network, container):
    builder = ConductorDistanceSpacingBuilder(network=network, container=container)
    spacing = builder.create(mRID="spacing1")

    spacing, row = builder.add_conductor_distance_row(
        spacing,
        sequenceNumber1=1,
        sequenceNumber2=None,
        distance=Qty(10, "ft"),
        conductorKind1="phase",
        conductorKind2="earth",
    )
    assert row.sequenceNumber2 is None
