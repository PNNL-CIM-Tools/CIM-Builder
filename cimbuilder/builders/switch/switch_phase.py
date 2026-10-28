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

from cimbuilder.builders.base import ObjectBuilder
from cimtables import graph_write


class SwitchPhaseBuilder(ObjectBuilder):
    cim_class_name = 'SwitchPhase'

    def add_connectivity(self, switch_phase, *, Switch: str, phaseSide1, phaseSide2,
                          normalOpen=None) -> object:
        """Resolves the named parent Switch (any concrete subclass -
        Breaker/Disconnector/... - via resolve_any_subclass, since the
        parent was built by whichever SwitchBuilder leaf matches its real
        type) and sets phaseSide1/phaseSide2 independently, so a switch can
        carry phase A on side 1 and phase B on side 2."""
        target = graph_write.resolve_any_subclass(self.network, self.cim.Switch, Switch)
        if target is None:
            raise ValueError(
                f"{switch_phase.name!r}: Switch {Switch!r} not found in graph "
                f"(build the switch before the SwitchPhase that references it)"
            )
        graph_write.set_assc(switch_phase, CN, 'Switch', target)
        graph_write.set_attr(switch_phase, CN, 'phaseSide1', self.cim.SinglePhaseKind(phaseSide1))
        graph_write.set_attr(switch_phase, CN, 'phaseSide2', self.cim.SinglePhaseKind(phaseSide2))
        graph_write.set_attr(switch_phase, CN, 'normalOpen', normalOpen)
        return target

    def add_electrical(self, switch_phase, *, ratedCurrent=None) -> None:
        graph_write.set_attr(switch_phase, EL_UNBAL, 'ratedCurrent', ratedCurrent)

    def add_ssh(self, switch_phase, *, open=None) -> None:
        graph_write.set_attr(switch_phase, SSH, 'open', open)
