import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH

from cimbuilder.builders.base import ObjectBuilder
from cimbuilder.builders.switch.switch_phase import SwitchPhaseBuilder
from cimtables import connectivity, graph_write
from cimtables.connectivity import parse_phases, phase_code


class SwitchBuilder(ObjectBuilder):
    cim_class_name = 'Switch'

    def add_connectivity(self, switch, *, node1: str, node2: str,
                          phaseSide1: list[str] | None = None, phaseSide2: list[str] | None = None,
                          container: object = None, normalOpen=None, retained=None,
                          areaBoundary=None, topologicalUsage=None, BaseVoltage=None) -> list[object]:
        """phaseSide1/phaseSide2 are parallel lists, one entry per SwitchPhase
        row: phaseSide1[i] is that row's phase on terminal 1 (node1 side),
        phaseSide2[i] is its phase on terminal 2 (node2 side) - independently,
        since a switch (unlike a line or wye/delta shunt) can carry a
        different phase on each side (an open-phase device, a cross-phased
        jumper, ...). cimtables.connectivity.add_phase_children cannot
        express this - it always sets phaseSide1 == phaseSide2 for a given
        child - so this method does NOT call it; it sets each terminal's own
        `phases` from that side's own token superset, and builds one
        SwitchPhase per row itself via SwitchPhaseBuilder (which owns the
        Switch FK/part-module details - see switch_phase.py)."""
        resolved_container = container if container is not None else self.container
        terminals = connectivity.add_connectivity(
            self.network, switch, node_cols={'node1': node1, 'node2': node2},
            container=resolved_container)

        if phaseSide1 is not None or phaseSide2 is not None:
            if phaseSide1 is None or phaseSide2 is None or len(phaseSide1) != len(phaseSide2):
                raise ValueError(
                    f"{switch.name!r}: phaseSide1 and phaseSide2 must both be given, "
                    f"as parallel lists of equal length (one entry per SwitchPhase row)"
                )
            terminal1, terminal2 = terminals
            graph_write.set_attr(terminal1, self.cim, 'phases', self.cim.PhaseCode(phase_code(phaseSide1)))
            graph_write.set_attr(terminal2, self.cim, 'phases', self.cim.PhaseCode(phase_code(phaseSide2)))

            phase_builder = SwitchPhaseBuilder(self.network)
            for i, (side1, side2) in enumerate(zip(phaseSide1, phaseSide2), start=1):
                switch_phase = phase_builder.create(name=f'{switch.name}_phase{i}')
                graph_write.add_to_graph(self.network, switch_phase)
                phase_builder.add_connectivity(switch_phase, Switch=switch.name, phaseSide1=side1, phaseSide2=side2)

        graph_write.set_attr(switch, CN, 'normalOpen', normalOpen)
        graph_write.set_attr(switch, CN, 'retained', retained)
        graph_write.set_attr(switch, CN, 'areaBoundary', areaBoundary)
        if topologicalUsage is not None:
            graph_write.set_attr(switch, CN, 'topologicalUsage', self.cim.TopologicalUsageKind(topologicalUsage))
        if BaseVoltage is not None:
            target = graph_write.resolve(self.network, self.cim.BaseVoltage, BaseVoltage)
            graph_write.set_assc(switch, CN, 'BaseVoltage', target)
        return terminals

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