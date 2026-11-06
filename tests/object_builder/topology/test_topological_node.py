from cimbuilder.object_builder.topology import TopologicalNodeBuilder


def test_topological_node_add_bus_number(network, container):
    builder = TopologicalNodeBuilder(network=network, container=container)
    node = builder.create(mRID="tn1")

    builder.add_bus_number(node, busName="BUS1", busNumber=1)
    assert node.busNumber == 1


def test_topological_node_add_bus_name_marker(network, container):
    builder = TopologicalNodeBuilder(network=network, container=container)
    node = builder.create(mRID="tn1")

    node, marker = builder.add_bus_name_marker(node, BusNameMarker="marker1", priority=1)
    assert marker.TopologicalNode is node
