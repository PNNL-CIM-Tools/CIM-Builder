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
        docstring).
        * sequenceNumber1/sequenceNumber2: plain ints, the conductor-position
          indices this distance is between (matches the phases= order a
          line's add_connectivity sets on its ACLineSegmentPhase children).
        * distance: a Qty (e.g. Qty(18, 'in'), Qty(0.5, 'm')) - set_attr
          resolves it to construction.Displacement (meters, SI base). A bare
          number is NOT unit-converted and should not be passed.
        * conductorKind1/conductorKind2: string value of
          construction.ConductorPositionKind (e.g. 'wire') - converted via
          `self.cim.ConductorPositionKind(...)` before set_attr; left unset
          (not even None-written) when omitted.

        Returns the built, graph-added ConductorDistance.
        """
        mRID = f'{spacing.mRID}_{sequenceNumber1}{sequenceNumber2}'
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
        return pair