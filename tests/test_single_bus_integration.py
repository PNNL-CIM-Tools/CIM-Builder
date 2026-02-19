"""
Integration test for single bus substation using the new functional API.

This test demonstrates the complete workflow:
1. Create a single bus substation
2. Add multiple feeders to the substation
3. Validate the topology and connections
4. Export to XML
"""

import os
import pytest
import tempfile
from pathlib import Path

import cimgraph.data_profile.cimhub_2023 as cim
from cimgraph.models import FeederModel, NodeBreakerModel
from cimgraph.databases import XMLFile

# Import new functional API
from cimbuilder import (
    new_single_bus_substation,
    add_feeder_to_single_bus,
)


@pytest.fixture
def setup_environment():
    """Set up environment variables for CIM profile."""
    os.environ['CIMG_CIM_PROFILE'] = 'cimhub_2023'
    yield
    # Cleanup if needed


@pytest.fixture
def sample_feeder_ieee13(tmp_path):
    """
    Create a sample feeder based on IEEE 13 bus model.

    In a real test, this would load from the sample_models directory.
    For now, we'll create a minimal feeder structure.
    """
    # Check if sample model exists
    sample_model_path = Path(__file__).parent.parent / 'sample_models' / 'ieee13.xml'

    if sample_model_path.exists():
        # Load real IEEE 13 model
        ieee13_feeder = cim.Feeder(mRID='49AD8E07-3BF9-A4E2-CB8F-C3722F837B62')
        xml13 = XMLFile(filename=str(sample_model_path))
        ieee13_network = FeederModel(connection=xml13, container=ieee13_feeder, distributed=False)
        return ieee13_feeder, ieee13_network
    else:
        # Create minimal feeder for testing
        output_xml = tmp_path / 'minimal_feeder.xml'
        xml_conn = XMLFile(filename=str(output_xml))

        feeder = cim.Feeder(mRID='TEST-FEEDER-001')
        feeder_network = FeederModel(connection=xml_conn, container=feeder, distributed=False)

        # Create minimal feeder structure with source bus
        source_node = cim.ConnectivityNode(name='sourcebus')
        source_node.ConnectivityNodeContainer = feeder
        feeder_network.add_to_graph(source_node)

        # Create energy source at sourcebus
        energy_source = cim.EnergySource(name='source')
        energy_source.EquipmentContainer = feeder
        terminal = cim.Terminal(name='source_t1', sequenceNumber=1)
        terminal.ConnectivityNode = source_node
        terminal.ConductingEquipment = energy_source
        energy_source.Terminals.append(terminal)
        feeder_network.add_to_graph(energy_source)
        feeder_network.add_to_graph(terminal)

        # Set NormalHeadTerminal
        feeder.NormalHeadTerminal = terminal
        feeder_network.add_to_graph(feeder)

        return feeder, feeder_network


def test_single_bus_substation_creation(setup_environment, tmp_path):
    """Test creating a single bus substation with the functional API."""

    # Create output file
    output_xml = tmp_path / 'test_single_bus.xml'
    connection = XMLFile(filename=str(output_xml))

    # Create substation using new functional API
    result = new_single_bus_substation(
        connection=connection,
        name='test_single_bus_sub',
        base_voltage=115000
    )

    # Verify returned components
    assert 'network' in result
    assert 'substation' in result
    assert 'main_bus' in result
    assert 'base_voltage' in result

    network = result['network']
    substation = result['substation']
    main_bus = result['main_bus']
    base_voltage = result['base_voltage']

    # Verify substation properties
    assert substation.name == 'test_single_bus_sub'
    assert isinstance(substation, cim.Substation)

    # Verify main bus
    assert main_bus.name == 'test_single_bus_sub_main_bus'
    assert isinstance(main_bus, cim.ConnectivityNode)
    assert main_bus.ConnectivityNodeContainer == substation

    # Verify base voltage
    assert isinstance(base_voltage, cim.BaseVoltage)
    assert base_voltage.nominalVoltage == 115000

    # Verify bus bar section was created
    network.get_all_edges(cim.BusbarSection)
    assert cim.BusbarSection in network.graph
    assert len(network.graph[cim.BusbarSection]) > 0


def test_add_feeder_to_single_bus(setup_environment, sample_feeder_ieee13, tmp_path):
    """Test adding a feeder to single bus substation."""

    # Create substation
    output_xml = tmp_path / 'test_single_bus_with_feeder.xml'
    connection = XMLFile(filename=str(output_xml))

    result = new_single_bus_substation(
        connection=connection,
        name='test_sub_with_feeder',
        base_voltage=115000
    )

    network = result['network']
    substation = result['substation']
    main_bus = result['main_bus']
    base_voltage = result['base_voltage']

    # Get feeder
    feeder, feeder_network = sample_feeder_ieee13

    # Add feeder using functional API
    feeder_result = add_feeder_to_single_bus(
        network=network,
        substation=substation,
        main_bus=main_bus,
        base_voltage=base_voltage,
        breaker_number=10,
        feeder_network=feeder_network,
        feeder=feeder
    )

    # Verify returned components
    assert 'breaker' in feeder_result
    assert 'disconnectors' in feeder_result
    assert 'junctions' in feeder_result

    breaker = feeder_result['breaker']
    disconnectors = feeder_result['disconnectors']
    junctions = feeder_result['junctions']

    # Verify switching equipment
    assert isinstance(breaker, cim.Breaker)
    assert breaker.name == 'test_sub_with_feeder_10'
    assert breaker.BaseVoltage == base_voltage

    # Verify disconnectors
    assert len(disconnectors) == 2
    assert all(isinstance(d, cim.Disconnector) for d in disconnectors)

    # Verify junctions
    assert len(junctions) == 2
    assert all(isinstance(j, cim.ConnectivityNode) for j in junctions)

    # Verify feeder linkage
    assert feeder.NormalEnergizingSubstation == substation
    assert feeder in substation.NormalEnergizedFeeder

    # Verify topology in graph
    network.get_all_edges(cim.Breaker)
    network.get_all_edges(cim.Disconnector)

    assert cim.Breaker in network.graph
    assert cim.Disconnector in network.graph
    assert len(network.graph[cim.Breaker]) >= 1
    assert len(network.graph[cim.Disconnector]) >= 2


