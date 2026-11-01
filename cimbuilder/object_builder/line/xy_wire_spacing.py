import cimprofiles.cim18.cim18v17.construction as CONST

from cimbuilder.object_builder.object_builder import ObjectBuilder
from cimtables import graph_write

class XYSpacingBuilder(ObjectBuilder):
    """
    XY spacing. This replaces WireSpacingInfo from CIM17
    (equivalent to OpenDSS line geometry)
    """
    cim_class_name = 'XYSpacing'

    def add_wire_position_row(self, spacing, *, sequenceNumber: int, xCoord, yCoord,
                                circuitNumber: int | None = None, kind=None) -> None:
        """
        Adds XY coordinates of a single conductor relative to origin (e.g. top of pole)
        * sequenceNumber: integer, matches the sequenceNumber of the ACLineSegmentPhase
        * xCoord: horizontal distance from center of pole, float in meter or Qty('length')
        * yCoord: vertical distance from origin (e.g. top of pole), float in meter or Qty('length')
        * circuitNumber: integer, matches the circuitNumber of the ACLineSegment
        * kind: string, phase|shield|neutral|mixed
        """
        if circuitNumber is not None:
            name = f'{spacing.name}_{sequenceNumber}_{circuitNumber}'
        else:
            name = f'{spacing.name}_{sequenceNumber}'
          
        position = self.cim.XYConductorPosition(name=name)
        graph_write.set_attr(position, CONST, 'sequenceNumber', sequenceNumber)
        graph_write.set_attr(position, CONST, 'xCoord', xCoord)
        graph_write.set_attr(position, CONST, 'yCoord', yCoord)
        graph_write.set_attr(position, CONST, 'circuitNumber', circuitNumber)
        if kind is not None:
            graph_write.set_attr(position, CONST, 'kind', self.cim.ConductorPositionKind(kind))
        graph_write.set_assc(position, CONST, 'XYSpacing', spacing)
        graph_write.add_to_graph(self.network, position)
        
