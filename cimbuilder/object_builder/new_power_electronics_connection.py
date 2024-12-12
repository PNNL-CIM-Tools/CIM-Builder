from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel
from cimgraph.databases import ConnectionInterface
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

from cimbuilder.utils.utils import terminal_to_node

_log = logging.getLogger(__name__)

def new_power_electronics_connection(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node:str|cim.ConnectivityNode, p:float = 0, q:float = 0) -> None:

    inverter = cim.PowerElectronicsConnection(name = name)

    t1 = cim.Terminal()
    t1.uuid(name=f"{name}_t1")
    t1.sequenceNumber=1
    t1.ConductingEquipment = inverter
    terminal_to_node(network, t1, node)

    inverter.EquipmentContainer = container
    inverter.p = p
    inverter.q = q
    inverter.Terminals.append(t1)

    network.add_to_graph(inverter)
    network.add_to_graph(t1)


    #TODO: new_discrete()

    return inverter