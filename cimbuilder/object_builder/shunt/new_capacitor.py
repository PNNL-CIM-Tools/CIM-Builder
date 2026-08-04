
from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel
from cimgraph.databases import ConnectionInterface
# from cimgraph.models.graph_model import new_mrid #TODO: replace with utils
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

from cimbuilder.utils.utils import terminal_to_node

_log = logging.getLogger(__name__)

def new_capacitor(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node:str|cim.ConnectivityNode, sectionNumber:float = 0, b:float = 0, b0:float = 0, g:float = 0, g0:float = 0) -> None:

    
    # capacitor = cim.NonlinearShuntCompensatorPoint(name = name, mRID = new_mrid())
    capacitor = cim.LinearShuntCompensator(name = name)

    t1 = cim.Terminal(name=f"{name}_t1",  sequenceNumber=1)
    t1.ConductingEquipment = capacitor
    terminal_to_node(network, t1, node)

    capacitor.EquipmentContainer = container
    capacitor.sectionNumber = sectionNumber
    capacitor.b = b
    capacitor.b0 = b0
    capacitor.g = g
    capacitor.g0 = g0
    capacitor.Terminals.append(t1)

    
 

    network.add_to_graph(capacitor)
    network.add_to_graph(t1)


    #TODO: new_discrete()

    return capacitor