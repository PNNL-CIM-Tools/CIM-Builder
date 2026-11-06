import cimprofiles.cim18.cim18v17.topology as TP
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class TopologicalNodeBuilder(ObjectBuilder):
    cim_class_name = "TopologicalNode"

    def add_bus_number(
        self, node: TP.TopologicalNode, *, busName: str, busNumber: int
    ) -> TP.TopologicalNode:

        graph_write.set_attr(node, TP, "busName", busName)
        graph_write.set_attr(node, TP, "busNumber", busNumber)

        return node

    def add_bus_name_marker(
        self,
        node: TP.TopologicalNode,
        *,
        BusNameMarker: str,
        priority: int,
    ) -> tuple[TP.TopologicalNode, TP.BusNameMarker]:

        tp: TP = self.cim  # type:ignore
        # TODO: implement better name logic
        marker = tp.BusNameMarker(mRID=BusNameMarker)
        graph_write.set_attr(marker, TP, "priority", priority)
        graph_write.set_assc(marker, TP, "TopologicalNode", node)
        graph_write.add_to_graph(self.network, marker)
        return node, marker
