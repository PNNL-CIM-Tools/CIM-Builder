import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, connectivity, graph_write

from cimbuilder.core.sort_terminals import sort_terminals_by_sequence
from cimbuilder.object_builder.object_builder import ObjectBuilder


class PowerElectronicsConnectionBuilder(ObjectBuilder):
    cim_class_name = "PowerElectronicsConnection"

    def add_connectivity(
        self,
        inverter: CN.PowerElectronicsConnection,
        *,
        node: str,
        phaseConnection: str | None = None,
        phases: str | None = None,
        # grounded: bool | None = None,
        aggregate: bool | None = None,
        EquipmentContainer: str | None = None,
        BaseVoltage: str,
    ) -> tuple[
        CN.PowerElectronicsConnection,
        CN.Terminal,
        list[CN.PowerElectronicsConnectionPhase],
    ]:
        """
        Adds base connectivity layer of terminals, base voltage, phasing
        * node: mRID of the ConnectivityNode or TopologicalNode
        * phaseConnection: string for whether wye or delta connected, D|Y|Yn|I
        * phases: phase-code string. None sets no PowerElectronicsConnectionPhase objects
        * aggregate: indicates the inverter is a modeling aggregate of multiple inverters
        * EquipmentContainer: mRID of the VoltageLevel or Feeder containing the inverter.
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore

        # graph_write.set_attr(inverter, CN, "grounded", grounded)
        if phaseConnection is not None:
            graph_write.set_attr(
                inverter,
                CN,
                "phaseConnection",
                cn.PhaseShuntConnectionKind(phaseConnection),
            )
        graph_write.set_attr(inverter, CN, "aggregate", aggregate)

        if EquipmentContainer is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=inverter,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=EquipmentContainer,
            )
        else:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=inverter,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=self.container.mRID,
            )

        if len(inverter.Terminals) != 1:
            terminals = connectivity.add_connectivity(
                network=self.network,
                equipment=inverter,
                node_cols={"node": node},
                equipment_container=inverter.EquipmentContainer,
            )
        else:
            terminals = sort_terminals_by_sequence(inverter)

        if phases is not None:
            connectivity.add_phase_children(
                self.network, inverter, terminals, phases=phases
            )

        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=inverter,
                profile_part=CN,
                association_name="BaseVoltage",
                target_class=cn.BaseVoltage,
                target_mRID=BaseVoltage,
            )
        return inverter, terminals[0], inverter.PowerElectronicsConnectionPhase

    def add_electrical(
        self,
        inverter:EL_BAL.PowerElectronicsConnection,
        *,
        ratedS: float | Qty | None = None,
        ratedU: float | Qty | None = None,
        minQ: float | Qty | None = None,
        maxQ: float | Qty | None = None,
        maxIFault: str | Qty | None = None,
    ) -> EL_BAL.PowerElectronicsConnection:
        """Adds electrical_balanced.PowerElectronicsConnection's fixed-inverter parameters.
        * ratedS: nameplate apparent power rating, float in VAr or Qty('kVAr'|'MVAr')
        * ratedU:
        * minQ:
        * maxQ:
        * maxIFault
        """

        graph_write.set_attr(inverter, EL_BAL, "ratedS", ratedS)
        graph_write.set_attr(inverter, EL_BAL, "ratedU", ratedU)
        graph_write.set_attr(inverter, EL_BAL, "minQ", minQ)
        graph_write.set_attr(inverter, EL_BAL, "maxQ", maxQ)
        graph_write.set_attr(inverter, EL_BAL, "maxIFault", maxIFault)

        return inverter

    def add_ssh(
        self,
        inverter: SSH.PowerElectronicsConnection,
        *,
        p: float | Qty | None = None,
        q: float | Qty | None = None,
        inService: bool | None = None,
    ) -> SSH.PowerElectronicsConnection:
        """
        Adds real-time p/q values from measurement or basecase.
        Use load sign convention (positive = flow out of node)
        * p: instantaneous active power, float in watts or Qty('kW'|'MW')
        * q: instantaneous reactive power, float in VArs or Qty('kVAr'|'MVAr')
        * inService: boolean, inverter is de-energized if false
        """
        graph_write.set_attr(inverter, SSH, "p", p)
        graph_write.set_attr(inverter, SSH, "q", q)
        graph_write.set_attr(inverter, SSH, "inService", inService)
        return inverter
