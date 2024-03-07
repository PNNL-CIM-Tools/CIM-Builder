from __future__ import annotations
import importlib
import logging

from cimgraph import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typing import


import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_two_terminal_object(network:GraphModel, container:cim.EquipmentContainer, class_type:type, 
                            name:str, node1:str|cim.ConnectivityNode, node2:str|cim.ConnectivityNode) -> object:

    new_object = class_type(name = name, mRID = utils.new_mrid())
    t1 = cim.Terminal(name=f"{name}_t1", mRID = utils.new_mrid(), sequenceNumber=1)
    t2 = cim.Terminal(name=f"{name}_t2", mRID = utils.new_mrid(), sequenceNumber=2)

    utils.terminal_to_node(network, t1, node1)
    utils.terminal_to_node(network, t2, node2)

    new_object.EquipmentContainer = container
    new_object.Terminals.append(t1)
    new_object.Terminals.append(t2)
    
    t1.ConductingEquipment = new_object
    t2.ConductingEquipment = new_object

    network.add_to_graph(new_object)
    network.add_to_graph(t1)
    network.add_to_graph(t2)

    #TODO: new_discrete()

    return new_object