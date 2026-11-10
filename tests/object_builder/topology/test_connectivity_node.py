from cimbuilder.object_builder.load import EnergyConsumerBuilder
from cimbuilder.object_builder.topology import ConnectivityNodeBuilder


def test_connectivity_node_reused_by_equipment(network, container, base_voltage):
    builder = ConnectivityNodeBuilder(network=network, container=container)
    node = builder.create(mRID="671", name="671")
    builder.add_connectivity(node, BaseVoltage=base_voltage.mRID)

    load_builder = EnergyConsumerBuilder(network=network, container=container)
    load = load_builder.create(mRID="ld_671")
    _, terminal, _ = load_builder.add_connectivity(load, node="671", BaseVoltage=base_voltage.mRID)

    assert node.name == "671"
    assert node.BaseVoltage is base_voltage
    assert node.ConnectivityNodeContainer is container
    assert terminal.ConnectivityNode is node
