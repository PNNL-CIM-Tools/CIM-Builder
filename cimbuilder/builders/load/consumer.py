"""Phase 5: EnergyConsumerBuilder (design: CIMTBL_DESIGN.md §8.1,
cimbuilder/development/GRAPH_WRITE_CONTRACT.md).

Direct/manual API only - bulk .cimtbl loading goes through the generic,
reflective ObjectBuilder.from_table (builders/base.py), not per-class
add_<part> dispatch here. Stateless: every add_<part> method takes `load` as
an explicit parameter, and returns nothing - callers chain values through the
object itself, not through `self`. See GRAPH_WRITE_CONTRACT.md §6 for the
worked walkthrough this file follows.
"""

import cimgraph.data_profile.cim18gmdm.connectivity as CN
import cimgraph.data_profile.cim18gmdm.electrical as EL
import cimgraph.data_profile.cimhub_2026 as cimhub_2026  # p/q/pFixed/pFixedPct: no SSH
                                                          # part in cim18gmdm yet (checked
                                                          # 2026-09-15) - no-op part,
                                                          # see GRAPH_WRITE_CONTRACT.md §6

from cimbuilder.builders.base import ObjectBuilder
from cimbuilder.core import connectivity, graph_write


class EnergyConsumerBuilder(ObjectBuilder):
    cim_class_name = 'EnergyConsumer'

    def add_connectivity(self, load, *, node: str, container: object = None,
                          phaseConnection=None, grounded=None, customerCount=None) -> None:
        connectivity.add_connectivity(
            self.network, load, node_cols={'node': node},
            container=container if container is not None else self.container)
        graph_write.set_attr(load, CN, 'customerCount', customerCount)
        graph_write.set_attr(load, CN, 'grounded', grounded)
        graph_write.set_attr(load, CN, 'phaseConnection', phaseConnection)

    def add_electrical(self, load, *, pFixed=None, qFixed=None, pFixedPct=None, qFixedPct=None) -> None:
        graph_write.set_attr(load, cimhub_2026, 'pFixed', pFixed)
        graph_write.set_attr(load, cimhub_2026, 'qFixed', qFixed)
        graph_write.set_attr(load, cimhub_2026, 'pFixedPct', pFixedPct)
        graph_write.set_attr(load, cimhub_2026, 'qFixedPct', qFixedPct)

    def add_ssh(self, load, *, p=None, q=None) -> None:
        graph_write.set_attr(load, cimhub_2026, 'p', p)
        graph_write.set_attr(load, cimhub_2026, 'q', q)

    def add_references(self, load, *, BaseVoltage=None, LoadResponse=None) -> None:
        if BaseVoltage is not None:
            target = graph_write.resolve(self.network, self.cim.BaseVoltage, BaseVoltage)
            graph_write.set_assc(load, CN, 'BaseVoltage', target)
        if LoadResponse is not None:
            target = graph_write.resolve(self.network, self.cim.LoadResponseCharacteristic, LoadResponse)
            graph_write.set_assc(load, EL, 'LoadResponse', target)
