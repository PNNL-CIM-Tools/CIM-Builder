"""ACLineSegmentBuilder: the instance tier (design: Phase 3 of
cimbuilder/development/OBJECT_BUILDER_MIGRATION.md, resolved against real
.cimtbl reference models and Visio modeling reference diagrams
(LineModel01-05) - see the approved implementation plan for the full
field-location evidence).

Four coexisting CIM line-impedance representations, confirmed against the
installed cimprofiles.cim18.cim18v17 package:

1. Direct balanced PI (LineModel01) - add_electrical writes r/x/bch/gch
   straight onto the ACLineSegment. Positive-sequence balanced impedance,
   commonly used by PSS/E/PowerWorld.
2. Direct zero-sequence PI (also LineModel01) - add_short_circuit writes
   r0/x0/b0ch/g0ch, the zero-sequence counterpart to shape 1.
3/4. Per-length reference (LineModel02 balanced, LineModel03 unbalanced
   matrix) - add_per_length_impedance resolves a PerLengthSequenceImpedance
   or PerLengthPhaseImpedance template by name and sets the one FK field
   both shapes share. The template itself is built by
   PerLengthImpedanceBuilder (by_template.py); this builder only
   references it.

Field locations confirmed directly against the installed cimprofiles
package (do not assume - every part module below was grepped, not guessed):
- r/x/bch/gch (the balanced PI values) live on electrical_balanced.ACLineSegment.
- r0/x0/b0ch/g0ch (the zero-sequence PI values) live on
  short_circuit.ACLineSegment - a part module with no fields of its own
  anywhere else in this file's scope, easy to mistake for empty on a casual
  read (the shared multi-paragraph class docstring pushed the real field
  list far enough down to look like there wasn't one).
- The PerLengthImpedance FK itself lives on electrical_unbalanced.ACLineSegment,
  not electrical_balanced (which only has the scalar fields, no FK) and not
  short_circuit (which has neither).
- circuitNumber lives on both connectivity_unbalanced and construction
  (two different concerns reusing the same field name); this builder does
  not set it today - add_connectivity only wires node1/node2/phases via the
  existing generic cimtables.connectivity helpers.
- ACLineSegmentPhase (the per-conductor child used by the matrix shape to
  bind phase -> sequenceNumber -> PhaseImpedanceData.row/column) is built
  generically by cimtables.connectivity.add_phase_children, confirmed via
  /home/ande188/CIMTBL-Models/distribution/IEEE/IEEE13_CDPSM/lines.cimtbl's
  own phases= column - this builder passes `phases` straight through rather
  than reimplementing the per-conductor sequencing.
- length (Conductor's own field) and BaseVoltage (ConductingEquipment's own
  field) both live on connectivity_unbalanced only - neither exists in any
  other part module, confirmed by grepping all five. Easy to assume these
  are "generic enough to live wherever" since they're on shared base
  classes; they are not - they're still a specific part module's fields,
  same rule as every other attribute in this file.
"""

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.short_circuit as SC

from cimbuilder.builders.base import ObjectBuilder
from cimtables import connectivity, graph_write


class ACLineSegmentBuilder(ObjectBuilder):
    cim_class_name = 'ACLineSegment'

    def add_connectivity(self, line, *, node1: str, node2: str, phases: str | None = None,
                          length=None, container: object = None, BaseVoltage=None) -> list[object]:
        """Two-terminal connectivity via the existing generic
        cimtables.connectivity.add_connectivity (the non-TransformerEnd
        branch already handles an arbitrary-terminal-count Conductor; no
        terminal/node logic is reimplemented here). `phases`, if given,
        builds the ACLineSegmentPhase children via add_phase_children -
        the same per-conductor sequenceNumber ordering
        lines.cimtbl's phases= column relies on. Returns the created
        Terminals, in node1/node2 order."""
        resolved_container = container if container is not None else self.container
        terminals = connectivity.add_connectivity(
            self.network, line, node_cols={'node1': node1, 'node2': node2},
            container=resolved_container)
        if phases is not None:
            connectivity.add_phase_children(self.network, line, terminals, phases=phases)
        graph_write.set_attr(line, CN, 'length', length)
        if BaseVoltage is not None:
            target = graph_write.resolve(self.network, self.cim.BaseVoltage, BaseVoltage)
            graph_write.set_assc(line, CN, 'BaseVoltage', target)
        return terminals

    def add_electrical(self, line, *, r=None, x=None, bch=None, gch=None) -> None:
        """Shape 1 (direct balanced PI): writes directly onto the
        ACLineSegment. Part module electrical_balanced."""
        graph_write.set_attr(line, EL_BAL, 'r', r)
        graph_write.set_attr(line, EL_BAL, 'x', x)
        graph_write.set_attr(line, EL_BAL, 'bch', bch)
        graph_write.set_attr(line, EL_BAL, 'gch', gch)

    def add_short_circuit(self, line, *, r0=None, x0=None, b0ch=None, g0ch=None) -> None:
        """Shape 2 (direct zero-sequence PI): the zero-sequence counterpart
        to add_electrical. Part module short_circuit."""
        graph_write.set_attr(line, SC, 'r0', r0)
        graph_write.set_attr(line, SC, 'x0', x0)
        graph_write.set_attr(line, SC, 'b0ch', b0ch)
        graph_write.set_attr(line, SC, 'g0ch', g0ch)

    def add_per_length_impedance(self, line, *, PerLengthImpedance: str) -> object:
        """Shapes 3/4 (per-length reference): resolves a
        PerLengthSequenceImpedance (LineModel02, balanced) or
        PerLengthPhaseImpedance (LineModel03, unbalanced matrix) template by
        name and sets the one FK field both shapes share
        (electrical_unbalanced.ACLineSegment.PerLengthImpedance). Build the
        template first (via PerLengthImpedanceBuilder) or this raises, same
        ordering rule Phase 1's add_tank already established for
        TankConfiguration."""
        target = graph_write.resolve_any_subclass(self.network, self.cim.PerLengthImpedance, PerLengthImpedance)
        if target is None:
            raise ValueError(
                f"{line.name!r}: PerLengthImpedance {PerLengthImpedance!r} not found in graph "
                f"(build the template before the instance that references it)"
            )
        graph_write.set_assc(line, EL_UNBAL, 'PerLengthImpedance', target)
        return target
