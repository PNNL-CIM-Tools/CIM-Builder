"""The reusable per-length/per-geometry template tier for lines (design:
Phase 3 of cimbuilder/development/OBJECT_BUILDER_MIGRATION.md; see the
approved implementation plan for the full field-location evidence).

Builds the two per-length template shapes LineModel02/03 show:
PerLengthSequenceImpedance (balanced, LineModel02 - OpenDSS LineCode's
positive-sequence form) and PerLengthPhaseImpedance + PhaseImpedanceData
(unbalanced matrix, LineModel03 - OpenDSS LineCode's rmatrix/xmatrix/cmatrix
form, confirmed against
/home/ande188/CIMTBL-Models/distribution/IEEE/IEEE13_CDPSM/linecodes.cimtbl),
plus the wire-geometry template shapes LineModel04/05 show:
WireConfiguration -> WireSpacing, either ConductorDistanceSpacing
(LineModel04, distance-pair form, equivalent to GridLAB-D line_spacing) or
XYSpacing (LineModel05, x/y coordinate form, equivalent to OpenDSS
LineSpacing/LineGeometry). ACLineSegmentBuilder.add_per_length_impedance /
.add_wire_configuration reference a built template by name - it never
builds one itself.

Field locations confirmed directly against the installed cimprofiles
package (do not assume):
- PerLengthSequenceImpedance's own scalars (bch/gch/r/x) live entirely in
  electrical_balanced - it has no definition at all in any other part
  module checked (electrical_unbalanced/connectivity_unbalanced/construction/
  short_circuit).
- calculatedFrequency/rg/xg (PerLengthImpedance's own base-class fields,
  shared by both template shapes) also live in electrical_balanced.
- PerLengthPhaseImpedance's own scalar (conductorCount) and its
  PhaseImpedanceData list FK both live in electrical_unbalanced - NOT
  construction, which also defines a PerLengthPhaseImpedance class but with
  no fields of its own at all (a bare pass-through placeholder in that part
  module).
- PhaseImpedanceData's own FK back to its matrix is the singular field
  'PhaseImpedance' (easy to miss on a quick scan - it sits right after the
  x scalar, long after the docstring most readers stop at). set_assc is
  called from this singular side, once per row
  (data.PhaseImpedance = matrix), which auto-appends data onto
  matrix.PhaseImpedanceData's list via the field's own
  inverse='PerLengthPhaseImpedance.PhaseImpedanceData' metadata - calling
  set_assc from the list side instead, with a list target, would wrongly
  append the whole list as a single list element (_set_side's list branch
  expects one target object per call, not a list of them).
- row/column bind to ACLineSegmentPhase.sequenceNumber (the order written in
  an ACLineSegmentBuilder.add_connectivity phases= string), not to a direct
  per-phase FK - confirmed against lines.cimtbl/linecodes.cimtbl's own
  convention (phases='CB' -> sequenceNumber 1=C, 2=B -> matrix row/column
  1/2). This builder does not resolve or validate that binding; it is purely
  declarative data the caller supplies already matched to the line's
  eventual phases order.
- WireConfiguration (numberOfPhases/installationType/usage, plus the
  singular WireSpacing FK) lives entirely in construction - the only part
  module that defines this class at all.
- ConductorDistanceSpacing and XYSpacing are both pure type-tag subclasses
  of WireSpacing with no fields of their own beyond what their children
  carry - WireSpacing itself only has list FKs back to ACLineSegment/
  WireConfiguration (the inverse side of singular fields that live on
  those other classes, not here). All the real geometry data lives on the
  per-conductor child rows (ConductorDistance, XYConductorPosition), not on
  the spacing container itself.
- ConductorDistance's singular FK back to its spacing is
  ConductorDistanceSpacing (not fromSequenceNumber/toSequenceNumber, a
  second, undocumented pair of gridappsd-extension fields on the same
  class with empty docstrings - this builder uses sequenceNumber1/
  sequenceNumber2 instead, the real CIM101 fields matching LineModel04's
  diagram and the only ones with actual documentation).
- XYConductorPosition's singular FK back to its spacing is XYSpacing
  (construction's own field); xCoord/yCoord are inherited from the shared
  SpacingPosition base, also in construction.
"""

import cimprofiles.cim18.cim18v17.construction as CONST
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL

from cimbuilder.builders.base import ObjectBuilder
from cimtables import graph_write


