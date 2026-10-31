"""
"""

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.construction as CONST
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.short_circuit as SC

from cimbuilder.builders.base import ObjectBuilder
from cimtables import connectivity, graph_write, impedance


def _system_base(self: 'ACLineSegmentBuilder', line) -> tuple[float, float] | None:
    """(z_base ohms, y_base siemens) for a line's r/x/r0/x0/bch/gch/b0ch/g0ch,
    from CIMG_SYSTEM_MVA_BASE (the PSS/E-RAW-SBASE equivalent) paired with
    `line`'s OWN BaseVoltage - ACLineSegment has no self-contained rating
    pair of its own (no ratedS/ratedU anywhere in this profile), so this is
    a different base source from TransformerWinding/PowerTransformerEnd's
    cimtables.impedance.resolve_winding_z_base/resolve_winding_y_base. Both
    bases come from the SAME rating pair (y_base = 1/z_base), matching PSS/E
    RAW's convention of one SBASE for both impedance and admittance.

    None if either self.system_mva (set once in ObjectBuilder.__init__ from
    CIMG_SYSTEM_MVA_BASE) or line.BaseVoltage is missing - set_attr then
    fails fast if a relative value actually needed it. `line.BaseVoltage`
    must already be resolved (via add_connectivity) before this is useful."""
    if self.system_mva is None or line.BaseVoltage is None:
        return None
    rated_u_v = line.BaseVoltage.nominalVoltage.to('V')
    rated_s_va = self.system_mva * 1e6
    return impedance.z_base(rated_u_v, rated_s_va), impedance.y_base(rated_u_v, rated_s_va)


