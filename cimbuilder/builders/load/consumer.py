import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
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
            if target is None:
                raise ValueError(
                    f"{load.mRID!r}: BaseVoltage {BaseVoltage!r} not found in graph "
                    f"(build it before the instance that references it)"
                )
            graph_write.set_assc(load, CN, 'BaseVoltage', target)

    def add_electrical(self, load, *, pfixed=None, qfixed=None, pfixedPct=None, qfixedPct=None, LoadResponse=None) -> None:

        graph_write.set_attr(load, EL_BAL, 'pfixed', pfixed)
        graph_write.set_attr(load, EL_BAL, 'qfixed', qfixed)
        graph_write.set_attr(load, EL_BAL, 'pfixedPct', pfixedPct)
        graph_write.set_attr(load, EL_BAL, 'qfixedPct', qfixedPct)

        if LoadResponse is not None:
            target = graph_write.resolve(self.network, self.cim.LoadResponseCharacteristic, LoadResponse)
            if target is None:
                raise ValueError(
                    f"{load.mRID!r}: LoadResponse {LoadResponse!r} not found in graph "
                    f"(build it before the instance that references it)"
                )
            graph_write.set_assc(load, EL_BAL, 'LoadResponse', target)

    def add_ssh(self, load, *, p=None, q=None) -> None:
        graph_write.set_attr(load, SSH, 'p', p)
        graph_write.set_attr(load, SSH, 'q', q)

