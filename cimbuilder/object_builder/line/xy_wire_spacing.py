import cimprofiles.cim18.cim18v17.construction as CONSTR
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class XYSpacingBuilder(ObjectBuilder):
    """
    XY spacing. This replaces WireSpacingInfo from CIM17
    (equivalent to OpenDSS line geometry)
    """

    cim_class_name = "XYSpacing"

    def add_construction(
        self,
        spacing:CONSTR.XYSpacing,
        *,
        isTemplate: bool | None = None,
    ) -> CONSTR.XYSpacing:
        """
        * isTemplate: denotes if used as part of a WireConfiguration template
        """
        graph_write.set_attr(spacing, CONSTR, "isTemplate", isTemplate)
        return spacing

    def add_wire_position_row(
        self,
        spacing: CONSTR.XYSpacing,
        *,
        sequenceNumber: int,
        xCoord: float | Qty,
        yCoord: float | Qty,
        circuitNumber: int | None = None,
        kind: str | None = None,
    ) -> None:
        """
        Adds XY coordinates of a single conductor relative to origin (e.g. top of pole)
        * sequenceNumber: integer, matches the sequenceNumber of the ACLineSegmentPhase
        * xCoord: horizontal distance from center of pole, float in meter or Qty('length')
        * yCoord: vertical distance from origin (e.g. top of pole), float in meter or Qty('length')
        * circuitNumber: integer, matches the circuitNumber of the ACLineSegment
        * kind: string, phase|shield|neutral|mixed
        """
        constr: CONSTR = self.cim  # type: ignore
        if circuitNumber is not None:
            name = f"{spacing.name}_{sequenceNumber}_{circuitNumber}"
        else:
            name = f"{spacing.name}_{sequenceNumber}"

        position = constr.XYConductorPosition(name=name)
        graph_write.set_attr(position, CONSTR, "sequenceNumber", sequenceNumber)
        graph_write.set_attr(position, CONSTR, "xCoord", xCoord)
        graph_write.set_attr(position, CONSTR, "yCoord", yCoord)
        graph_write.set_attr(position, CONSTR, "circuitNumber", circuitNumber)
        if kind is not None:
            graph_write.set_attr(
                position, CONSTR, "kind", constr.ConductorPositionKind(kind)
            )
        graph_write.set_assc(position, CONSTR, "XYSpacing", spacing)
        graph_write.add_to_graph(self.network, position)
