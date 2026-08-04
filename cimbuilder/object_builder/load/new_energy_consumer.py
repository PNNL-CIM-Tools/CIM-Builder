from __future__ import annotations
import logging

from cimgraph.models import GraphModel
from cimgraph.databases import get_cim_profile
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

from cimbuilder.utils.utils import terminal_to_node

_log = logging.getLogger(__name__)

def new_energy_consumer(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node:str|cim.ConnectivityNode, p:float = 0, q:float = 0) -> None:
    
    cim_profile, cim_module = get_cim_profile()
    cim:cim = cim_module

    load = cim.EnergyConsumer(name = name)

    t1 = cim.Terminal()
    t1.uuid(name=f"{name}_t1")
    t1.sequenceNumber=1
    t1.ConductingEquipment = load
    terminal_to_node(network, t1, node)

    load.EquipmentContainer = container
    load.p = p
    load.q = q
    load.Terminals.append(t1)

    
 

    network.add_to_graph(load)
    network.add_to_graph(t1)


    return load