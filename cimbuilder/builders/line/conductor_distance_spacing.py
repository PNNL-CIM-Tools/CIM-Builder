import cimprofiles.cim18.cim18v17.construction as CONST

from cimbuilder.builders.base import ObjectBuilder
from cimtables import graph_write

class ConductorDistanceSpacingBuilder(ObjectBuilder):
    """LineModel04: distance-pair wire spacing (equivalent to GridLAB-D
    line_spacing). add_conductor_distance builds one ConductorDistance row
    per described pair, mirroring GridLAB-D's distance_AB/distance_BC/...
    convention - one call per pair, not a single matrix."""

    cim_class_name = 'ConductorDistanceSpacing'

    def add_conductor_distance(self, spacing, *, sequenceNumber1: int, sequenceNumber2: int,
                                distance, conductorKind1=None, conductorKind2=None) -> object:
        """Builds+returns a ConductorDistance, FK'd to `spacing` via its own
        singular ConductorDistanceSpacing field (not the two undocumented
        fromSequenceNumber/toSequenceNumber fields - see this module's
        docstring)."""
        name = f'{spacing.name}_{sequenceNumber1}{sequenceNumber2}'
        pair = self.cim.ConductorDistance(name=name)
        graph_write.set_attr(pair, CONST, 'sequenceNumber1', sequenceNumber1)
        graph_write.set_attr(pair, CONST, 'sequenceNumber2', sequenceNumber2)
        graph_write.set_attr(pair, CONST, 'distance', distance)
        if conductorKind1 is not None:
            graph_write.set_attr(pair, CONST, 'conductorKind1', self.cim.ConductorPositionKind(conductorKind1))
        if conductorKind2 is not None:
            graph_write.set_attr(pair, CONST, 'conductorKind2', self.cim.ConductorPositionKind(conductorKind2))
        graph_write.set_assc(pair, CONST, 'ConductorDistanceSpacing', spacing)
        graph_write.add_to_graph(self.network, pair)
        return pair