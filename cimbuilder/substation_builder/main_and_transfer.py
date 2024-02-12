from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface
from cimgraph.models.graph_model import new_mrid #TODO: replace with utils
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

from cimbuilder.object_builder import new_breaker, new_disconnector

_log = logging.getLogger(__name__)


def new_main_and_transfer(connection:ConnectionInterface, network:GraphModel = None, name:str = "new_sub"):
    
    # create substation
    substation_mrid = new_mrid()
    substation = cim.Substation(mRID = substation_mrid, name=name)

    if not network:
        network = DistributedArea(connection=connection, container=substation, distributed=False)

       

    # main bus
    main_bus = cim.ConnectivityNode(name="main_bus", mRID=new_mrid())
    main_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(main_bus)

    # transfer bus
    transfer_bus = cim.ConnectivityNode(name="transfer_bus", mRID=new_mrid())
    transfer_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(transfer_bus)

    # create bus_tie
    new_bus_tie(network, substation, main_bus, transfer_bus)

    return network

def new_bus_tie(network:GraphModel, substation:cim.Substation, main_bus:cim.ConnectivityNode, transfer_bus:cim.ConnectivityNode):

    junction1 = cim.ConnectivityNode(name=f"{substation.name}_bt_j1", mRID = new_mrid(), ConnectivityNodeContainer=substation)
    junction2 = cim.ConnectivityNode(name=f"{substation.name}_bt_j2", mRID = new_mrid(), ConnectivityNodeContainer=substation)
    airgap1 = new_disconnector(network, substation, name = f'{substation.name}_bt1', node1 = main_bus, node2 = junction1)
    bus_tie = new_breaker(network, substation, name = f"{substation.name}_bus_tie", node1 = junction1, node2 = junction2)
    airgap2 = new_disconnector(network, substation, name = f'{substation.name}_bt1', node1 = junction2, node2 = transfer_bus)
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)
    

def new_main_trans_branch(network:GraphModel, substation:cim.Substation, main_bus:cim.ConnectivityNode, transfer_bus:cim.ConnectivityNode, 
               branch:cim.ConductingEquipment, sequenceNumber:int):

    junction1 = cim.ConnectivityNode(name=f"{substation.name}_{sequenceNumber}_j1", mRID = new_mrid(), ConnectivityNodeContainer=substation)
    junction2 = cim.ConnectivityNode(name=f"{substation.name}_{sequenceNumber}_j2", mRID = new_mrid(), ConnectivityNodeContainer=substation)
    junction3 = cim.ConnectivityNode(name=f"{substation.name}_{sequenceNumber}_j3", mRID = new_mrid(), ConnectivityNodeContainer=substation)

    breaker = new_breaker(network, substation, name = f"{substation.name}_{sequenceNumber}", node1 = junction1, node2 = junction2)

    airgap1 = new_disconnector(network, substation, name = f'{substation.name}_{sequenceNumber+1}', node1 = main_bus, node2 = junction1)
    airgap2 = new_disconnector(network, substation, name = f'{substation.name}_{sequenceNumber+2}', node1 = junction2, node2 = junction3)
    airgap3 = new_disconnector(network, substation, name = f'{substation.name}_{sequenceNumber+3}', node1 = junction3, node2 = transfer_bus)

    for terminal in branch.Terminals:
        if int(terminal.sequenceNumber) == 1:
            terminal.ConnectivityNode = junction3
        
    
    network.add_to_graph(junction1)
    network.add_to_graph(junction2)
    network.add_to_graph(junction3)