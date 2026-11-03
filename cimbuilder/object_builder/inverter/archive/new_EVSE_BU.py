from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel
from cimgraph.databases import get_cim_profile
from cimgraph.models.graph_model import new_mrid #TODO: replace with utils
import uuid
import cimgraph.data_profile.cim18gad as cim #TODO: cleaner typying import

from cimbuilder.utils.utils import terminal_to_node

_log = logging.getLogger(__name__)

def new_EVSE_BU(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node:str|cim.ConnectivityNode, kWhrated:float,  chargingMode: str = None) -> None:
    
    # current assumption: same power charging everytime, and we can charge upto rated energy
    cim_profile, cim_module = get_cim_profile()
    cim:cim = cim_module
    
    #EVSE_BU = cim.BatteryUnit(name = name, mRID = new_mrid())
    EVSE_BU = cim.BatteryUnit(name = name, mRID = str(uuid.uuid4()))


    t1 = cim.Terminal(name=f"{name}_t1")
    t1.ConductingEquipment = EVSE_BU
    terminal_to_node(network, t1, node)

    EVSE_BU.EquipmentContainer = container
    EVSE_BU.batteryState = chargingMode
    EVSE_BU.ratedE = kWhrated
    EVSE_BU.Terminals.append(t1)
    

     
    EVSE_BU.Terminals.append(t1)

    network.add_to_graph(EVSE_BU)
    network.add_to_graph(t1)


    #TODO: new_discrete()

    return EVSE_BU