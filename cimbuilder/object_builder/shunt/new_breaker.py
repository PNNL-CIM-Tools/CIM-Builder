from __future__ import annotations
import logging

from cimgraph.models import GraphModel

import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typing import

import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_breaker(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node1:str|cim.ConnectivityNode, node2:str|cim.ConnectivityNode,
                open:bool=False, normalOpen:bool=False, retained:bool=True) -> cim.Breaker:
    
    cim = network.cim


    breaker = cim.Breaker(name = name)
    breaker.uuid(name=name, seed=str(node1)+str(node2))
    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t2 = cim.Terminal(name=f"{name}_t2", sequenceNumber=2)

    utils.terminal_to_node(network, t1, node1)
    utils.terminal_to_node(network, t2, node2)

    breaker.EquipmentContainer = container
    breaker.open = open
    breaker.normalOpen = normalOpen
    breaker.retained = retained
    breaker.Terminals.append(t1)
    breaker.Terminals.append(t2)
    
    t1.ConductingEquipment = breaker
    t2.ConductingEquipment = breaker

    network.add_to_graph(breaker)
    network.add_to_graph(t1)
    network.add_to_graph(t2)

    #TODO: new_discrete()

    return breaker