from typing import Optional

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.construction as CONST
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.short_circuit as SC

from cimbuilder.object_builder.object_builder import ObjectBuilder
from cimtables import connectivity, graph_write, impedance
from cimtables.units import Qty

class ACLineSegmentBuilder(ObjectBuilder):
    cim_class_name = 'ACLineSegment'

    def add_connectivity(self, line, *, node1: str, node2: str, phases: str | None = None,
                    length=None, circuitNumber=None, 
                    EquipmentContainer=None, BaseVoltage=None) -> None:
        """
        Adds base connectivity layer of terminals, base voltage, phasing
        * node1: mRID of the "from" ConnectivityNode or TopologicalNode
        * node2: mRID of the "to" ConnectivityNode or Topological Node
        * phases: phase-code string in conductor order (e.g. CABN). None sets 
        * length: physical length, float in meters or Qty('mi'|'ft'|etc)
        * circuitNumber: integer denotes adjacent parallel lines, default None
        * EquipmentContainer: mRID of the Line or Feeder container
        * BaseVoltage: mRID string of the BaseVoltage

        Returns the Terminals created for node1/node2, in that order
        (sequenceNumber 1, 2).
        """
        if EquipmentContainer is not None:
            graph_write.set_assc_from_mrid(self.network, line, CN, 'EquipmentContainer', 
                                           self.cim.EquipmentContainer, EquipmentContainer)
        else:
            graph_write.set_assc_from_mrid(self.network, line, CN, 'EquipmentContainer', 
                                           self.cim.EquipmentContainer, self.container.mRID)
            
        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(self.network, line, CN, 'BaseVoltage', self.cim.BaseVoltage, BaseVoltage)

        terminals = connectivity.add_connectivity(
            self.network, line, node_cols={'node1': node1, 'node2': node2},
            container=line.EquipmentContainer)
        
        if phases is not None:
            connectivity.add_phase_children(self.network, line, terminals, phases=phases)
        
        graph_write.set_attr(line, CN, 'length', length)
        graph_write.set_attr(line, CN, 'circuitNumber', circuitNumber)


    def add_electrical(self, line, *, r=None, x=None, bch=None, gch=None) -> None:
        """
        Adds positive sequence three-phase balanced impedance values:
        * r: positive sequence resistance, float in ohm or Qty('ohm'|'pu')
        * x: positive sequence reactance, float in ohm or Qty('ohm'|'pu')
        * bch: positive sequence shunt susceptance, float in siemens or Qty('S'|'pu')
        * gch: positive sequence shunt conductance, float in siemens or Qty('S'|'pu')
        """
        z_base = impedance.z_base(line, [], self.network.base_power)
        graph_write.set_attr(line, EL_BAL, 'r', r, z_base=z_base)
        graph_write.set_attr(line, EL_BAL, 'x', x, z_base=z_base)
        graph_write.set_attr(line, EL_BAL, 'bch', bch, z_base=z_base)
        graph_write.set_attr(line, EL_BAL, 'gch', gch, z_base=z_base)

    def add_short_circuit(self, line, *, r0=None, x0=None, b0ch=None, g0ch=None) -> None:
        """
        Adds zero-sequence short-circuit impedances to the line
        * r0: zero sequence resistance, float in ohm or Qty('ohm'|'pu')
        * x0: zero sequence reactance, float in ohm or Qty('ohm'|'pu')
        * b0ch: zero sequence shunt susceptance, float in siemens or Qty('S'|'pu')
        * g0ch: zero sequence shunt conductance, float in siemens or Qty('S'|'pu')
        """
        z_base = impedance.z_base(line, [], self.network.base_power)

        graph_write.set_attr(line, SC, 'r0', r0, z_base=z_base)
        graph_write.set_attr(line, SC, 'x0', x0, z_base=z_base)
        graph_write.set_attr(line, SC, 'b0ch', b0ch, z_base=z_base)
        graph_write.set_attr(line, SC, 'g0ch', g0ch, z_base=z_base)

    def add_per_length_impedance(self, line, *, PerLengthImpedance: str) -> object:
        """
        Associates `line` with a PerLengthSequenceImpedance or PerLengthPhaseImpedance
        specfic to this line. Reusable linecode style impedances use WireConfiguration
        * PerLengthImpedance: mRID string of target impedance class
        """
        target = graph_write.set_assc_from_mrid(
            self.network, line, EL_UNBAL, 'PerLengthImpedance', self.cim.PerLengthImpedance, PerLengthImpedance)
        return target

    def add_wire_configuration(self, line, *, WireConfiguration: str) -> object:
        """
        Associates `line` with an existing WireConfiguration template
        * WireConfiguration: mRID string of the target WireConfiguration
        """
        target = graph_write.set_assc_from_mrid(
            self.network, line, CONST, 'WireConfiguration', self.cim.WireConfiguration, WireConfiguration)
        return target
