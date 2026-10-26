"""Phase 5: EnergyConsumerBuilder (design: CIMTBL_DESIGN.md §8.1,
cimbuilder/development/GRAPH_WRITE_CONTRACT.md).

Direct/manual API only - bulk .cimtbl loading goes through the generic,
reflective ObjectBuilder.from_table (builders/base.py), not per-class
add_<part> dispatch here. Stateless: every add_<part> method takes `load` as
an explicit parameter, and returns nothing - callers chain values through the
object itself, not through `self`. See GRAPH_WRITE_CONTRACT.md §6 for the
worked walkthrough this file follows.
"""

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH

from cimbuilder.builders.base import ObjectBuilder
from cimtables import connectivity, graph_write


class EnergyConsumerBuilder(ObjectBuilder):
    cim_class_name = 'EnergyConsumer'

    def add_connectivity(self, load, *, node: str, container: object = None,
                          phaseConnection=None, grounded=None, customerCount=None, BaseVoltage=None) -> None:
        connectivity.add_connectivity(
            self.network, load, node_cols={'node': node},
            container=container if container is not None else self.container)
        graph_write.set_attr(load, CN, 'customerCount', customerCount)
        graph_write.set_attr(load, CN, 'grounded', grounded)
        graph_write.set_attr(load, CN, 'phaseConnection', phaseConnection)
        if BaseVoltage is not None:
                    target = graph_write.resolve(self.network, self.cim.BaseVoltage, BaseVoltage)
                    graph_write.set_assc(load, CN, 'BaseVoltage', target)

    def add_electrical(self, load, *, pfixed=None, qfixed=None, pfixedPct=None, qfixedPct=None, LoadResponse=None) -> None:
        # cim18v17.electrical_unbalanced.EnergyConsumer spells these lowercase
        # (pfixed/qfixed/...), unlike the old merged cimhub_2026 profile's
        # pfixed/qfixed - keyword args keep the public camelCase name, only the
        # set_attr target changes.
        graph_write.set_attr(load, EL, 'pfixed', pfixed)
        graph_write.set_attr(load, EL, 'qfixed', qfixed)
        graph_write.set_attr(load, EL, 'pfixedPct', pfixedPct)
        graph_write.set_attr(load, EL, 'qfixedPct', qfixedPct)
        
        if LoadResponse is not None:
                    target = graph_write.resolve(self.network, self.cim.LoadResponseCharacteristic, LoadResponse)
                    graph_write.set_assc(load, EL, 'LoadResponse', target)

    def add_ssh(self, load, *, p=None, q=None) -> None:
        graph_write.set_attr(load, SSH, 'p', p)
        graph_write.set_attr(load, SSH, 'q', q)

