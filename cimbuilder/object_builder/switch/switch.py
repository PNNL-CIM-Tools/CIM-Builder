import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, connectivity, graph_write

from cimbuilder.core.sort_terminals import sort_terminals_by_sequence
from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str

class SwitchBuilder(ObjectBuilder):
    cim_class_name = "Switch"

    def add_connectivity(
        self,
        switch: CN.Switch,
        *,
        node1: mRID,
        node2: mRID,
        phases: str | None = None,
        phaseSide1: str | None = None,
        phaseSide2: str | None = None,
        normalOpen: bool | None = None,
        retained: bool | None = None,
        areaBoundary: bool | None = None,
        topologicalUsage: str | None = None,
        EquipmentContainer: mRID | None = None,
        BaseVoltage: mRID,
    ) -> tuple[CN.Switch, list[CN.Terminal], list[CN.SwitchPhase]]:
        """
        Adds connectivity_unbalanced profile layer: terminals/nodes,
        per-side phasing, base voltage, and switch status flags.
        * node1: mRID of the "from" ConnectivityNode or TopologicalNode
        * node2: mRID of the "from" ConnectivityNode or TopologicalNode
        * phases: phase string, same on both sides (e.g. 'ABC'); one SwitchPhase per phase
        * phaseSide1: side 1 phasing when the sides differ (e.g. 'AB' -> 'AC')
        * phaseSide2: side 2 phasing when the sides differ (e.g. 'AB' -> 'AC')
        * normalOpen: boolean, indicates normal open
        * retained: boolean, indicates switch must be preserved in bus-branch topology reduction
        * areaBoundary: boolean, indicates boundary of a ConnectedArea
        * topologicalUsage: string, acrossArea|bypass|busTie
        * EquipmentContainer: mRID of the VoltageLevel or Feeder containing the switch
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore

        if EquipmentContainer is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=switch,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=EquipmentContainer,
            )
        else:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=switch,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=self.container.mRID,
            )

        if len(switch.Terminals) != 2:
            terminals = connectivity.add_connectivity(
                network=self.network,
                equipment=switch,
                node_cols={"node1": node1, "node2": node2},
                equipment_container=switch.EquipmentContainer,
            )
        else:
            terminals = sort_terminals_by_sequence(switch)

        if phases is not None or phaseSide1 is not None or phaseSide2 is not None:
            connectivity.add_phase_children(
                self.network,
                switch,
                terminals,
                phases=phases,
                phaseSide1=phaseSide1,
                phaseSide2=phaseSide2,
            )

        graph_write.set_attr(switch, CN, "normalOpen", normalOpen)
        graph_write.set_attr(switch, CN, "retained", retained)
        graph_write.set_attr(switch, CN, "areaBoundary", areaBoundary)
        if topologicalUsage is not None:
            graph_write.set_attr(
                source_object=switch,
                profile_part=CN,
                attribute_name="topologicalUsage",
                attribute_value=cn.TopologicalUsageKind(topologicalUsage),
            )
        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=switch,
                profile_part=CN,
                association_name="BaseVoltage",
                target_class=cn.BaseVoltage,
                target_mRID=BaseVoltage,
            )

        return switch, terminals, switch.SwitchPhase

    def add_electrical(
        self,
        switch: EL_BAL.Switch,
        *,
        ratedCurrent: float | Qty | None = None,
        gangOperated: bool | None = None,
        motorOperated: bool | None = None,
        remotelyOperated: bool | None = None,
        loadBreak: bool | None = None,
    ) -> EL_BAL.Switch:
        """
        Adds balanced electrical parameters for the switch
        * ratedCurrent: max normal operating current, float in amps or Qty('A')
        * gangOperated: boolean, all phases operate together if true
        * motorOperated: boolean, operated by motor (not hand-crank) if true
        * remotelyOperated: boolean, can be operated by SCADA if true
        * loadBreak: boolean, can be opened under load (has vacuum/SF6/arc chute) if true
        """
        graph_write.set_attr(switch, EL_BAL, "ratedCurrent", ratedCurrent)
        graph_write.set_attr(switch, EL_BAL, "gangOperated", gangOperated)
        graph_write.set_attr(switch, EL_BAL, "motorOperated", motorOperated)
        graph_write.set_attr(switch, EL_BAL, "remotelyOperated", remotelyOperated)
        graph_write.set_attr(switch, EL_BAL, "loadBreak", loadBreak)
        return switch

    def add_ssh(
        self,
        switch: SSH.Switch,
        *,
        inService: bool | None = None,
        open: bool | None = None,
    ) -> SSH.Switch:
        """
        Adds real-time switch status from measurement or basecase.
        * open: boolean, indicates switch open/closed status
        * inService: boolean, switch is de-energized/bypassed if false
        """
        graph_write.set_attr(switch, SSH, "open", open)
        graph_write.set_attr(switch, SSH, "inService", inService)
        return switch


class FuseBuilder(SwitchBuilder):
    cim_class_name = "Fuse"


class SectionaliserBuilder(SwitchBuilder):
    cim_class_name = "Sectionaliser"


class DisconnectorBuilder(SwitchBuilder):
    cim_class_name = "Disconnector"


class ServiceDisconnectBuilder(DisconnectorBuilder):
    cim_class_name = "ServiceDisconnect"


class ElbowBuilder(DisconnectorBuilder):
    cim_class_name = "Elbow"


class AirBreakSwitchBuilder(DisconnectorBuilder):
    cim_class_name = "AirBreakSwitch"


class HookstickSwitchBuilder(DisconnectorBuilder):
    cim_class_name = "HookstickSwitch"
