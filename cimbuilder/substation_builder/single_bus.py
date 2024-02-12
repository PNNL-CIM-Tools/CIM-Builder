from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface
from cimgraph.models.graph_model import new_mrid #TODO: replace with utils
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

from cimbuilder.object_builder import new_breaker, new_disconnector

_log = logging.getLogger(__name__)


def new_single_bus(connection:ConnectionInterface, network:GraphModel = None, name:str = "new_sub"):
    
    # create substation
    substation_mrid = new_mrid()
    substation = cim.Substation(mRID = substation_mrid, name=name)

    if not network:
        network = DistributedArea(connection=connection, container=substation, distributed=False)

       
    # main bus
    main_bus = cim.ConnectivityNode(name="main_bus", mRID=new_mrid())
    main_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(main_bus)

    return network

def new_branch(network:GraphModel, substation:cim.Substation, main_bus:cim.ConnectivityNode, transfer_bus:cim.ConnectivityNode, 
               branch:cim.ConductingEquipment, sequenceNumber:int):

    junction1 = cim.ConnectivityNode(name=f"{substation.name}_{sequenceNumber}_j1", mRID = new_mrid(), ConnectivityNodeContainer=substation)
   
    breaker = new_breaker(network, substation, name = f"{substation.name}_{sequenceNumber}", node1 = main_bus, node2 = junction1)

    for terminal in branch.Terminals:
        if int(terminal.sequenceNumber) == 1:
            terminal.ConnectivityNode = junction1
        
    
    network.add_to_graph(junction1)
  