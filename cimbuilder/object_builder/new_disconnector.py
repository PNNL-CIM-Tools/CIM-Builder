from __future__ import annotations
import logging

from cimgraph import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

import cimbuilder.utils as utils
 
def new_disconnector(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node1:str|cim.ConnectivityNode, node2:str|cim.ConnectivityNode,
                open:bool=False, normalOpen:bool=False, retained:bool=False) -> None:

    disconnector = cim.Disconnector(name = name, mRID = utils.new_mrid())
    t1 = cim.Terminal(name=f"{name}.1", mRID = utils.new_mrid(), sequenceNumber=1)
    t2 = cim.Terminal(name=f"{name}.2", mRID = utils.new_mrid(), sequenceNumber=2)

    utils.terminal_to_node(network, t1, node1)
    utils.terminal_to_node(network, t2, node2)

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
