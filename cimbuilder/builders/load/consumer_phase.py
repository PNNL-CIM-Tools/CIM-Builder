import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH

from cimbuilder.builders.base import ObjectBuilder
from cimtables import graph_write

class EnergyConsumerBuilder(ObjectBuilder):
    cim_class_name = 'EnergyConsumer'

    def add_connectivity(self, load_phs, *, EnergyConsumer) -> None:
        
        pass
    
    def add_electrical(self, load_phs, *, pfixed=None, qfixed=None, pfixedPct=None, qfixedPct=None) -> None:

        graph_write.set_attr(load_phs, EL_UNBAL, 'pfixed', pfixed)
        graph_write.set_attr(load_phs, EL_UNBAL, 'qfixed', qfixed)
        graph_write.set_attr(load_phs, EL_UNBAL, 'pfixedPct', pfixedPct)
        graph_write.set_attr(load_phs, EL_UNBAL, 'qfixedPct', qfixedPct)