from __future__ import annotations

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface, get_cim_profile
import cimgraph.data_profile.cimhub_2023 as cim

from cimbuilder import object_builder
import cimbuilder.utils as utils

import logging
_log = logging.getLogger(__name__)


def new_sectionalized_bus_substation(
    connection: ConnectionInterface,
    name: str = 'new_sectionalized_bus_sub',
    base_voltage: int | cim.BaseVoltage = 115000,
    total_sections: int = 2,
    network: GraphModel = None
) -> dict:
    """
    Create a sectionalized bus substation in node-breaker representation.

    A sectionalized bus topology divides a single bus into multiple sections
    connected by bus ties, allowing isolation of faults while maintaining service.

    Args:
        connection: Connection interface to the CIM database
        name: Name of the substation
        base_voltage: Base voltage in volts or a BaseVoltage object
        total_sections: Number of bus sections to create
        network: Optional existing network to add the substation to

    Returns:
        Dictionary with keys: 'network', 'substation', 'buses', 'base_voltage'
        where 'buses' is a list of bus connectivity nodes
    """
    cim_profile, cim_module = get_cim_profile()
    cim_mod = cim_module

    # Create substation
    substation = cim_mod.Substation(name=name)

    # Create or use existing network
    if not network:
        network = DistributedArea(connection=connection, container=substation, distributed=False)
    network.add_to_graph(substation)

    # Get or create base voltage
    base_voltage = utils.get_base_voltage(network, base_voltage)

    # Create bus sections
    buses = []
    for section in range(total_sections):
        bus = cim_mod.ConnectivityNode(name=f'{name}_bus_{section + 1}')
        bus.ConnectivityNodeContainer = substation
        network.add_to_graph(bus)
        object_builder.new_bus_bar_section(network, bus)
        buses.append(bus)

    # Create bus ties between adjacent sections
    for section in range(total_sections - 1):
        from_bus = buses[section]
        to_bus = buses[section + 1]
        series_number = (section + 1) * 10
        _create_bus_tie(network, substation, from_bus, to_bus, series_number, name, base_voltage)

    return {
        'network': network,
        'substation': substation,
        'buses': buses,
        'base_voltage': base_voltage
    }


def _create_bus_tie(
    network: GraphModel,
    substation: cim.Substation,
    from_bus: cim.ConnectivityNode,
    to_bus: cim.ConnectivityNode,
    series_number: int,
    substation_name: str,
    base_voltage: cim.BaseVoltage
) -> None:
    """Create a bus tie between two bus sections."""
    cim_profile, cim_module = get_cim_profile()
    cim_mod = cim_module

    # Create junction nodes
    junction1 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{series_number}_bt_j1',
        ConnectivityNodeContainer=substation
    )
    junction2 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{series_number}_bt_j2',
        ConnectivityNodeContainer=substation
    )

    # Create switching equipment
    bus_tie = object_builder.new_breaker(
        network, substation,
        name=f'{substation_name}_bt_{series_number}',
        node1=junction1, node2=junction2
    )
    airgap1 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation_name}_bt_{series_number + 1}',
        node1=from_bus, node2=junction1
    )
    airgap2 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation_name}_bt_{series_number + 2}',
        node1=junction2, node2=to_bus
    )

    # Set base voltage
    bus_tie.BaseVoltage = base_voltage
    airgap1.BaseVoltage = base_voltage
    airgap2.BaseVoltage = base_voltage

    # Add to graph
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)


def add_branch_to_sectionalized_bus(
    network: GraphModel,
    substation: cim.Substation,
    section_number: int,
    buses: list[cim.ConnectivityNode],
    base_voltage: cim.BaseVoltage,
    branch_equipment: cim.ConductingEquipment,
    branch_terminal: cim.Terminal | int
) -> None:
    """
    Add a branch connection to a sectionalized bus substation.

    Args:
        network: Graph model containing the substation
        substation: The substation object
        section_number: 1-indexed section number to connect to
        buses: List of bus connectivity nodes
        base_voltage: Base voltage object
        branch_equipment: Branch equipment to be connected
        branch_terminal: Terminal or terminal index of the branch equipment
    """
    cim_profile, cim_module = get_cim_profile()
    cim_mod = cim_module

    section_bus = buses[section_number - 1]  # Convert to 0-indexed

    # Create junction nodes
    junction1 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{section_number}_j1',
        ConnectivityNodeContainer=substation
    )
    junction2 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{section_number}_j2',
        ConnectivityNodeContainer=substation
    )
    junction3 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{section_number}_j3',
        ConnectivityNodeContainer=substation
    )

    # Create switching equipment
    breaker = object_builder.new_breaker(
        network, substation,
        name=f'{substation.name}_{10*section_number}',
        node1=junction1, node2=junction2
    )
    airgap1 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{10*section_number+1}',
        node1=section_bus, node2=junction1
    )
    airgap2 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{10*section_number+2}',
        node1=junction2, node2=junction3
    )

    # Set base voltage
    breaker.BaseVoltage = base_voltage
    airgap1.BaseVoltage = base_voltage
    airgap2.BaseVoltage = base_voltage

    # Connect branch terminal
    if isinstance(branch_terminal, cim_mod.Terminal):
        branch_terminal.ConnectivityNode = junction3

    # Add to graph
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)
    network.add_to_graph(junction3)


def add_feeder_to_sectionalized_bus(
    network: GraphModel,
    substation: cim.Substation,
    section_number: int,
    buses: list[cim.ConnectivityNode],
    base_voltage: cim.BaseVoltage,
    feeder_network: GraphModel,
    feeder: cim.Feeder,
    sourcebus: cim.ConnectivityNode = None
) -> None:
    """
    Add a feeder connection to a sectionalized bus substation.

    Args:
        network: Graph model containing the substation
        substation: The substation object
        section_number: 1-indexed section number to connect to
        buses: List of bus connectivity nodes
        base_voltage: Base voltage object
        feeder_network: Graph model containing the feeder
        feeder: Feeder object to be connected
        sourcebus: Optional source bus for the feeder
    """
    cim_profile, cim_module = get_cim_profile()
    cim_mod = cim_module

    feeder_network.get_all_edges(cim_mod.Feeder)

    # Find sourcebus if not provided
    if not sourcebus:
        sourcebus = utils.get_source_bus(feeder_network, feeder)

    section_bus = buses[section_number - 1]  # Convert to 0-indexed

    # Create junction nodes
    junction1 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{section_number}_j1',
        ConnectivityNodeContainer=substation
    )
    junction2 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{section_number}_j2',
        ConnectivityNodeContainer=substation
    )

    # Create switching equipment
    breaker = object_builder.new_breaker(
        network, substation,
        name=f'{substation.name}_{10*section_number}',
        node1=junction1, node2=junction2
    )
    airgap1 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{10*section_number+1}',
        node1=section_bus, node2=junction1
    )
    airgap2 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{10*section_number+2}',
        node1=junction2, node2=sourcebus
    )

    # Set base voltage
    breaker.BaseVoltage = base_voltage
    airgap1.BaseVoltage = base_voltage
    airgap2.BaseVoltage = base_voltage

    # Configure feeder-substation relationship
    feeder.NormalEnergizingSubstation = substation
    substation.NormalEnergizedFeeder.append(feeder)

    # Add to graph
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)
    network.add_to_graph(sourcebus)
    network.add_to_graph(feeder)
