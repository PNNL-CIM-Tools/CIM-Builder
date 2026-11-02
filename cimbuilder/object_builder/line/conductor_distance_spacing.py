import cimprofiles.cim18.cim18v17.construction as CONSTR
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class ConductorDistanceSpacingBuilder(ObjectBuilder):
    """
    Create a phase-to-phase conductor distance specification (used by GridLAB-D, Hitachi, etc.)
    """

    cim_class_name = "ConductorDistanceSpacing"

    def add_conductor_distance_row(
        self,
        spacing: CONSTR.ConductorDistanceSpacing,
        *,
        sequenceNumber1: int,
        sequenceNumber2: int | None,
        distance: float|Qty,
        conductorKind1: str,
        conductorKind2: str,
    ) -> tuple[CONSTR.ConductorDistanceSpacing, CONSTR.ConductorDistance]:
        """
        Adds a single phase-to-phase conductor distance pair
        * sequenceNumber1: integer, sequenceNumber of the "from" ACLineSegmentPhase
        * sequenceNumber2: integer, sequenceNumber of the "to" ACLineSegmentPhase
        * distance: distance between conductors, float in meter or Qty('length')
        * conductorKind1: string, phase|shield|neutral|earth
        * conductorKind2: string, phase|shield|neutral|earth
        """
        constr: CONSTR = self.cim  # type: ignore
        if sequenceNumber2 is not None:
            mRID = f"{spacing.mRID}_{sequenceNumber1}_{sequenceNumber2}"
        else:
            mRID = f"{spacing.mRID}_{sequenceNumber1}_earth"

        distance_row = constr.ConductorDistance(mRID=mRID)
        graph_write.set_attr(distance_row, CONSTR, "sequenceNumber1", sequenceNumber1)
        graph_write.set_attr(distance_row, CONSTR, "sequenceNumber2", sequenceNumber2)
        graph_write.set_attr(distance_row, CONSTR, "distance", distance)
        if conductorKind1 is not None:
            graph_write.set_attr(
                source_object=distance_row,
                profile_part=CONSTR,
                attribute_name="conductorKind1",
                attribute_value=constr.ConductorPositionKind(conductorKind1),
            )
        if conductorKind2 is not None:
            graph_write.set_attr(
                source_object=distance_row,
                profile_part=CONSTR,
                attribute_name="conductorKind2",
                attribute_value=constr.ConductorPositionKind(conductorKind2),
            )
        graph_write.set_assc(distance_row, CONSTR, "ConductorDistanceSpacing", spacing)
        graph_write.add_to_graph(self.network, distance_row)
        return spacing, distance_row
