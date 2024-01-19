from __future__ import annotations
import importlib
import logging

from cimgraph import GraphModel
from cimgraph.databases import ConnectionInterface
from cimgraph.models.graph_model import new_mrid #TODO: replace with utils
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

from cimbuilder.object_builder.utils import terminal_to_node

def new_disconnector(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node1:str|cim.ConnectivityNode, node2:str|cim.ConnectivityNode,
                open:bool=False, normalOpen:bool=False, retained:bool=True) -> None:

    disconnector = cim.Disconnector(name = name, mRID = new_mrid())
    t1 = cim.Terminal(name=f"{name}.1", mRID = new_mrid(), sequenceNumber=1)
    t2 = cim.Terminal(name=f"{name}.2", mRID = new_mrid(), sequenceNumber=2)

    terminal_to_node(network, t1, node1)
    terminal_to_node(network, t2, node2)

    disconnector.EquipmentContainer = container
    disconnector.open = open
    disconnector.normalOpen = normalOpen
    disconnector.Terminals.append(t1)
    disconnector.Terminals.append(t2)
    
    t1.ConductingEquipment = disconnector
    t2.ConductingEquipment = disconnector

    network.add_to_graph(disconnector)
    network.add_to_graph(t1)
    network.add_to_graph(t2)
