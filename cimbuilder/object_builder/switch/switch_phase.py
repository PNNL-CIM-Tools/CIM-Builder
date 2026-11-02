"""SwitchPhaseBuilder: per-phase override of a multi-phase Switch, for the
case a switch is wired to a different SinglePhaseKind on each side (e.g.
phase A on side 1, phase B on side 2 - an open-phase/cross-connected tap),
which the generic cimtables.connectivity.add_phase_children path cannot
express (it always sets phaseSide1 == phaseSide2 == the same token, one
token per phases= character).

Field locations confirmed directly against the installed cimprofiles
package:
- phaseSide1/phaseSide2/normalOpen, plus the singular Switch FK, all live in
  connectivity_unbalanced.SwitchPhase.
- ratedCurrent lives in electrical_unbalanced.SwitchPhase instead - a
  different part module, which also carries its own duplicate Switch FK but
  none of phaseSide1/phaseSide2/normalOpen.
- open lives in steady_state_hypothesis.SwitchPhase - a third part module,
  with none of the above fields and no Switch FK of its own.
Since the singular Switch FK is what the association is set through
(inverse='Switch.SwitchPhase', auto-appending this child onto the parent
switch's own SwitchPhase list), and connectivity_unbalanced is the only part
module carrying that FK alongside phaseSide1/phaseSide2, add_connectivity
below resolves and sets the FK through connectivity_unbalanced.
"""

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder
from cimbuilder.object_builder.switch import switch


class SwitchPhaseBuilder(ObjectBuilder):
    cim_class_name = "SwitchPhase"

    def add_connectivity(
        self,
        switch_phase: CN.SwitchPhase,
        *,
        Switch: str,
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
        self, switch_phase: EL_UNBAL.SwitchPhase, *, ratedCurrent: float | Qty | None = None
    ) -> EL_UNBAL.SwitchPhase:
        """
        Adds single-phase electrical parameters for the switch
        * ratedCurrent: max normal operating current, float in amps or Qty('A')
        """
        graph_write.set_attr(switch_phase, EL_UNBAL, "ratedCurrent", ratedCurrent)
        return switch_phase

    def add_ssh(self, switch_phase:SSH.SwitchPhase, *, open:bool) -> SSH.SwitchPhase:
        """
        Adds real-time switch status from measurement or basecase.
        * open: boolean, indicates single-phase switch open/closed status
        """
        graph_write.set_attr(switch_phase, SSH, "open", open)
        return switch_phase
