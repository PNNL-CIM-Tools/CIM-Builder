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
        """Resolves the parent Switch by mRID (any concrete subclass -
        Breaker/Disconnector/... - via resolve, since cim_cls may be an
        abstract base and the parent was built by whichever SwitchBuilder
        leaf matches its real type) and sets phaseSide1/phaseSide2
        independently, so a switch can carry phase A on side 1 and phase B
        on side 2.
        * Switch: mRID string of an existing Switch (or subclass, e.g.
          Breaker/Disconnector) - already built via one of the SwitchBuilder
          classes. Resolved via set_assc_from_mrid, which raises ValueError
          if that mRID isn't already in the graph.
        * phaseSide1/phaseSide2: string value of
          connectivity_unbalanced.SinglePhaseKind (e.g. 'A', 's1'), converted
          via `self.cim.SinglePhaseKind(...)` before set_attr - this switch
          phase's phase on terminal 1 / terminal 2 respectively.
        * normalOpen: plain bool, no unit wrapping.

        Returns the resolved parent Switch object.
        """
        target = graph_write.set_assc_from_mrid(self.network, switch_phase, CN, 'Switch', self.cim.Switch, Switch)
        graph_write.set_attr(switch_phase, CN, 'phaseSide1', self.cim.SinglePhaseKind(phaseSide1))
        graph_write.set_attr(switch_phase, CN, 'phaseSide2', self.cim.SinglePhaseKind(phaseSide2))
        graph_write.set_attr(switch_phase, CN, 'normalOpen', normalOpen)
        return target

    def add_electrical(self, switch_phase, *, ratedCurrent=None) -> None:
        """Adds electrical_unbalanced.SwitchPhase's per-phase rating.
        * ratedCurrent: a Qty resolved to CurrentFlow (A, SI base). A bare
          number is stored unconverted via plain setattr.
        """
        graph_write.set_attr(switch_phase, EL_UNBAL, 'ratedCurrent', ratedCurrent)

    def add_ssh(self, switch_phase, *, open=None) -> None:
        """Adds steady_state_hypothesis.SwitchPhase's solved per-phase state.
        * open: plain bool, no unit wrapping - True means this phase is open.
        """
        graph_write.set_attr(switch_phase, SSH, 'open', open)
