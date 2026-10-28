import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH

from cimbuilder.builders.base import ObjectBuilder
from cimtables import connectivity, graph_write

class SwitchBuilder(ObjectBuilder):
    cim_class_name = 'Switch'

    def add_connectivity(self, switch, *, node1: str, node2: str, phases: str | None = None,
                        container: object = None, normalOpen=None, retained=None,
                        areaBoundary=None, topologicalUsage=None, BaseVoltage=None) -> None:

        resolved_container = container if container is not None else self.container
        terminals = connectivity.add_connectivity(
            self.network, switch, node_cols={'node1': node1, 'node2': node2},
            container=resolved_container)
        if phases is not None:
            connectivity.add_phase_children(self.network, switch, terminals, phases=phases)
            
        graph_write.set_attr(switch, CN, 'normalOpen', normalOpen)
        graph_write.set_attr(switch, CN, 'retained', retained)
        graph_write.set_attr(switch, CN, 'areaBoundary', areaBoundary)
        if topologicalUsage is not None:
            graph_write.set_attr(switch, CN, 'topologicalUsage', self.cim.TopologicalUsageKind(topologicalUsage))
        if BaseVoltage is not None:
            target = graph_write.resolve(self.network, self.cim.BaseVoltage, BaseVoltage)
            graph_write.set_assc(switch, CN, 'BaseVoltage', target)

    def add_electrical(self, switch, *, ratedCurrent=None,
                                gangOperated=None, motorOperated=None,
                                remotelyOperated=None, loadBreak=None) -> None:
       
        graph_write.set_attr(switch, EL_BAL, 'ratedCurrent', ratedCurrent)
        graph_write.set_attr(switch, EL_BAL, 'gangOperated', gangOperated)
        graph_write.set_attr(switch, EL_BAL, 'motorOperated', motorOperated)
        graph_write.set_attr(switch, EL_BAL, 'remotelyOperated', remotelyOperated)
        graph_write.set_attr(switch, EL_BAL, 'loadBreak', loadBreak)

    def add_ssh(self, switch, *, open=None) -> None:
        graph_write.set_attr(switch, SSH, 'open', open)


class FuseBuilder(SwitchBuilder):
    cim_class_name = 'Fuse'

class SectionaliserBuilder(SwitchBuilder):
    cim_class_name='Sectionaliser'

class DisconnectorBuilder(SwitchBuilder):
    cim_class_name = 'Disconnector'
    
class ServiceDisconnectBuilder(DisconnectorBuilder):
    cim_class_name = 'ServiceDisconnect'
    
class ElbowBuilder(DisconnectorBuilder):
    cim_class_name = 'Elbow'
    
class AirBreakSwitchBuilder(DisconnectorBuilder):
    cim_class_name = 'AirBreakSwitch'
    
class HookstickSwitchBuilder(DisconnectorBuilder):
    cim_class_name = 'HookstickSwitch'