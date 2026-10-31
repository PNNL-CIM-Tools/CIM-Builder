import cimprofiles.cim18.cim18v17.construction as CONST

from cimbuilder.builders.base import ObjectBuilder
from cimtables import graph_write

class XYSpacingBuilder(ObjectBuilder):
    """LineModel05: x/y coordinate wire spacing (equivalent to OpenDSS
    LineSpacing/LineGeometry). add_conductor_position builds one
    XYConductorPosition per conductor, mirroring OpenDSS's cond=/x=/h=
    convention - one call per conductor, not a single table."""

    cim_class_name = 'XYSpacing'

    def add_conductor_position(self, spacing, *, sequenceNumber: int, xCoord, yCoord,
                                circuitNumber: int | None = None, kind=None) -> object:
        """Builds+returns an XYConductorPosition, FK'd to `spacing` via its
        own singular XYSpacing field."""
        position = self.cim.XYConductorPosition(name=f'{spacing.name}_{sequenceNumber}')
        graph_write.set_attr(position, CONST, 'sequenceNumber', sequenceNumber)
        graph_write.set_attr(position, CONST, 'xCoord', xCoord)
        graph_write.set_attr(position, CONST, 'yCoord', yCoord)
        graph_write.set_attr(position, CONST, 'circuitNumber', circuitNumber)
        if kind is not None:
            graph_write.set_attr(position, CONST, 'kind', self.cim.ConductorPositionKind(kind))
        graph_write.set_assc(position, CONST, 'XYSpacing', spacing)
        graph_write.add_to_graph(self.network, position)
        return position
