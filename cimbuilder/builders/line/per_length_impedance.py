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

    def add_electrical(self, impedance, *, r=None, x=None, bch=None, gch=None,
                    calculatedFrequency=None, rg=None, xg=None) -> None:
        """Positive-sequence per-length impedance (electrical_balanced.PerLengthSequenceImpedance),
        the OpenDSS LineCode form. All params are per-unit-length Qtys unless noted:
        * r: resolves to Resistance (ohm, SI base) - but note this is really
          an ohm-per-length value stored on a field typed as plain
          Resistance, not a PerLength unit; the caller is responsible for
          using whatever length basis the rest of the model assumes.
        * x: resolves to Reactance (ohm, SI base), same per-length caveat.
        * bch: resolves to Susceptance (siemens, SI base), same caveat.
        * gch: resolves to Conductance (siemens, SI base), same caveat.
        * calculatedFrequency: resolves to Frequency (Hz, SI base) - the
          frequency r/x/bch/gch were calculated at.
        * rg/xg: resolve to Resistance/Reactance (ohm, SI base) - ground
          return path values.
        A bare number for any of these is stored unconverted via plain
        setattr. No `z_base` is ever passed here, so a pu/percent r or x
        would raise ValueError.
        """
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

    def add_electrical_earthing(self, matrix, *, conductorCount: int | None = None,
                    calculatedFrequency=None, rg=None, xg=None) -> None:
        """
        * conductorCount: plain int, no unit wrapping.
        * calculatedFrequency: a Qty resolved to Frequency (Hz, SI base).
        * rg/xg: Qtys resolved to ResistancePerLength/ReactancePerLength
          (ohm/m, SI base) - ground return path values, inherited
          PerLengthImpedance base-class fields.
        A bare number for calculatedFrequency/rg/xg is stored unconverted.
        """
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
        carries an explicit FK - see this module's docstring).

        Each entry dict:
        * row/column: plain ints, no unit wrapping (also note: entries with
          no 'row'/'column' key will KeyError, since these are accessed via
          entry['row']/entry['column'] rather than .get()).
        * r/x: optional Qtys (via entry.get, defaulting to None) resolved to
          ResistancePerLength/ReactancePerLength (ohm/m, SI base).
        * b/g: optional Qtys resolved to SusceptancePerLength/
          ConductancePerLength (siemens/m, SI base).
        A bare number for r/x/b/g is stored unconverted via plain setattr.
        """
        data_rows = []
        for entry in entries:
            # Identity-only class (no mRID/name field) - seed its UUID from a
            # stable key instead, same route cimtables.binder uses for
            # Identity-only rows (MRID_MIGRATION.md).
            data = self.cim.PhaseImpedanceData()
            data.uuid(mRID=f"{matrix.mRID}_{entry['row']}_{entry['column']}")
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


