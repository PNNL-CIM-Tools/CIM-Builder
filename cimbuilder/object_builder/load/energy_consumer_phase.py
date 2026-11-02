import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class EnergyConsumerPhaseBuilder(ObjectBuilder):
    cim_class_name = "EnergyConsumerPhase"

    def add_connectivity(
        self,
        load_phs: CN.EnergyConsumerPhase,
        phase: str,
        EnergyConsumer: str,
    ) -> CN.EnergyConsumerPhase:
        """
        Add connectivity and phasing information
        * phase: Single phase kind, A|B|C|N|s1|s2|X|Y
        """
        cn: CN = self.cim  # type: ignore

        graph_write.set_attr(load_phs, CN, "phase", phase)
        if EnergyConsumer is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=load_phs,
                profile_part=CN,
                association_name="EnergyConsumer",
                target_class=cn.EnergyConsumer,
                target_mRID=EnergyConsumer,
            )
        return load_phs

    def add_electrical(
        self,
        load_phs,
        *,
        pfixed: float | Qty | None = None,
        qfixed: float | Qty | None = None,
        pfixedPct: float | None = None,
        qfixedPct: float | None = None,
        LoadResponse: str | None = None,
    ) -> EL_UNBAL.EnergyConsumerPhase:
        """Adds electrical_balanced.EnergyConsumer's fixed-load parameters.
        * pfixed: active power of the load that is a fixed quantity and does not vary as load group value varies
        * qfixed: reactive power of the load that is a fixed quantity and does not vary as load group value varies
        * pfixedPct: percentage of load group fixed active power. Used to represent the time-varying component
        * qfixedPct: percentage of load group fixed reactive power. Used to represent the time-varying component.
        * LoadResponse: mRID string of the LoadResponseCharacteristic ZIP fraction
        """
        el_bal: EL_UNBAL = self.cim  # type: ignore
        graph_write.set_attr(load_phs, EL_UNBAL, "pfixed", pfixed)
        graph_write.set_attr(load_phs, EL_UNBAL, "qfixed", qfixed)
        graph_write.set_attr(load_phs, EL_UNBAL, "pfixedPct", pfixedPct)
        graph_write.set_attr(load_phs, EL_UNBAL, "qfixedPct", qfixedPct)

        if LoadResponse is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=load_phs,
                profile_part=EL_UNBAL,
                association_name="LoadResponse",
                target_class=el_bal.LoadResponseCharacteristic,
                target_mRID=LoadResponse,
            )
        return load_phs

    def add_ssh(
        self,
        load_phs: SSH.EnergyConsumerPhase,
        *,
        p: float | Qty | None = None,
        q: float | Qty | None = None,
    ) -> SSH.EnergyConsumerPhase:
        """
        Adds real-time p/q values from measurement or basecase.
        Use load sign convention (positive = flow out of node)
        * p: instantaneous active power, float in watts or Qty('kW'|'MW')
        * q: instantaneous reactive power, float in VArs or Qty('kVAr'|'MVAr')
        """
        graph_write.set_attr(load_phs, SSH, "p", p)
        graph_write.set_attr(load_phs, SSH, "q", q)
        return load_phs