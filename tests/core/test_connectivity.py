"""Phase 4 connectivity backend tests (design: CIMTBL_DESIGN.md §5, §12.4).

"ACLineSegment with node1/node2/phases -> terminals + N ACLineSegmentPhase;
undeclared nodes auto-vivified; bus* -> TopologicalNode disambiguation proven
on the line_1_2 sequence row." (§8's Phase 4 exit criterion.)
"""

import os
import tempfile

import pytest

os.environ['CIMG_CIM_PROFILE'] = 'cimhub_2026'

import cimgraph.data_profile.cimhub_2026 as cim
from cimgraph.databases import XMLFile
from cimgraph.models import BusBranchModel

from cimbuilder.core import connectivity, graph_write
from cimbuilder.core.name_index import NameIndex


@pytest.fixture
def network():
    conn = XMLFile(filename=tempfile.mktemp(suffix='.xml'))
    container = cim.Feeder(name='test_feeder')
    net = BusBranchModel(connection=conn, container=container, distributed=False)
    net.name_index = NameIndex()
    return net


def test_add_connectivity_auto_vivifies_nodes_and_wires_terminals(network):
    line = cim.ACLineSegment(name='650632')
    graph_write.add_to_graph(network, line)

    terminals = connectivity.add_connectivity(
        network, line, node_cols={'node1': 'RG60', 'node2': '362'}
    )

    assert len(terminals) == 2
    assert [t.sequenceNumber for t in terminals] == [1, 2]
    assert line.Terminals == terminals

    rg60 = graph_write.resolve(network, cim.ConnectivityNode, 'RG60')
    n362 = graph_write.resolve(network, cim.ConnectivityNode, '362')
    assert rg60 is not None and n362 is not None
    assert terminals[0].ConnectivityNode is rg60
    assert terminals[1].ConnectivityNode is n362
    assert terminals[0] in rg60.Terminals
    assert terminals[1] in n362.Terminals


def test_add_connectivity_sets_equipment_container_from_network_default(network):
    line = cim.ACLineSegment(name='650632')
    graph_write.add_to_graph(network, line)

    connectivity.add_connectivity(network, line, node_cols={'node1': 'RG60', 'node2': '362'})

    assert line.EquipmentContainer is network.container


def test_add_connectivity_propagates_container_to_nodes(network):
    line = cim.ACLineSegment(name='650632')
    graph_write.add_to_graph(network, line)

    connectivity.add_connectivity(network, line, node_cols={'node1': 'RG60', 'node2': '362'})

    rg60 = graph_write.resolve(network, cim.ConnectivityNode, 'RG60')
    n362 = graph_write.resolve(network, cim.ConnectivityNode, '362')
    assert rg60.ConnectivityNodeContainer is network.container
    assert n362.ConnectivityNodeContainer is network.container


def test_add_connectivity_does_not_overwrite_existing_node_container(network):
    other_container = cim.Feeder(name='other_feeder')
    node = cim.ConnectivityNode(name='671')
    graph_write.link(node, 'ConnectivityNodeContainer', other_container)
    graph_write.add_to_graph(network, node)

    line = cim.ACLineSegment(name='670671')
    graph_write.add_to_graph(network, line)
    connectivity.add_connectivity(network, line, node_cols={'node1': '670', 'node2': '671'})

    assert node.ConnectivityNodeContainer is other_container


def test_add_connectivity_explicit_container_overrides_network_default(network):
    explicit_container = cim.Feeder(name='explicit_feeder')
    line = cim.ACLineSegment(name='650632')
    graph_write.add_to_graph(network, line)

    connectivity.add_connectivity(
        network, line, node_cols={'node1': 'RG60', 'node2': '362'}, container=explicit_container
    )

    assert line.EquipmentContainer is explicit_container
    rg60 = graph_write.resolve(network, cim.ConnectivityNode, 'RG60')
    assert rg60.ConnectivityNodeContainer is explicit_container


def test_add_connectivity_bus_prefix_disambiguates_topological_node(network):
    line = cim.ACLineSegment(name='line_1_2')
    graph_write.add_to_graph(network, line)

    terminals = connectivity.add_connectivity(
        network, line, node_cols={'bus1': 'topo_bus_1', 'bus2': 'topo_bus_2'}
    )

    assert graph_write.resolve(network, cim.ConnectivityNode, 'topo_bus_1') is None
    topo_1 = graph_write.resolve(network, cim.TopologicalNode, 'topo_bus_1')
    topo_2 = graph_write.resolve(network, cim.TopologicalNode, 'topo_bus_2')
    assert topo_1 is not None and topo_2 is not None
    assert terminals[0].TopologicalNode is topo_1
    assert terminals[0].ConnectivityNode is None


def test_add_connectivity_reuses_same_node_across_calls(network):
    line_a = cim.ACLineSegment(name='362670')
    line_b = cim.ACLineSegment(name='670671')
    graph_write.add_to_graph(network, line_a)
    graph_write.add_to_graph(network, line_b)

    connectivity.add_connectivity(network, line_a, node_cols={'node1': 'MID', 'node2': '670'})
    connectivity.add_connectivity(network, line_b, node_cols={'node1': '670', 'node2': '671'})

    n670_via_a = graph_write.resolve(network, cim.ConnectivityNode, '670')
    n670_via_b = line_b.Terminals[0].ConnectivityNode
    assert n670_via_a is n670_via_b
    assert len(n670_via_a.Terminals) == 2


def test_add_connectivity_unknown_column_prefix_raises(network):
    line = cim.ACLineSegment(name='650632')
    graph_write.add_to_graph(network, line)

    with pytest.raises(ValueError, match='not a connectivity column'):
        connectivity.add_connectivity(network, line, node_cols={'terminal1': 'RG60'})


def test_add_phase_children_creates_correct_phase_kinds_and_sequence(network):
    line = cim.ACLineSegment(name='650632')
    graph_write.add_to_graph(network, line)
    terminals = connectivity.add_connectivity(
        network, line, node_cols={'node1': 'RG60', 'node2': '362'}
    )

    children = connectivity.add_phase_children(
        network, line, terminals, phases='ABCN', phase_cls=cim.ACLineSegmentPhase
    )

    assert len(children) == 4
    assert [c.phase for c in children] == [
        cim.SinglePhaseKind.A, cim.SinglePhaseKind.B,
        cim.SinglePhaseKind.C, cim.SinglePhaseKind.N,
    ]
    assert [c.sequenceNumber for c in children] == [1, 2, 3, 4]
    assert all(c.ACLineSegment is line for c in children)


def test_add_phase_children_resolves_parent_field_name_not_equal_to_class_name(network):
    shunt = cim.LinearShuntCompensator(name='cap1')
    graph_write.add_to_graph(network, shunt)

    children = connectivity.add_phase_children(
        network, shunt, [], phases='BC', phase_cls=cim.LinearShuntCompensatorPhase
    )

    assert all(c.ShuntCompensator is shunt for c in children)
