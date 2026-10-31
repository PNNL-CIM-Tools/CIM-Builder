import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH

from cimtables import graph_write
from cimbuilder.builders.switch.switch import SwitchBuilder


class ProtectedSwitchBuilder(SwitchBuilder):
    cim_class_name = 'ProtectedSwitch'

    def add_electrical(self, switch, *,  ratedCurrent=None,
                                gangOperated=None, motorOperated=None,
                                remotelyOperated=None, loadBreak=None,
                                breakingCapacity=None, makingCapacity=None) -> None:
        """Extends SwitchBuilder.add_electrical with ProtectedSwitch's own
        interrupting-capacity ratings (electrical_balanced.ProtectedSwitch);
        ratedCurrent/gangOperated/motorOperated/remotelyOperated/loadBreak
        are passed straight through to the parent (same contract as
        SwitchBuilder.add_electrical).
        * breakingCapacity: a Qty resolved to CurrentFlow (A, SI base) -
          max current this switch can safely interrupt.
        * makingCapacity: a Qty resolved to CurrentFlow (A, SI base) - max
          current this switch can safely close onto.
        A bare number for either is stored unconverted via plain setattr.
        """
        super().add_electrical(switch, ratedCurrent=ratedCurrent, gangOperated=gangOperated,
                               motorOperated=motorOperated, remotelyOperated=remotelyOperated,
                               loadBreak=loadBreak)
        graph_write.set_attr(switch, EL_BAL, 'breakingCapacity', breakingCapacity)
        graph_write.set_attr(switch, EL_BAL, 'makingCapacity', makingCapacity)
        

class BreakerBuilder(ProtectedSwitchBuilder):
    cim_class_name = 'Breaker'

    def add_electrical(self, switch, *, ratedCurrent=None, gangOperated=None,
                       motorOperated=None, remotelyOperated=None, loadBreak=None,
                       breakingCapacity=None, makingCapacity=None,
                       inTransitTime=None) -> None:
        """Extends ProtectedSwitchBuilder.add_electrical with Breaker's own
        operating-time field (electrical_balanced.Breaker); all other
        params are passed straight through to the parent/grandparent (same
        contract as ProtectedSwitchBuilder.add_electrical /
        SwitchBuilder.add_electrical).
        * inTransitTime: a Qty resolved to Seconds (s, SI base) - time the
          breaker's contacts spend transitioning from closed to open. A bare
          number is stored unconverted via plain setattr.
        """
        super().add_electrical(switch, breakingCapacity=breakingCapacity, makingCapacity=makingCapacity,
                               ratedCurrent=ratedCurrent, gangOperated=gangOperated,
                               motorOperated=motorOperated, remotelyOperated=remotelyOperated,
                               loadBreak=loadBreak)
        graph_write.set_attr(switch, EL_BAL, 'inTransitTime', inTransitTime)


class RecloserBuilder(ProtectedSwitchBuilder):
    cim_class_name = 'Recloser'
    

class LoadBreakSwitchBuilder(ProtectedSwitchBuilder):
    cim_class_name = 'LoadBreakSwitch'