from cimtables.units import Qty

from cimbuilder.object_builder.line import XYSpacingBuilder


def test_xy_spacing_add_construction(network, container):
    builder = XYSpacingBuilder(network=network, container=container)
    spacing = builder.create(mRID="xy_spacing1", name="xy_spacing1")
    builder.add_construction(spacing, isTemplate=True)
    assert spacing.isTemplate is True


def test_xy_spacing_add_wire_position_row(network, container):
    builder = XYSpacingBuilder(network=network, container=container)
    spacing = builder.create(mRID="xy_spacing1", name="xy_spacing1")

    builder.add_wire_position_row(
        spacing,
        sequenceNumber=1,
        xCoord=Qty(-1, "ft"),
        yCoord=Qty(30, "ft"),
        circuitNumber=1,
        kind="phase",
    )
