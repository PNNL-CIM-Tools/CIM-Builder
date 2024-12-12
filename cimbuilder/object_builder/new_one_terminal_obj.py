from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_one_terminal_object(network:GraphModel, container:cim.EquipmentContainer, class_type:type,
                             name:str, node:str|cim.ConnectivityNode) -> object:

    cim = network.connection.cim
    new_object = class_type()
    new_object.uuid(name = name)

    t1 = cim.Terminal()
    t1.uuid(name=f"{name}_t1")
    t1.sequenceNumber=1
    t1.ConductingEquipment = new_object
    utils.terminal_to_node(network, t1, node)

    new_object.EquipmentContainer = container
    new_object.Terminals.append(t1)

    network.add_to_graph(new_object)
    network.add_to_graph(t1)

    return new_object