from __future__ import annotations

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface, get_cim_profile
import cimgraph.data_profile.cimhub_2023 as cim

import cimbuilder.object_builder as object_builder
import cimbuilder.utils as utils

import logging
_log = logging.getLogger(__name__)


def new_double_bus_single_breaker_substation(
    connection: ConnectionInterface,
    name: str = 'new_double_bus_single_breaker_sub',
    base_voltage: int | cim.BaseVoltage = 115000,
    network: GraphModel = None
) -> dict:
    """
    Create a double bus single breaker substation in node-breaker representation.

    This topology features two main buses (north and south) connected by a bus tie,
    with each connection using a single breaker and disconnectors to either bus.

    Args:
        connection: Connection interface to the CIM database
        name: Name of the substation
        base_voltage: Base voltage in volts or a BaseVoltage object
        network: Optional existing network to add the substation to

    Returns:
        Dictionary with keys: 'network', 'substation', 'north_bus', 'south_bus', 'base_voltage'
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

    # Create north bus
    north_bus = cim_mod.ConnectivityNode(name=f'{name}_north_bus')
    north_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(north_bus)
    object_builder.new_bus_bar_section(network, north_bus)

    # Create south bus
    south_bus = cim_mod.ConnectivityNode(name=f'{name}_south_bus')
    south_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(south_bus)
    object_builder.new_bus_bar_section(network, south_bus)

    # Create bus tie
    _create_bus_tie(network, substation, north_bus, south_bus, base_voltage)

    return {
        'network': network,
        'substation': substation,
        'north_bus': north_bus,
        'south_bus': south_bus,
        'base_voltage': base_voltage
    }


def _create_bus_tie(
    network: GraphModel,
    substation: cim.Substation,
    north_bus: cim.ConnectivityNode,
    south_bus: cim.ConnectivityNode,
    base_voltage: cim.BaseVoltage
) -> None:
    """Create a bus tie between north and south buses."""
    cim_profile, cim_module = get_cim_profile()
    cim_mod = cim_module

    # Create junction nodes
    junction1 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_bt_j1',
        ConnectivityNodeContainer=substation
    )
    junction2 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_bt_j2',
        ConnectivityNodeContainer=substation
    )

    # Create switching equipment
    airgap1 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_bt1',
        node1=north_bus, node2=junction1
    )
    bus_tie = object_builder.new_breaker(
        network, substation,
        name=f'{substation.name}_bus_tie',
        node1=junction1, node2=junction2
    )
    airgap2 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_bt2',
        node1=junction2, node2=south_bus
    )

    # Set base voltage
    airgap1.BaseVoltage = base_voltage
    bus_tie.BaseVoltage = base_voltage
    airgap2.BaseVoltage = base_voltage

    # Add to graph
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)


def add_branch_to_double_bus_single_breaker(
    network: GraphModel,
    substation: cim.Substation,
    north_bus: cim.ConnectivityNode,
    south_bus: cim.ConnectivityNode,
    base_voltage: cim.BaseVoltage,
    breaker_number: int,
    branch_equipment: cim.ConductingEquipment,
    branch_terminal: cim.Terminal | int
) -> None:
    """
    Add a branch connection to a double bus single breaker substation.

    Args:
        network: Graph model containing the substation
        substation: The substation object
        north_bus: The north bus connectivity node
        south_bus: The south bus connectivity node
        base_voltage: Base voltage object
        breaker_number: Identifier number for the branch breaker
        branch_equipment: Branch equipment to be connected
        branch_terminal: Terminal or terminal index of the branch equipment
    """
    cim_profile, cim_module = get_cim_profile()
    cim_mod = cim_module

    # Create junction nodes
    junction1 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{breaker_number}_j1',
        ConnectivityNodeContainer=substation
    )
    junction2 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{breaker_number}_j2',
        ConnectivityNodeContainer=substation
    )
    junction3 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{breaker_number}_j3',
        ConnectivityNodeContainer=substation
    )

    # Create switching equipment
    breaker = object_builder.new_breaker(
        network, substation,
        name=f'{substation.name}_{breaker_number}',
        node1=junction1, node2=junction2
    )
    airgap1 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{breaker_number+1}',
        node1=north_bus, node2=junction1
    )
    airgap2 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{breaker_number+2}',
        node1=junction2, node2=junction3
    )
    airgap3 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{breaker_number+3}',
        node1=junction3, node2=south_bus
    )

    # Set base voltage
    breaker.BaseVoltage = base_voltage
    airgap1.BaseVoltage = base_voltage
    airgap2.BaseVoltage = base_voltage
    airgap3.BaseVoltage = base_voltage

    # Connect branch terminal
    if isinstance(branch_terminal, cim_mod.Terminal):
        branch_terminal.ConnectivityNode = junction3

    # Add to graph
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)
    network.add_to_graph(junction3)


def add_feeder_to_double_bus_single_breaker(
    network: GraphModel,
    substation: cim.Substation,
    north_bus: cim.ConnectivityNode,
    south_bus: cim.ConnectivityNode,
    base_voltage: cim.BaseVoltage,
    breaker_number: int,
    feeder_network: GraphModel,
    feeder: cim.Feeder,
    sourcebus: cim.ConnectivityNode = None
) -> None:
    """
    Add a feeder connection to a double bus single breaker substation.

    Args:
        network: Graph model containing the substation
        substation: The substation object
        north_bus: The north bus connectivity node
        south_bus: The south bus connectivity node
        base_voltage: Base voltage object
        breaker_number: Identifier number for the feeder breaker
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

    # Create junction node
    junction1 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{breaker_number}_j1',
        ConnectivityNodeContainer=substation
    )

    # Create switching equipment
    breaker = object_builder.new_breaker(
        network, substation,
        name=f'{substation.name}_{breaker_number}',
        node1=junction1, node2=sourcebus
    )
    airgap1 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{breaker_number+1}',
        node1=north_bus, node2=junction1
    )
    airgap2 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{breaker_number+2}',
        node1=junction1, node2=south_bus
    )

    # Set base voltage
    breaker.BaseVoltage = base_voltage
    airgap1.BaseVoltage = base_voltage
    airgap2.BaseVoltage = base_voltage

    # Configure normally open disconnector (alternate between north and south)
    if breaker_number % 2 == 0:
        airgap1.open = True
        airgap1.normalOpen = True
    else:
        airgap2.open = True
        airgap2.normalOpen = True

    # Configure feeder-substation relationship
    feeder.NormalEnergizingSubstation = substation
    sourcebus.AdditionalEquipmentContainer = substation
    substation.NormalEnergizedFeeder.append(feeder)

    # Add to graph
    network.add_to_graph(junction1)
    network.add_to_graph(sourcebus)
    network.add_to_graph(feeder)
    feeder_network.add_to_graph(substation)
