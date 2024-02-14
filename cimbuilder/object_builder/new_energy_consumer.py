from __future__ import annotations
import importlib
import logging

from cimgraph import GraphModel
from cimgraph.databases import ConnectionInterface
from cimgraph.models.graph_model import new_mrid #TODO: replace with utils
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

from cimbuilder.utils.utils import terminal_to_node

_log = logging.getLogger(__name__)

def new_energy_consumer(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node:str|cim.ConnectivityNode, p:float = 0, q:float = 0) -> None:

    load = cim.EnergyConsumer(name = name, mRID = new_mrid())

    t1 = cim.Terminal(name=f"{name}_t1", mRID = new_mrid(), sequenceNumber=1)
    t1.ConductingEquipment = load
    terminal_to_node(network, t1, node)

    load.EquipmentContainer = container
    load.p = p
    load.q = q
    load.Terminals.append(t1)

    
 

    network.add_to_graph(load)
    network.add_to_graph(t1)


    #TODO: new_discrete()

    return load