class PerLengthSequenceImpedanceBuilder(ObjectBuilder):
    """LineModel02: balanced per-length template (OpenDSS LineCode)."""

    cim_class_name = 'PerLengthSequenceImpedance'

    def add_rating(self, impedance, *, r=None, x=None, bch=None, gch=None,
                    calculatedFrequency=None, rg=None, xg=None) -> None:
        graph_write.set_attr(impedance, EL_BAL, 'r', r)
        graph_write.set_attr(impedance, EL_BAL, 'x', x)
        graph_write.set_attr(impedance, EL_BAL, 'bch', bch)
        graph_write.set_attr(impedance, EL_BAL, 'gch', gch)
        graph_write.set_attr(impedance, EL_BAL, 'calculatedFrequency', calculatedFrequency)
        graph_write.set_attr(impedance, EL_BAL, 'rg', rg)
        graph_write.set_attr(impedance, EL_BAL, 'xg', xg)


class PerLengthPhaseImpedanceBuilder(ObjectBuilder):
    """LineModel03: unbalanced matrix per-length template (OpenDSS LineCode's
    rmatrix/xmatrix/cmatrix form), confirmed against linecodes.cimtbl."""

    cim_class_name = 'PerLengthPhaseImpedance'

    def add_rating(self, matrix, *, conductorCount: int | None = None,
                    calculatedFrequency=None, rg=None, xg=None) -> None:
        # calculatedFrequency/rg/xg are PerLengthImpedance's own base-class
        # fields, inherited by both PerLengthSequenceImpedance and
        # PerLengthPhaseImpedance - but _part_field matches by exact class
        # name, not inheritance, and electrical_balanced has no
        # PerLengthPhaseImpedance class at all (only electrical_unbalanced
        # does). So this method's part module is EL_UNBAL throughout, unlike
        # PerLengthSequenceImpedanceBuilder's EL_BAL.
        graph_write.set_attr(matrix, EL_UNBAL, 'conductorCount', conductorCount)
        graph_write.set_attr(matrix, EL_UNBAL, 'calculatedFrequency', calculatedFrequency)
        graph_write.set_attr(matrix, EL_UNBAL, 'rg', rg)
        graph_write.set_attr(matrix, EL_UNBAL, 'xg', xg)

    def add_phase_impedance_data(self, matrix, *, entries: list[dict]) -> list[object]:
        """entries = [{'row': 1, 'column': 1, 'r': ..., 'x': ..., 'b': ...}, ...],
        one dict per lower-triangle matrix element - mirrors
        linecodes.cimtbl's PhaseImpedanceData table exactly (row >= column).
        Builds+returns the PhaseImpedanceData rows, FK'd to `matrix` via its
        PhaseImpedanceData list field (the only side of the association that
        carries an explicit FK - see this module's docstring)."""
        data_rows = []
        for entry in entries:
            data = self.cim.PhaseImpedanceData(name=f"{matrix.name}_{entry['row']}_{entry['column']}")
            graph_write.set_attr(data, EL_UNBAL, 'row', entry['row'])
            graph_write.set_attr(data, EL_UNBAL, 'column', entry['column'])
            graph_write.set_attr(data, EL_UNBAL, 'r', entry.get('r'))
            graph_write.set_attr(data, EL_UNBAL, 'x', entry.get('x'))
            graph_write.set_attr(data, EL_UNBAL, 'b', entry.get('b'))
            graph_write.set_attr(data, EL_UNBAL, 'g', entry.get('g'))
            graph_write.set_assc(data, EL_UNBAL, 'PhaseImpedance', matrix)
            graph_write.add_to_graph(self.network, data)
            data_rows.append(data)
        return data_rows


class WireConfigurationBuilder(ObjectBuilder):
    """LineModel04/05's template container: WireConfiguration ->
    WireSpacing. Build the WireSpacing first (via ConductorDistanceSpacingBuilder
    or XYSpacingBuilder), then add_rating here to set it - same build-template-
    then-reference-it ordering as every other template tier in this codebase."""

    cim_class_name = 'WireConfiguration'

    def add_rating(self, config, *, numberOfPhases: int | None = None, installationType=None,
                    usage=None, WireSpacing: str | None = None) -> None:
        graph_write.set_attr(config, CONST, 'numberOfPhases', numberOfPhases)
        if installationType is not None:
            graph_write.set_attr(config, CONST, 'installationType', self.cim.WireInstallationKind(installationType))
        if usage is not None:
            graph_write.set_attr(config, CONST, 'usage', self.cim.WireUsageKind(usage))
        if WireSpacing is not None:
            target = graph_write.resolve_any_subclass(self.network, self.cim.WireSpacing, WireSpacing)
            if target is None:
                raise ValueError(
                    f"{config.name!r}: WireSpacing {WireSpacing!r} not found in graph "
                    f"(build the spacing before the WireConfiguration that references it)"
                )
            graph_write.set_assc(config, CONST, 'WireSpacing', target)


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
