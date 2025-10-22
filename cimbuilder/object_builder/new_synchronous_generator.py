from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel
from cimgraph.databases import ConnectionInterface
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

from cimbuilder.utils.utils import terminal_to_node

_log = logging.getLogger(__name__)

def new_synchronous_generator(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node:str|cim.ConnectivityNode, p:float = 0, q:float = 0, ratedS:float = 0, ratedU:float = 0) -> None:

    synchr_generator = cim.SynchronousMachine(name = name)

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.ConductingEquipment = synchr_generator
    terminal_to_node(network, t1, node)

    synchr_generator.EquipmentContainer = container
    synchr_generator.p = p
    synchr_generator.q = q
    synchr_generator.ratedS = ratedS
    synchr_generator.ratedU = ratedU
    synchr_generator.Terminals.append(t1)

    
 

    network.add_to_graph(synchr_generator)
    network.add_to_graph(t1)


    #TODO: new_discrete()

    return synchr_generator