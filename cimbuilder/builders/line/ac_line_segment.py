"""
"""

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.construction as CONST
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.short_circuit as SC

from cimbuilder.builders.base import ObjectBuilder
from cimtables import connectivity, graph_write


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
        * r: resolves to Resistance (ohm, SI base) - e.g. Qty(0.3, 'ohm').
        * x: resolves to Reactance (ohm, SI base).
        * bch: resolves to Susceptance (siemens, SI base).
        * gch: resolves to Conductance (siemens, SI base).
        A bare number for any of these is stored unconverted via plain
        setattr, not wrapped in the CIMUnit type. A relative Qty (pu/percent)
        would need a z_base to convert to ohms, but this method never passes
        `z_base` to set_attr, so a pu/percent r or x raises ValueError.
        """
        graph_write.set_attr(line, EL_BAL, 'r', r)
        graph_write.set_attr(line, EL_BAL, 'x', x)
        graph_write.set_attr(line, EL_BAL, 'bch', bch)
        graph_write.set_attr(line, EL_BAL, 'gch', gch)

    def add_short_circuit(self, line, *, r0=None, x0=None, b0ch=None, g0ch=None) -> None:
        """
        Adds zero-sequence short-circuit parameters (short_circuit.ACLineSegment),
        the short_circuit-profile counterpart to add_electrical's positive-sequence set.
        All four are Qtys, same rules as add_electrical:
        * r0: resolves to Resistance (ohm, SI base).
        * x0: resolves to Reactance (ohm, SI base).
        * b0ch: resolves to Susceptance (siemens, SI base).
        * g0ch: resolves to Conductance (siemens, SI base).
        No `z_base` is passed here either, so a pu/percent r0 or x0 raises
        ValueError.
        """
        graph_write.set_attr(line, SC, 'r0', r0)
        graph_write.set_attr(line, SC, 'x0', x0)
        graph_write.set_attr(line, SC, 'b0ch', b0ch)
        graph_write.set_attr(line, SC, 'g0ch', g0ch)

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
        Associates `line` with an existing wire-geometry template
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
