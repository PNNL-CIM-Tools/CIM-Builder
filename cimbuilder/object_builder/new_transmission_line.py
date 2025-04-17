from __future__ import annotations
import logging

from cimgraph.models import GraphModel
from cimgraph.databases import get_cim_profile
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

from cimbuilder.utils import terminal_to_node

_log = logging.getLogger(__name__)

def new_transmission_line(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node:str|cim.ConnectivityNode, length:float = 0, r:float = 0, x:float = 0, bch:float = 0, r0:float = 0, x0:float = 0, bch0:float = 0) -> None:

    cim_profile, cim_module = get_cim_profile()
    cim:cim = cim_module
    transmission_line = cim.ACLineSegment(name = name)

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t2 = cim.Terminal(name=f"{name}_t2", sequenceNumber=2)
    t1.ConductingEquipment = transmission_line 
    t2.ConductingEquipment = transmission_line 
    terminal_to_node(network, t1, node)

    transmission_line.EquipmentContainer = container
    transmission_line.length = length
    transmission_line.r = r
    transmission_line.x = x
    transmission_line.bch = bch
    transmission_line.r0 = r0
    transmission_line.x0 = x0
    transmission_line.bch0 = bch0


    
    transmission_line.Terminals.append(t1)

    
 

    network.add_to_graph(transmission_line)
    network.add_to_graph(t1)
    network.add_to_graph(t2)


    #TODO: new_discrete()

    return transmission_line