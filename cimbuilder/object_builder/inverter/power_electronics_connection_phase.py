import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class PowerElectronicsConnectionPhaseBuilder(ObjectBuilder):
    cim_class_name = "PowerElectronicsConnectionPhase"

    def add_connectivity(
        self,
        inverter_phs: CN.PowerElectronicsConnectionPhase,
        phase: str,
        PowerElectronicsConnection: str,
    ) -> CN.PowerElectronicsConnectionPhase:
        """
        Add connectivity and phasing information
        * phase: Single phase kind, A|B|C|N|s1|s2|X|Y
        """
        cn: CN = self.cim  # type: ignore

        graph_write.set_attr(inverter_phs, CN, "phase", phase)
        if PowerElectronicsConnection is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=inverter_phs,
                profile_part=CN,
                association_name="PowerElectronicsConnection",
                target_class=cn.PowerElectronicsConnection,
                target_mRID=PowerElectronicsConnection,
            )
        return inverter_phs

    def add_ssh(
        self,
        inverter_phs: SSH.PowerElectronicsConnectionPhase,
        *,
        p: float | Qty | None = None,
        q: float | Qty | None = None,
    ) -> SSH.PowerElectronicsConnectionPhase:
        """
        Adds real-time p/q values from measurement or basecase.
        Use load sign convention (positive = flow out of node)
        * p: instantaneous active power, float in watts or Qty('kW'|'MW')
        * q: instantaneous reactive power, float in VArs or Qty('kVAr'|'MVAr')
        """
        graph_write.set_attr(inverter_phs, SSH, "p", p)
        graph_write.set_attr(inverter_phs, SSH, "q", q)
        return inverter_phs