def test_single_bus_with_multiple_feeders(setup_environment, sample_feeder_ieee13, tmp_path):
    """Test adding multiple feeders to single bus substation."""

    # Create substation
    output_xml = tmp_path / 'test_single_bus_multi_feeder.xml'
    connection = XMLFile(filename=str(output_xml))

    result = new_single_bus_substation(
        connection=connection,
        name='test_multi_feeder_sub',
        base_voltage=115000
    )

    network = result['network']
    substation = result['substation']
    main_bus = result['main_bus']
    base_voltage = result['base_voltage']

    # Get first feeder
    feeder1, feeder_network1 = sample_feeder_ieee13

    # Add first feeder
    feeder_result1 = add_feeder_to_single_bus(
        network=network,
        substation=substation,
        main_bus=main_bus,
        base_voltage=base_voltage,
        breaker_number=10,
        feeder_network=feeder_network1,
        feeder=feeder1
    )

    # Create second feeder (reuse same feeder structure with different mRID)
    feeder2 = cim.Feeder(mRID='TEST-FEEDER-002')
    output_xml2 = tmp_path / 'feeder2.xml'
    xml_conn2 = XMLFile(filename=str(output_xml2))
    feeder_network2 = FeederModel(connection=xml_conn2, container=feeder2, distributed=False)

    # Create minimal structure for feeder2
    source_node2 = cim.ConnectivityNode(name='sourcebus')
    source_node2.ConnectivityNodeContainer = feeder2
    feeder_network2.add_to_graph(source_node2)

    energy_source2 = cim.EnergySource(name='source2')
    energy_source2.EquipmentContainer = feeder2
    terminal2 = cim.Terminal(name='source2_t1', sequenceNumber=1)
    terminal2.ConnectivityNode = source_node2
    terminal2.ConductingEquipment = energy_source2
    energy_source2.Terminals.append(terminal2)
    feeder_network2.add_to_graph(energy_source2)
    feeder_network2.add_to_graph(terminal2)
    feeder2.NormalHeadTerminal = terminal2
    feeder_network2.add_to_graph(feeder2)

    # Add second feeder
    feeder_result2 = add_feeder_to_single_bus(
        network=network,
        substation=substation,
        main_bus=main_bus,
        base_voltage=base_voltage,
        breaker_number=20,
        feeder_network=feeder_network2,
        feeder=feeder2
    )

    # Verify both feeders are connected
    assert len(substation.NormalEnergizedFeeder) >= 2
    assert feeder1 in substation.NormalEnergizedFeeder
    assert feeder2 in substation.NormalEnergizedFeeder

    # Verify breakers have different names
    assert feeder_result1['breaker'].name != feeder_result2['breaker'].name
    assert feeder_result1['breaker'].name == 'test_multi_feeder_sub_10'
    assert feeder_result2['breaker'].name == 'test_multi_feeder_sub_20'


def test_export_to_xml(setup_environment, sample_feeder_ieee13, tmp_path):
    """Test exporting single bus substation to XML."""

    # Create substation
    output_xml = tmp_path / 'test_export.xml'
    connection = XMLFile(filename=str(output_xml))

    result = new_single_bus_substation(
        connection=connection,
        name='test_export_sub',
        base_voltage=115000
    )

    network = result['network']
    substation = result['substation']
    main_bus = result['main_bus']
    base_voltage = result['base_voltage']

    # Add a feeder
    feeder, feeder_network = sample_feeder_ieee13

    add_feeder_to_single_bus(
        network=network,
        substation=substation,
        main_bus=main_bus,
        base_voltage=base_voltage,
        breaker_number=10,
        feeder_network=feeder_network,
        feeder=feeder
    )

    # Upload (writes to XML)
    network.upload()

    # Verify XML file was created
    assert output_xml.exists()
    assert output_xml.stat().st_size > 0

    # Verify we can read it back
    content = output_xml.read_text()
    assert 'test_export_sub' in content
    assert 'Substation' in content
    assert 'ConnectivityNode' in content


def test_functional_api_idempotence(setup_environment, tmp_path):
    """Test that functional API calls are idempotent and don't have side effects."""

    # Create two substations independently
    output_xml1 = tmp_path / 'sub1.xml'
    connection1 = XMLFile(filename=str(output_xml1))

    result1 = new_single_bus_substation(
        connection=connection1,
        name='sub1',
        base_voltage=115000
    )

    output_xml2 = tmp_path / 'sub2.xml'
    connection2 = XMLFile(filename=str(output_xml2))

    result2 = new_single_bus_substation(
        connection=connection2,
        name='sub2',
        base_voltage=230000
    )

    # Verify they are independent
    assert result1['substation'] != result2['substation']
    assert result1['substation'].name == 'sub1'
    assert result2['substation'].name == 'sub2'

    assert result1['main_bus'] != result2['main_bus']
    assert result1['base_voltage'].nominalVoltage == 115000
    assert result2['base_voltage'].nominalVoltage == 230000

    # Verify networks are separate
    assert result1['network'] != result2['network']


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v'])
