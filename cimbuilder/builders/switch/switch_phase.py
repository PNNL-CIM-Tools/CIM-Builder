import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH

from cimbuilder.builders.base import ObjectBuilder
from cimtables import connectivity, graph_write

class SwitchBuilder(ObjectBuilder):
    cim_class_name = 'SwitchPhase'

    def add_connectivity(self, switch_phase, *, Switch, phaseSide1, phaseSide2, normalOpen=None) -> None:


        if Switch is not None:
            target = graph_write.resolve(self.network, self.cim.Switch, Switch)
            graph_write.set_assc(switch_phase, CN, 'BaseVoltage', target)
        
        graph_write.set_attr(switch_phase, CN, 'normalOpen', normalOpen)
        
        
    def add_ssh(self, switch_phase, *, open) -> None:
        graph_write.set_attr(switch_phase, SSH, 'open', open)
        