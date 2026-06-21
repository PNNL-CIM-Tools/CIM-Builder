from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel

from cimgraph.models.graph_model import new_mrid #TODO: replace with utils
import uuid
import cimgraph.data_profile.cim18gad as cim #TODO: cleaner typying import

from cimbuilder.utils.utils import terminal_to_node

_log = logging.getLogger(__name__)

def new_EVSE_PEC(network:GraphModel, container:cim.EquipmentContainer, name:str, 
                node:str|cim.ConnectivityNode, kW:float) -> None:
    
    # current assumption: same power charging everytime, and we can charge upto rated energy
    cim = network.cim

    
    EVSE_PEC = cim.PowerElectronicsConnection(name = name, mRID = new_mrid())
    EVSE_PEC = cim.PowerElectronicsConnection(name = name, mRID = str(uuid.uuid4()))

    t1 = cim.Terminal(name=f"{name}_t1")
    t1.ConductingEquipment = EVSE_PEC
    terminal_to_node(network, t1, node)

    EVSE_PEC.EquipmentContainer = container
    EVSE_PEC.p = kW
    EVSE_PEC.q = 0
    EVSE_PEC.Terminals.append(t1)
    

    network.add_to_graph(EVSE_PEC)
    network.add_to_graph(t1)


    #TODO: new_discrete()

    return EVSE_PEC