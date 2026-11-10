from cimtables.units import Qty

from cimbuilder.object_builder.line import XYSpacingBuilder


def test_xy_spacing_create_is_template(network, container):
    builder = XYSpacingBuilder(network=network, container=container)
    spacing = builder.create(mRID="xy_spacing1", name="xy_spacing1", isTemplate=True)
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


def test_xy_spacing_positions_keyed_by_spacing_mrid(network, container):
    """two unnamed spacings must not collide on their positions' identities"""
    builder = XYSpacingBuilder(network=network, container=container)
    positions = []
    for mRID in ("spc_500", "spc_505"):
        spacing = builder.create(mRID=mRID)
        _, position = builder.add_wire_position_row(
            spacing, sequenceNumber=1, xCoord=Qty(-4, "ft"), yCoord=Qty(28, "ft")
        )
        positions.append(position)
    assert [position.mRID for position in positions] == ["spc_500_1", "spc_505_1"]
    assert positions[0].XYSpacing.mRID == "spc_500"
