from __future__ import annotations

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface, get_cim_profile
import cimgraph.data_profile.cimhub_2023 as cim

from cimbuilder import object_builder
import cimbuilder.utils as utils

import logging
_log = logging.getLogger(__name__)


def new_main_and_transfer_substation(
    connection: ConnectionInterface,
    name: str = 'new_main_transfer_sub',
    base_voltage: int | cim.BaseVoltage = 115000,
    network: GraphModel = None
) -> dict:
    """
    Create a main-and-transfer bus substation in node-breaker representation.

    This substation topology features a main bus and a transfer bus connected by a bus tie.
    It allows for equipment maintenance without service interruption by transferring
    loads to the transfer bus during maintenance operations.

    Args:
        connection: Connection interface to the CIM database
        name: Name of the substation
        base_voltage: Base voltage in volts or a BaseVoltage object
        network: Optional existing network to add the substation to

    Returns:
        Dictionary with keys: 'network', 'substation', 'main_bus', 'transfer_bus', 'base_voltage'
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

    # Create main bus
    main_bus = cim_mod.ConnectivityNode(name=f'{name}_main_bus')
    main_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(main_bus)
    object_builder.new_bus_bar_section(network, main_bus)

    # Create transfer bus
    transfer_bus = cim_mod.ConnectivityNode(name=f'{name}_transfer_bus')
    transfer_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(transfer_bus)
    object_builder.new_bus_bar_section(network, transfer_bus)

    # Create bus tie between main and transfer buses
    _create_bus_tie(network, substation, main_bus, transfer_bus, base_voltage)

    return {
        'network': network,
        'substation': substation,
        'main_bus': main_bus,
        'transfer_bus': transfer_bus,
        'base_voltage': base_voltage
    }


def _create_bus_tie(
    network: GraphModel,
    substation: cim.Substation,
    main_bus: cim.ConnectivityNode,
    transfer_bus: cim.ConnectivityNode,
    base_voltage: cim.BaseVoltage
) -> None:
    """
    Create a bus tie between main and transfer buses.

    The bus tie consists of two disconnectors and a breaker,
    connected in series with two junction nodes.
    """
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
        node1=main_bus, node2=junction1
    )
    bus_tie = object_builder.new_breaker(
        network, substation,
        name=f'{substation.name}_bus_tie',
        node1=junction1, node2=junction2
    )
    airgap2 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_bt2',
        node1=junction2, node2=transfer_bus
    )

    # Set base voltage
    airgap1.BaseVoltage = base_voltage
    bus_tie.BaseVoltage = base_voltage
    airgap2.BaseVoltage = base_voltage

    # Add to graph
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)


def add_branch_to_main_and_transfer(
    network: GraphModel,
    substation: cim.Substation,
    main_bus: cim.ConnectivityNode,
    transfer_bus: cim.ConnectivityNode,
    base_voltage: cim.BaseVoltage,
    breaker_number: int,
    branch_equipment: cim.ConductingEquipment,
    branch_terminal: cim.Terminal | int
) -> None:
    """
    Add a branch connection to a main-and-transfer bus substation.

    The branch connection consists of a breaker and three disconnectors arranged to allow
    the branch to be connected to either the main bus or the transfer bus.

    Args:
        network: Graph model containing the substation
        substation: The substation object
        main_bus: The main bus connectivity node
        transfer_bus: The transfer bus connectivity node
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
        name=f'{substation.name}_{10*breaker_number + 1}',
        node1=main_bus, node2=junction1
    )
    airgap2 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{10*breaker_number + 2}',
        node1=junction2, node2=junction3
    )
    airgap3 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{10*breaker_number + 3}',
        node1=junction3, node2=transfer_bus
    )

    # Set base voltage
    breaker.BaseVoltage = base_voltage
    airgap1.BaseVoltage = base_voltage
    airgap2.BaseVoltage = base_voltage
    airgap3.BaseVoltage = base_voltage

    # Connect branch terminal
    if isinstance(branch_terminal, cim_mod.Terminal):
        branch_terminal.ConnectivityNode = junction3
    elif isinstance(branch_terminal, int):
        branch_equipment.Terminals[branch_terminal].ConnectivityNode = junction3

    # Add to graph
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)
    network.add_to_graph(junction3)


def add_feeder_to_main_and_transfer(
    network: GraphModel,
    substation: cim.Substation,
    main_bus: cim.ConnectivityNode,
    transfer_bus: cim.ConnectivityNode,
    base_voltage: cim.BaseVoltage,
    series_number: int,
    feeder_network: GraphModel,
    feeder: cim.Feeder,
    sourcebus: cim.ConnectivityNode = None
) -> None:
    """
    Add a feeder connection to a main-and-transfer bus substation.

    The feeder connection includes a breaker and disconnectors to allow for
    connection to either the main bus or transfer bus.

    Args:
        network: Graph model containing the substation
        substation: The substation object
        main_bus: The main bus connectivity node
        transfer_bus: The transfer bus connectivity node
        base_voltage: Base voltage object
        series_number: Identifier number for the feeder connection
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

    # Create junction nodes
    junction1 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{10*series_number}_j1',
        ConnectivityNodeContainer=substation
    )
    junction2 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{10*series_number}_j2',
        ConnectivityNodeContainer=substation
    )

    # Create switching equipment
    breaker = object_builder.new_breaker(
        network, substation,
        name=f'{substation.name}_{10*series_number}',
        node1=junction1, node2=junction2
    )
    airgap1 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{10*series_number + 1}',
        node1=main_bus, node2=junction1
    )
    airgap2 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{10*series_number + 2}',
        node1=junction2, node2=sourcebus
    )
    airgap3 = object_builder.new_disconnector(
        network, substation,
        name=f'{substation.name}_{10*series_number + 3}',
        node1=sourcebus, node2=transfer_bus,
        open=True, normalOpen=True
    )

    # Set base voltage
    breaker.BaseVoltage = base_voltage
    airgap1.BaseVoltage = base_voltage
    airgap2.BaseVoltage = base_voltage
    airgap3.BaseVoltage = base_voltage

    # Configure feeder-substation relationship
    feeder.NormalEnergizingSubstation = substation
    substation.NormalEnergizedFeeder.append(feeder)

    # Add to graph
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)
    network.add_to_graph(sourcebus)
    network.add_to_graph(feeder)
