from __future__ import annotations

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface, get_cim_profile
import cimgraph.data_profile.cimhub_2023 as cim

from cimbuilder import object_builder
import cimbuilder.utils as utils

import logging
_log = logging.getLogger(__name__)


def new_breaker_and_a_half_substation(
    connection: ConnectionInterface,
    name: str = 'new_breaker_and_half_bus_sub',
    base_voltage: int | cim.BaseVoltage = 115000,
    total_bus_ties: int = 2,
    network: GraphModel = None
) -> dict:
    """
    Create a breaker-and-a-half substation in node-breaker representation.

    This topology features two main buses with breaker strings between them,
    where each string contains three breakers (hence "breaker and a half" per connection).

    Args:
        connection: Connection interface to the CIM database
        name: Name of the substation
        base_voltage: Base voltage in volts or a BaseVoltage object
        total_bus_ties: Number of breaker strings to create
        network: Optional existing network to add the substation to

    Returns:
        Dictionary with keys: 'network', 'substation', 'main_bus_1', 'main_bus_2', 'base_voltage', 'total_bus_ties'
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

    # Create main bus 1
    main_bus_1 = cim_mod.ConnectivityNode(name=f'{name}_main_bus_1')
    main_bus_1.ConnectivityNodeContainer = substation
    network.add_to_graph(main_bus_1)
    object_builder.new_bus_bar_section(network, main_bus_1)

    # Create main bus 2
    main_bus_2 = cim_mod.ConnectivityNode(name=f'{name}_main_bus_2')
    main_bus_2.ConnectivityNodeContainer = substation
    network.add_to_graph(main_bus_2)
    object_builder.new_bus_bar_section(network, main_bus_2)

    # Create bus ties (breaker strings)
    for tie in range(total_bus_ties):
        _create_bus_tie(network, substation, main_bus_1, main_bus_2, tie, name, base_voltage)

    return {
        'network': network,
        'substation': substation,
        'main_bus_1': main_bus_1,
        'main_bus_2': main_bus_2,
        'base_voltage': base_voltage,
        'total_bus_ties': total_bus_ties
    }


def _create_bus_tie(
    network: GraphModel,
    substation: cim.Substation,
    main_bus_1: cim.ConnectivityNode,
    main_bus_2: cim.ConnectivityNode,
    tie_number: int,
    substation_name: str,
    base_voltage: cim.BaseVoltage
) -> None:
    """
    Create a breaker string (bus tie) between the two main buses.

    Each string contains 3 breakers and 8 junctions, forming the breaker-and-a-half configuration.
    """
    cim_profile, cim_module = get_cim_profile()
    cim_mod = cim_module

    # Create junction nodes
    junctions = []
    for i in range(8):
        junction = cim_mod.ConnectivityNode(
            name=f'{substation.name}_{tie_number}_bt_j{i + 1}',
            ConnectivityNodeContainer=substation
        )
        junctions.append(junction)

    tie_number_base = 10 * tie_number

    # Create first breaker section
    bus_tie_1 = object_builder.new_breaker(
        network, substation,
        name=f'{substation_name}_bt_{tie_number_base}',
        node1=junctions[0], node2=junctions[1]
    )
    airgap1 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation_name}_bt_{10 + tie_number_base + 1}',
        node1=main_bus_1, node2=junctions[0]
    )
    airgap2 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation_name}_bt_{10 + tie_number_base + 2}',
        node1=junctions[1], node2=junctions[2]
    )

    # Create second breaker section
    bus_tie_2 = object_builder.new_breaker(
        network, substation,
        name=f'{substation_name}_bt_{2 * tie_number_base}',
        node1=junctions[3], node2=junctions[4]
    )
    airgap3 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation_name}_bt_{20 + tie_number_base + 1}',
        node1=junctions[2], node2=junctions[3]
    )
    airgap4 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation_name}_bt_{20 + tie_number_base + 2}',
        node1=junctions[4], node2=junctions[5]
    )

    # Create third breaker section
    bus_tie_3 = object_builder.new_breaker(
        network, substation,
        name=f'{substation_name}_bt_{3 * tie_number_base}',
        node1=junctions[6], node2=junctions[7]
    )
    airgap5 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation_name}_bt_{30 + tie_number_base + 1}',
        node1=junctions[5], node2=junctions[6]
    )
    airgap6 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation_name}_bt_{30 + tie_number_base + 2}',
        node1=junctions[7], node2=main_bus_2
    )

    # Set base voltage for all equipment
    for equip in [bus_tie_1, bus_tie_2, bus_tie_3, airgap1, airgap2, airgap3, airgap4, airgap5, airgap6]:
        equip.BaseVoltage = base_voltage

    # Add all junctions to graph
    for junction in junctions:
        network.add_to_graph(junction)


def add_branch_to_breaker_and_a_half(
    network: GraphModel,
    substation: cim.Substation,
    base_voltage: cim.BaseVoltage,
    breaker_number: int,
    tie_number: int,
    branch_equipment: cim.ConductingEquipment,
    branch_terminal: cim.Terminal | int
) -> None:
    """
    Add a branch connection to a breaker-and-a-half substation.

    Args:
        network: Graph model containing the substation
        substation: The substation object
        base_voltage: Base voltage object
        breaker_number: Identifier number for the branch
        tie_number: Bus tie number to connect to
        branch_equipment: Branch equipment to be connected
        branch_terminal: Terminal or terminal index of the branch equipment
    """
    cim_profile, cim_module = get_cim_profile()
    cim_mod = cim_module

    # Determine connection point based on breaker number
    if breaker_number % 2 == 0:
        jcn_name = f'{substation.name}_{tie_number}_bt_j6'
        jcn_num = 2
    else:
        jcn_name = f'{substation.name}_{tie_number}_bt_j3'
        jcn_num = 1

    # Create junction node
    junction1 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{breaker_number}_j{jcn_num}',
        ConnectivityNodeContainer=substation
    )

    # Create disconnector
    airgap1 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{10 * breaker_number}',
        node1=jcn_name, node2=junction1
    )
    airgap1.BaseVoltage = base_voltage

    # Connect branch terminal
    branch_terminal.ConnectivityNode = junction1

    # Add to graph
    network.add_to_graph(junction1)


def add_feeder_to_breaker_and_a_half(
    network: GraphModel,
    substation: cim.Substation,
    base_voltage: cim.BaseVoltage,
    breaker_number: int,
    tie_number: int,
    feeder_network: GraphModel,
    feeder: cim.Feeder,
    sourcebus: cim.ConnectivityNode = None
) -> None:
    """
    Add a feeder connection to a breaker-and-a-half substation.

    Args:
        network: Graph model containing the substation
        substation: The substation object
        base_voltage: Base voltage object
        breaker_number: Identifier number for the feeder
        tie_number: Bus tie number to connect to
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

    # Determine connection point based on breaker number
    if breaker_number % 2 == 0:
        jcn_name = f'{substation.name}_{tie_number}_bt_j6'
    else:
        jcn_name = f'{substation.name}_{tie_number}_bt_j3'

    # Create disconnector
    airgap1 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{10 * breaker_number}',
        node1=jcn_name, node2=sourcebus
    )
    airgap1.BaseVoltage = base_voltage

    # Configure feeder-substation relationship
    feeder.NormalEnergizingSubstation = substation
    substation.NormalEnergizedFeeder.append(feeder)

    # Add to graph
    network.add_to_graph(sourcebus)
    network.add_to_graph(feeder)
    feeder_network.add_to_graph(substation)
