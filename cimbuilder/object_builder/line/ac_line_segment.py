import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.construction as CONSTR
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.short_circuit as SC
from cimtables import Qty, connectivity, graph_write, impedance

from cimbuilder.object_builder.object_builder import ObjectBuilder


class ACLineSegmentBuilder(ObjectBuilder):
    cim_class_name = "ACLineSegment"

    def add_connectivity(
        self,
        line: CN.ACLineSegment,
        *,
        node1: str,
        node2: str,
        phases: str | None = None,
        length: float | Qty | None = None,
        EquipmentContainer: str | None = None,
        BaseVoltage: str | None = None,
    ) -> tuple[CN.ACLineSegment, list[CN.Terminal], list[CN.ACLineSegmentPhase]]:
        """
        Adds base connectivity layer of terminals, base voltage, phasing
        * node1: mRID of the "from" ConnectivityNode or TopologicalNode
        * node2: mRID of the "to" ConnectivityNode or Topological Node
        * phases: phase-code string in conductor order (e.g. CABN). None sets
        * length: physical length, float in meters or Qty('mi'|'ft'|etc)
        * EquipmentContainer: mRID of the Line or Feeder containing the line. New mRID will create a new Line container
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore

        if EquipmentContainer is not None:
            if not self.network.find_by_mRID(EquipmentContainer):
                container = cn.Line(mRID=EquipmentContainer)
                self.network.add_to_graph(container)

            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=line,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=EquipmentContainer,
            )
        else:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=line,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=self.container.mRID,
            )
        if len(line.Terminals) != 2:
            terminals = connectivity.add_connectivity(
                network=self.network,
                equipment=line,
                node_cols={"node1": node1, "node2": node2},
                equipment_container=line.EquipmentContainer,
            )
        if phases is not None:
            line_phs: list[CN.ACLineSegmentPhase] = connectivity.add_phase_children(
                self.network, line, terminals, phases=phases
            )  # type:ignore

        graph_write.set_attr(line, CN, "length", length)
        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(
                network=self.network, 
                source_object=line,
                profile_part=CN,
                association_name="BaseVoltage",
                target_class=cn.BaseVoltage,
                target_mRID= BaseVoltage,
            )
        return line, terminals, line_phs

    def add_electrical(
        self, line, *, r=None, x=None, bch=None, gch=None
    ) -> EL_BAL.ACLineSegment:
        """
        Adds positive sequence three-phase balanced impedance values:
        * r: positive sequence resistance, float in ohm or Qty('ohm'|'pu')
        * x: positive sequence reactance, float in ohm or Qty('ohm'|'pu')
        * bch: positive sequence shunt susceptance, float in siemens or Qty('S'|'pu')
        * gch: positive sequence shunt conductance, float in siemens or Qty('S'|'pu')
        """
        z_base = impedance.z_base(line, [], self.network.base_power)
        graph_write.set_attr(line, EL_BAL, "r", r, z_base=z_base)
        graph_write.set_attr(line, EL_BAL, "x", x, z_base=z_base)
        graph_write.set_attr(line, EL_BAL, "bch", bch, z_base=z_base)
        graph_write.set_attr(line, EL_BAL, "gch", gch, z_base=z_base)
        return line

    def add_short_circuit(
        self, line, *, r0=None, x0=None, b0ch=None, g0ch=None
    ) -> SC.ACLineSegment:
        """
        Adds zero-sequence short-circuit impedances to the line
        * r0: zero sequence resistance, float in ohm or Qty('ohm'|'pu')
        * x0: zero sequence reactance, float in ohm or Qty('ohm'|'pu')
        * b0ch: zero sequence shunt susceptance, float in siemens or Qty('S'|'pu')
        * g0ch: zero sequence shunt conductance, float in siemens or Qty('S'|'pu')
        """
        z_base = impedance.z_base(line, [], self.network.base_power)
        graph_write.set_attr(line, SC, "r0", r0, z_base=z_base)
        graph_write.set_attr(line, SC, "x0", x0, z_base=z_base)
        graph_write.set_attr(line, SC, "b0ch", b0ch, z_base=z_base)
        graph_write.set_attr(line, SC, "g0ch", g0ch, z_base=z_base)
        return line

    def add_per_length_impedance(
        self, line, *, PerLengthImpedance: str
    ) -> EL_UNBAL.ACLineSegment:
        """
        Associates `line` with a PerLengthSequenceImpedance or PerLengthPhaseImpedance
        specfic to this line. Reusable linecode style impedances use WireConfiguration
        * PerLengthImpedance: mRID string of target impedance class
        """
        el_unbal: EL_UNBAL = self.cim  # type: ignore
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=line,
            profile_part=EL_UNBAL,
            association_name="PerLengthImpedance",
            target_class=el_unbal.PerLengthImpedance,
            target_mRID=PerLengthImpedance,
        )
        return line

    def add_wire_configuration(self, line, *, WireConfiguration: str) -> object:
        """
        Associates `line` with an existing WireConfiguration template
        * WireConfiguration: mRID string of the target WireConfiguration
        """
        cnst: CONSTR = self.cim  # type: ignore
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=line,
            profile_part=CONSTR,
            association_name="WireConfiguration",
            target_class=cnst.WireConfiguration,
            target_mRID=WireConfiguration,
        )
        return line

    def add_multi_circuit_group(
        self, line, *, circuitNumber=None, MultiCircuitGroup
    ) -> CN.ACLineSegment:
        """
        * circuitNumber: integer denotes adjacent lines, default None
        """
        cn: CN = self.cim  # type: ignore
        graph_write.set_attr(line, CN, "circuitNumber", circuitNumber)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=line,
            profile_part=CN,
            association_name="MultiCircuitGroup",
            target_class=cn.MultiCircuitGroup,
            target_mRID=MultiCircuitGroup,
        )
        return line
