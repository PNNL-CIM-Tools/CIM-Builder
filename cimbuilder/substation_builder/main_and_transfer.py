from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface
from cimgraph.models.graph_model import new_mrid #TODO: replace with utils
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

import cimbuilder.object_builder as object_builder

_log = logging.getLogger(__name__)


def new_main_and_transfer(connection:ConnectionInterface, network:GraphModel = None, name:str = 'new_sub'):
    # cim = connection.cim_profile
    # create substation
    substation_mrid = new_mrid()
    substation = cim.Substation(mRID = substation_mrid, name=name)

    if not network:
        network = DistributedArea(connection=connection, container=substation, distributed=False)

       

    # main bus
    main_bus = cim.ConnectivityNode(name=f'{name}_main_bus', mRID=new_mrid())
    main_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(main_bus)
    object_builder.new_bus_bar_section(network, main_bus)

    # transfer bus
    transfer_bus = cim.ConnectivityNode(name=f'{name}_transfer_bus', mRID=new_mrid())
    transfer_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(transfer_bus)
    object_builder.new_bus_bar_section(network, transfer_bus)

    # create bus_tie
    new_bus_tie(network, substation, main_bus, transfer_bus)

    return network, substation, main_bus, transfer_bus

def new_bus_tie(network:GraphModel, substation:cim.Substation, main_bus:cim.ConnectivityNode, transfer_bus:cim.ConnectivityNode):
    #cim = network.connection.cim_profile
    junction1 = cim.ConnectivityNode(name=f'{substation.name}_bt_j1', mRID = new_mrid(), ConnectivityNodeContainer=substation)
    junction2 = cim.ConnectivityNode(name=f'{substation.name}_bt_j2', mRID = new_mrid(), ConnectivityNodeContainer=substation)
    airgap1 = object_builder.new_disconnector(network, substation, name = f'{substation.name}_bt1', node1 = main_bus, node2 = junction1)
    bus_tie = object_builder.new_breaker(network, substation, name = f'{substation.name}_bus_tie', node1 = junction1, node2 = junction2)
    airgap2 = object_builder.new_disconnector(network, substation, name = f'{substation.name}_bt1', node1 = junction2, node2 = transfer_bus)
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)
    
def new_main_trans_branch(network:GraphModel, substation:cim.Substation, main_bus:cim.ConnectivityNode, transfer_bus:cim.ConnectivityNode, 
               series_number:int, branch_equipment:cim.ConductingEquipment, branch_terminal:cim.Terminal|int) -> None:
    cim_profile = network.connection.connection_params.cim_profile
    cim = importlib.import_module(f'cimgraph.data_profile.{cim_profile}')

    junction1 = cim.ConnectivityNode(name=f'{substation.name}_{series_number}_j1', mRID = new_mrid(), ConnectivityNodeContainer=substation)
    junction2 = cim.ConnectivityNode(name=f'{substation.name}_{series_number}_j2', mRID = new_mrid(), ConnectivityNodeContainer=substation)
    junction3 = cim.ConnectivityNode(name=f'{substation.name}_{series_number}_j3', mRID = new_mrid(), ConnectivityNodeContainer=substation)

    breaker = object_builder.new_breaker(network, substation, name = f'{substation.name}_{series_number}', node1 = junction1, node2 = junction2)

    airgap1 = object_builder.new_disconnector(network, substation, name = f'{substation.name}_{series_number+1}', node1 = main_bus, node2 = junction1)
    airgap2 = object_builder.new_disconnector(network, substation, name = f'{substation.name}_{series_number+2}', node1 = junction2, node2 = junction3)
    airgap3 = object_builder.new_disconnector(network, substation, name = f'{substation.name}_{series_number+3}', node1 = junction3, node2 = transfer_bus)

    if type(branch_terminal) == cim.Terminal:
        branch_terminal.ConnectivityNode = junction3
    
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)
    network.add_to_graph(junction3)

       
def new_main_trans_feeder(network:GraphModel, substation:cim.Substation, feeder:cim.Feeder, series_number:int,
                          main_bus:cim.ConnectivityNode = None, transfer_bus:cim.ConnectivityNode = None, 
                          sourcebus:cim.ConnectivityNode=None) -> None:
    
    cim_profile = network.connection.connection_params.cim_profile
    cim = importlib.import_module(f'cimgraph.data_profile.{cim_profile}')

    if not main_bus: # If node not specified, look for something named main_bus
        for node in network.graph[cim.ConnectivityNode].values():
            if node.name == 'main_bus' or node.name == f'{substation.name}_main_bus':
                main_bus = node

    if not transfer_bus: # If node not specified, look for something named main_bus
        for node in network.graph[cim.ConnectivityNode].values():
            if node.name == 'main_bus' or node.name == f'{substation.name}_main_bus':
                main_bus = node

    if not sourcebus:
        pass

    junction1 = cim.ConnectivityNode(name=f'{substation.name}_{series_number}_j1', mRID = new_mrid(), ConnectivityNodeContainer=substation)
    junction2 = cim.ConnectivityNode(name=f'{substation.name}_{series_number}_j2', mRID = new_mrid(), ConnectivityNodeContainer=substation)
    # junction3 = cim.ConnectivityNode(name=f'{substation.name}_{series_number}_j3', mRID = new_mrid(), ConnectivityNodeContainer=substation)

    breaker = object_builder.new_breaker(network, substation, name = f'{substation.name}_{series_number}', node1 = junction1, node2 = junction2)
    airgap1 = object_builder.new_disconnector(network, substation, name = f'{substation.name}_{series_number+1}', node1 = main_bus, node2 = junction1)
    airgap2 = object_builder.new_disconnector(network, substation, name = f'{substation.name}_{series_number+2}', node1 = junction2, node2 = sourcebus)
    airgap3 = object_builder.new_disconnector(network, substation, name = f'{substation.name}_{series_number+3}', node1 = sourcebus, node2 = transfer_bus)
    airgap3.open = True
    airgap3.normalOpen = True

    feeder.NormalEnergizingSubstation = substation
    sourcebus.AdditionalEquipmentContainer = substation

    network.add_to_graph(junction1)
    network.add_to_graph(junction2)
    network.add_to_graph(sourcebus)
    network.add_to_graph(feeder)