class ACLineSegmentBuilder(ObjectBuilder):
    cim_class_name = 'ACLineSegment'

    def add_connectivity(self, line, *, node1: str, node2: str, phases: str | None = None,
                          length=None, circuitNumber=None,
                          EquipmentContainer: object = None, BaseVoltage=None) -> list[object]:
        """
        Adds connectivity_unbalanced profile layer: terminals/nodes, phasing,
        length, circuit number, and base voltage.
        * node1: mRID of the "from" ConnectivityNode/TopologicalNode. Must
          already exist in the graph, or is auto-vivified (an empty node
          object with just that mRID) if not found - this is NOT a
          required-FK-raises-if-missing lookup like the mRID params below.
        * node2: same as node1, for the "to" end.
        * phases: phase-code string in conductor order (e.g. 'ABC', 'CB',
          's1s2') - each character/token becomes one ACLineSegmentPhase child
          (via connectivity.add_phase_children), and both terminals get this
          same PhaseCode.
        * length: a Qty (e.g. Qty(5, 'mile'), Qty(100, 'm')) - set_attr
          resolves it to connectivity_unbalanced.Length (meters, SI base). A
          bare number is NOT unit-converted (stored via plain setattr) and
          should not be passed.
        * circuitNumber: plain int, set as-is (no unit wrapping).
        * EquipmentContainer: a live container object (e.g. a Feeder/Line),
          NOT an mRID string - falls back to `self.container` if omitted.
          Passed straight through to connectivity.add_connectivity, which
          sets it as the line's EquipmentContainer and propagates it onto
          any newly-vivified node.
        * BaseVoltage: mRID string of an existing BaseVoltage; resolved via
          set_assc_from_mrid, which raises ValueError if it's not already in
          the graph.

        Returns the Terminals created for node1/node2, in that order
        (sequenceNumber 1, 2).
        """
        

        resolved_container = EquipmentContainer if EquipmentContainer is not None else self.container
        terminals = connectivity.add_connectivity(
            self.network, line, node_cols={'node1': node1, 'node2': node2},
            container=resolved_container)
        if phases is not None:
            connectivity.add_phase_children(self.network, line, terminals, phases=phases)
        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(self.network, line, CN, 'BaseVoltage', self.cim.BaseVoltage, BaseVoltage)
        
        graph_write.set_attr(line, CN, 'length', length)
        graph_write.set_attr(line, CN, 'circuitNumber', circuitNumber)
        return terminals

    def add_electrical(self, line, *, r=None, x=None, bch=None, gch=None) -> None:
        """
        Adds positive-sequence balanced electrical parameters (electrical_balanced.ACLineSegment).
        All four are Qtys resolved to the line's whole length (not per-length):
        * r: a Qty resolved to Resistance (ohm, SI base) if absolute (e.g.
          Qty(0.3, 'ohm')), or converted to ohms against a z_base derived
          from CIMG_SYSTEM_MVA_BASE + `line`'s own BaseVoltage if relative
          (pu only - e.g. Qty(0.05, 'pu'); percent/%Z is a nameplate-
          impedance convention for transformer tanks, not how line
          impedance is expressed on a system base, though a percent Qty is
          not rejected here). Requires `line.BaseVoltage` already resolved
          (via add_connectivity) and CIMG_SYSTEM_MVA_BASE set, or raises
          ValueError naming both prerequisites.
        * x: a Qty resolved to Reactance (ohm, SI base); same relative-Qty
          rule and z_base source as r.
        * bch: a Qty resolved to Susceptance (siemens, SI base) if absolute,
          or converted to siemens against a y_base derived from the SAME
          CIMG_SYSTEM_MVA_BASE + BaseVoltage as r/x's z_base (y_base =
          1/z_base) if relative (pu) - PSS/E RAW convention: one SBASE for
          both a branch's impedance and its charging susceptance. Same
          prerequisites/ValueError as r.
        * gch: a Qty resolved to Conductance (siemens, SI base); same
          relative-Qty rule and y_base source as bch.
        A bare number for any of these is stored unconverted via plain
        setattr, not wrapped in the CIMUnit type.
        """
        base = _system_base(self, line) if (r is not None or x is not None or bch is not None or gch is not None) else None
        z_base, y_base = base if base is not None else (None, None)
        graph_write.set_attr(line, EL_BAL, 'r', r, z_base=z_base)
        graph_write.set_attr(line, EL_BAL, 'x', x, z_base=z_base)
        graph_write.set_attr(line, EL_BAL, 'bch', bch, y_base=y_base)
        graph_write.set_attr(line, EL_BAL, 'gch', gch, y_base=y_base)

    def add_short_circuit(self, line, *, r0=None, x0=None, b0ch=None, g0ch=None) -> None:
        """
        Adds zero-sequence short-circuit parameters (short_circuit.ACLineSegment),
        the short_circuit-profile counterpart to add_electrical's positive-sequence set.
        All four are Qtys, same rules as add_electrical:
        * r0: resolves to Resistance (ohm, SI base) if absolute, or
          converted to ohms against the SAME system-base z_base as
          add_electrical's r/x (CIMG_SYSTEM_MVA_BASE + `line`'s own
          BaseVoltage) if relative (pu) - zero-sequence line impedance is
          conventionally expressed on the same system base as
          positive-sequence, unlike transformers where the mesh-vs-winding
          tier genuinely differs. Same prerequisites/ValueError as r.
        * x0: resolves to Reactance (ohm, SI base); same relative-Qty rule
          and z_base source as r0.
        * b0ch: a Qty resolved to Susceptance (siemens, SI base) if
          absolute, or converted to siemens against the SAME system-base
          y_base as add_electrical's bch/gch if relative (pu). Same
          prerequisites/ValueError as r0.
        * g0ch: a Qty resolved to Conductance (siemens, SI base); same
          relative-Qty rule and y_base source as b0ch.
        """
        base = _system_base(self, line) if (r0 is not None or x0 is not None or b0ch is not None or g0ch is not None) else None
        z_base, y_base = base if base is not None else (None, None)
        graph_write.set_attr(line, SC, 'r0', r0, z_base=z_base)
        graph_write.set_attr(line, SC, 'x0', x0, z_base=z_base)
        graph_write.set_attr(line, SC, 'b0ch', b0ch, y_base=y_base)
        graph_write.set_attr(line, SC, 'g0ch', g0ch, y_base=y_base)

    def add_per_length_impedance(self, line, *, PerLengthImpedance: str) -> object:
        """
        Associates `line` with an existing per-length template
        (electrical_unbalanced.ACLineSegment's PerLengthImpedance FK).
        * PerLengthImpedance: mRID string of an existing
          PerLengthSequenceImpedance or PerLengthPhaseImpedance (built
          earlier, e.g. via PerLengthSequenceImpedanceBuilder/
          PerLengthPhaseImpedanceBuilder). Resolved via set_assc_from_mrid,
          which raises ValueError if that mRID isn't already in the graph.

        Returns the resolved template object.
        """
        target = graph_write.set_assc_from_mrid(
            self.network, line, EL_UNBAL, 'PerLengthImpedance', self.cim.PerLengthImpedance, PerLengthImpedance)
        return target

    def add_wire_configuration(self, line, *, WireConfiguration: str) -> object:
        """
        Associates `line` with an existing WireConfiguration template
        (construction.ACLineSegment's WireConfiguration FK).
        * WireConfiguration: mRID string of an existing WireConfiguration
          (built earlier via WireConfigurationBuilder). Resolved via
          set_assc_from_mrid, which raises ValueError if that mRID isn't
          already in the graph.

        Returns the resolved WireConfiguration object.
        """
        target = graph_write.set_assc_from_mrid(
            self.network, line, CONST, 'WireConfiguration', self.cim.WireConfiguration, WireConfiguration)
        return target
