import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, connectivity, graph_write

from cimbuilder.core.sort_terminals import sort_terminals_by_sequence
from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str

class EnergyConsumerBuilder(ObjectBuilder):
    cim_class_name = "EnergyConsumer"

    def add_connectivity(
        self,
        load: CN.EnergyConsumer,
        *,
        node: mRID,
        phaseConnection: str | None = None,
        phases: str | None = None,
        grounded: bool | None = None,
        customerCount: int | None = None,
        aggregate: bool | None = None,
        EquipmentContainer: mRID | None = None,
        BaseVoltage: mRID,
    ) -> tuple[CN.EnergyConsumer, CN.Terminal, list[CN.EnergyConsumerPhase]]:
        """
        Adds base connectivity layer of terminals, base voltage, phasing
        * node: mRID of the ConnectivityNode or TopologicalNode
        * phaseConnection: string for whether wye or delta connected, D|Y|Yn|I
        * phases: phase-code string in conductor order (e.g. CABN). None sets no EnergyConsumerPhase objects
        * grounded: boolean, load is grounded if true
        * customerCount: the number of metered customers aggregated into the load
        * aggregate: indicates the load is an aggregate of multiple customers
        * EquipmentContainer: mRID of the VoltageLevel or Feeder containing the load.
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore

        graph_write.set_attr(load, CN, "customerCount", customerCount)
        graph_write.set_attr(load, CN, "grounded", grounded)
        if phaseConnection is not None:
            graph_write.set_attr(
                load, CN, "phaseConnection", cn.PhaseShuntConnectionKind(phaseConnection)
            )
        graph_write.set_attr(load, CN, "aggregate", aggregate)

        if EquipmentContainer is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=load,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=EquipmentContainer,
            )
        else:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=load,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=self.container.mRID,
            )
            
        if len(load.Terminals) != 1:
            terminals = connectivity.add_connectivity(
                network=self.network,
                equipment=load,
                node_cols={"node": node},
                equipment_container=load.EquipmentContainer,
            )
        else:
            terminals = sort_terminals_by_sequence(load)

        if phases is not None:
            connectivity.add_phase_children(self.network, load, terminals, phases=phases)

        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=load,
                profile_part=CN,
                association_name="BaseVoltage",
                target_class=cn.BaseVoltage,
                target_mRID=BaseVoltage,
            )
        return load, terminals[0], load.EnergyConsumerPhase

    def add_electrical(
        self,
        load: EL_BAL.EnergyConsumer,
        *,
        minP: float | Qty | None = None,
        maxP: float | Qty | None = None,
        pfixed: float | Qty | None = None,
        qfixed: float | Qty | None = None,
        pfixedPct: float | None = None,
        qfixedPct: float | None = None,
        LoadResponse: mRID | None = None,
    ) -> EL_BAL.EnergyConsumer:
        """Adds electrical_balanced.EnergyConsumer's fixed-load parameters.
        * minP: minimum power demand, float in watts or Qty('kW')
        * maxP: 
        * pfixed: active power of the load that is a fixed quantity and does not vary as load group value varies
        * qfixed: reactive power of the load that is a fixed quantity and does not vary as load group value varies
        * pfixedPct: percentage of load group fixed active power. Used to represent the time-varying component
        * qfixedPct: percentage of load group fixed reactive power. Used to represent the time-varying component.
        * LoadResponse: mRID string of the LoadResponseCharacteristic ZIP fraction
        """
        el_bal: EL_BAL = self.cim  # type: ignore
        graph_write.set_attr(load, EL_BAL, "minP", minP)
        graph_write.set_attr(load, EL_BAL, "maxP", maxP)
        graph_write.set_attr(load, EL_BAL, "pfixed", pfixed)
        graph_write.set_attr(load, EL_BAL, "qfixed", qfixed)
        graph_write.set_attr(load, EL_BAL, "pfixedPct", pfixedPct)
        graph_write.set_attr(load, EL_BAL, "qfixedPct", qfixedPct)

        if LoadResponse is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=load,
                profile_part=EL_BAL,
                association_name="LoadResponse",
                target_class=el_bal.LoadResponseCharacteristic,
                target_mRID=LoadResponse,
            )
        return load

    def add_ssh(
        self,
        load: SSH.EnergyConsumer,
        *,
        p: float | Qty | None = None,
        q: float | Qty | None = None,
        inService: bool | None = None,
    ) -> SSH.EnergyConsumer:
        """
        Adds real-time p/q values from measurement or basecase.
        Use load sign convention (positive = flow out of node)
        * p: instantaneous active power, float in watts or Qty('kW'|'MW')
        * q: instantaneous reactive power, float in VArs or Qty('kVAr'|'MVAr')
        * inService: boolean, load is de-energized if false
        """
        graph_write.set_attr(load, SSH, "p", p)
        graph_write.set_attr(load, SSH, "q", q)
        graph_write.set_attr(load, SSH, "inService", inService)
        return load
