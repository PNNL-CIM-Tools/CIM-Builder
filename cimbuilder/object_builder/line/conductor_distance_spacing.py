import cimprofiles.cim18.cim18v17.construction as CONST

from cimbuilder.object_builder.object_builder import ObjectBuilder
from cimtables import graph_write

class ConductorDistanceSpacingBuilder(ObjectBuilder):
    """
    Create a phase-to-phase conductor distance specification (used by GridLAB-D, Hitachi, etc.)
    """

    cim_class_name = 'ConductorDistanceSpacing'

    def add_conductor_distance_row(self, spacing, *, sequenceNumber1: int, sequenceNumber2: int|None,
                              distance, conductorKind1, conductorKind2) -> object:
        """
        Adds a single phase-to-phase conductor distance pair
        * sequenceNumber1: integer, sequenceNumber of the "from" ACLineSegmentPhase
        * sequenceNumber2: integer, sequenceNumber of the "to" ACLineSegmentPhase
        * distance: distance between conductors, float in meter or Qty('length')
        * conductorKind1: string, phase|shield|neutral|earth
        * conductorKind2: string, phase|shield|neutral|earth
        """
        if sequenceNumber2 is not None:
            mRID = f'{spacing.mRID}_{sequenceNumber1}_{sequenceNumber2}'
        else:
            mRID = f'{spacing.mRID}_{sequenceNumber1}_earth'
            
        pair = self.cim.ConductorDistance(mRID=mRID)
        graph_write.set_attr(pair, CONST, 'sequenceNumber1', sequenceNumber1)
        graph_write.set_attr(pair, CONST, 'sequenceNumber2', sequenceNumber2)
        graph_write.set_attr(pair, CONST, 'distance', distance)
        if conductorKind1 is not None:
            graph_write.set_attr(pair, CONST, 'conductorKind1', self.cim.ConductorPositionKind(conductorKind1))
        if conductorKind2 is not None:
            graph_write.set_attr(pair, CONST, 'conductorKind2', self.cim.ConductorPositionKind(conductorKind2))
        graph_write.set_assc(pair, CONST, 'ConductorDistanceSpacing', spacing)
        graph_write.add_to_graph(self.network, pair)
