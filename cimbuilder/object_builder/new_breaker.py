from __future__ import annotations
import importlib
import logging

from cimgraph import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typing import

import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_breaker(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node1:str|cim.ConnectivityNode, node2:str|cim.ConnectivityNode,
                open:bool=False, normalOpen:bool=False, retained:bool=True) -> cim.Breaker:

    breaker = cim.Breaker(name = name, mRID = utils.new_mrid())
    t1 = cim.Terminal(name=f"{name}.1", mRID = utils.new_mrid(), sequenceNumber=1)
    t2 = cim.Terminal(name=f"{name}.2", mRID = utils.new_mrid(), sequenceNumber=2)

    utils.terminal_to_node(network, t1, node1)
    utils.terminal_to_node(network, t2, node2)

    breaker.EquipmentContainer = container
    breaker.open = open
    breaker.normalOpen = normalOpen
    breaker.Terminals.append(t1)
    breaker.Terminals.append(t2)
    
    t1.ConductingEquipment = breaker
    t2.ConductingEquipment = breaker

    network.add_to_graph(breaker)
    network.add_to_graph(t1)
    network.add_to_graph(t2)

    #TODO: new_discrete()

    return breaker