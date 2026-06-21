from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel 

import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

from cimbuilder.utils.utils import terminal_to_node

_log = logging.getLogger(__name__)

def new_tap_changer(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node:str|cim.ConnectivityNode, highStep:float = 0, lowStep:float = 0, initialDelay:float = 0) -> None:

    cim = network.cim


    regulator = cim.RatioTapChanger(name = name)

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    
    t1.ConductingEquipment = regulator

    terminal_to_node(network, t1, node)

    regulator.highStep = highStep
    regulator.lowStep = lowStep
    regulator.initialDelay = initialDelay



   
    regulator.Terminals.append(t1)

    
 

    network.add_to_graph(regulator)
    network.add_to_graph(t1)
    


    #TODO: new_discrete()

    return regulator