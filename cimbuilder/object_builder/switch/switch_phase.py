import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str

class SwitchPhaseBuilder(ObjectBuilder):
    cim_class_name = "SwitchPhase"

    def add_connectivity(
        self,
        switch_phase: CN.SwitchPhase,
        *,
        Switch: mRID,
        phaseSide1: str,
        phaseSide2: str,
        normalOpen: bool | None = None,
    ) -> CN.SwitchPhase:
        """
        Add connectivity and phasing information
        * sequenceNumber: integer for indexing of wire position / impedance matrix
        * phaseSide1: Single phase kind string, A|B|C|N|s1|s2|X|Y
        * phaseSide2: Single phase kind string, A|B|C|N|s1|s2|X|Y
        """
        cn: CN = self.cim  # type: ignore
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=switch_phase,
            profile_part=CN,
            association_name="Switch",
            target_class=cn.Switch,
            target_mRID=Switch,
        )
        graph_write.set_attr(
            switch_phase, CN, "phaseSide1", cn.SinglePhaseKind(phaseSide1)
        )
        graph_write.set_attr(
            switch_phase, CN, "phaseSide2", cn.SinglePhaseKind(phaseSide2)
        )
        graph_write.set_attr(switch_phase, CN, "normalOpen", normalOpen)
        return switch_phase

    def add_electrical(
        self,
        switch_phase: EL_UNBAL.SwitchPhase,
        *,
        ratedCurrent: float | Qty | None = None,
    ) -> EL_UNBAL.SwitchPhase:
        """
        Adds single-phase electrical parameters for the switch
        * ratedCurrent: max normal operating current, float in amps or Qty('A')
        """
        graph_write.set_attr(switch_phase, EL_UNBAL, "ratedCurrent", ratedCurrent)
        return switch_phase

    def add_ssh(self, switch_phase: SSH.SwitchPhase, *, open: bool) -> SSH.SwitchPhase:
        """
        Adds real-time switch status from measurement or basecase.
        * open: boolean, indicates single-phase switch open/closed status
        """
        graph_write.set_attr(switch_phase, SSH, "open", open)
        return switch_phase
