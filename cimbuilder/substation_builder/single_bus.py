from __future__ import annotations

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface, get_cim_profile
import cimgraph.data_profile.cimhub_2023 as cim

import cimbuilder.object_builder as object_builder
import cimbuilder.utils as utils

import logging
_log = logging.getLogger(__name__)


def new_single_bus_substation(
    connection: ConnectionInterface,
    name: str = 'new_single_bus_sub',
    base_voltage: int | cim.BaseVoltage = 115000,
    network: GraphModel = None
) -> dict:
    """
    Create a single bus substation in node-breaker representation.

    Args:
        connection: Connection interface to the CIM database
        name: Name of the substation
        base_voltage: Base voltage in volts or a BaseVoltage object
        network: Optional existing network to add the substation to

    Returns:
        Dictionary with keys: 'network', 'substation', 'main_bus', 'base_voltage'
    """
    cim_profile, cim_module = get_cim_profile()
    cim_mod = cim_module

    # Create substation
    substation = cim_mod.Substation(name=name)

    # Create or use existing network
    if not network:
        network = DistributedArea(connection=connection, container=substation)
    network.add_to_graph(substation)

    # Get or create base voltage
    base_voltage = utils.get_base_voltage(network, base_voltage)

    # Create main bus
    main_bus = cim_mod.ConnectivityNode(name=f'{name}_main_bus')
    main_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(main_bus)
    object_builder.new_bus_bar_section(network, main_bus)

    return {
        'network': network,
        'substation': substation,
        'main_bus': main_bus,
        'base_voltage': base_voltage
    }


def add_branch_to_single_bus(
    network: GraphModel,
    substation: cim.Substation,
    main_bus: cim.ConnectivityNode,
    base_voltage: cim.BaseVoltage,
    breaker_number: int,
    branch_equipment: cim.ConductingEquipment,
    branch_terminal: cim.Terminal | int
) -> None:
    """
    Add a branch connection to a single bus substation.

    Args:
        network: Graph model containing the substation
        substation: The substation object
        main_bus: The main bus connectivity node
        base_voltage: Base voltage object
        breaker_number: Identifier number for the branch breaker
        branch_equipment: Branch equipment to be connected
        branch_terminal: Terminal or terminal index of the branch equipment
    """
    cim_profile, cim_module = get_cim_profile()
    cim_mod = cim_module

    junction1 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{breaker_number}_j1',
        ConnectivityNodeContainer=substation
    )

    breaker = object_builder.new_breaker(
        network, substation,
        name=f"{substation.name}_{breaker_number}",
        node1=main_bus, node2=junction1
    )
    breaker.BaseVoltage = base_voltage

    if isinstance(branch_terminal, cim_mod.Terminal):
        branch_terminal.ConnectivityNode = junction1

    network.add_to_graph(junction1)


def add_feeder_to_single_bus(
    network: GraphModel,
    substation: cim.Substation,
    main_bus: cim.ConnectivityNode,
    base_voltage: cim.BaseVoltage,
    breaker_number: int,
    feeder_network: GraphModel,
    feeder: cim.Feeder,
    sourcebus: cim.ConnectivityNode = None
) -> None:
    """
    Add a feeder connection to a single bus substation.

    Args:
        network: Graph model containing the substation
        substation: The substation object
        main_bus: The main bus connectivity node
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

    # Create junction nodes
    junction1 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{breaker_number}_j1',
        ConnectivityNodeContainer=substation
    )
    junction2 = cim_mod.ConnectivityNode(
        name=f'{substation.name}_{breaker_number}_j2',
        ConnectivityNodeContainer=substation
    )

    # Create switching equipment
    breaker = object_builder.new_breaker(
        network, container=substation,
        name=f'{substation.name}_{breaker_number}',
        node1=junction1, node2=junction2
    )
    airgap1 = object_builder.new_disconnector(
        network, container=substation,
        name=f'{substation.name}_{breaker_number+1}',
        node1=main_bus, node2=junction1
    )
    airgap2 = object_builder.new_disconnector(
        network, container=substation,
        name=f'{substation.name}_{breaker_number+2}',
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
