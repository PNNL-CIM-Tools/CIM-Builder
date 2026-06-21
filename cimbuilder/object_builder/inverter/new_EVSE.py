from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel

import cimgraph.data_profile.cim18gad as cim #TODO: cleaner typying import
from cimgraph.models.graph_model import new_mrid #TODO: replace with utils
import uuid

from cimbuilder.utils.utils import terminal_to_node

_log = logging.getLogger(__name__)

def new_EVSE(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node:str|cim.ConnectivityNode, chargingMode: str = None) -> None:
    
    # current assumption: same power charging everytime, and we can charge upto rated energy
    cim = network.cim

    
    EVSE = cim.evse(name = name, mRID = str(uuid.uuid4()))

    t1 = cim.Terminal()
    t1.uuid(name=f"{name}_t1")
    t1.sequenceNumber=1
    t1.ConductingEquipment = EVSE
    terminal_to_node(network, t1, node)

    EVSE.EquipmentContainer = container
    
    EVSE.chargingModeType = chargingMode  
    

     
    EVSE.Terminals.append(t1)

    network.add_to_graph(EVSE)
    network.add_to_graph(t1)


    #TODO: new_discrete()

    return EVSE