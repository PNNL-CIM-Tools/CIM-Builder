from __future__ import annotations
import importlib
import logging

from cimgraph.models import GraphModel
from cimgraph.databases import ConnectionInterface
import cimgraph.data_profile.ufls as cim #TODO: cleaner typying import

from cimbuilder.utils.utils import terminal_to_node

_log = logging.getLogger(__name__)

def new_under_frequency_protection_function_block(network:GraphModel, ProtectedSwitch:cim.ProtectedSwitch, operateValue:float, 
                    enabled:bool, ProtectionEquipment:cim.ProtectionEquipment) -> cim.UnderFrequencyProtectionFunctionBlock:

    ufls = cim.UnderFrequencyProtectionFunctionBlock()
    ufls.uuid(name = f'ufls_{operateValue}_{ProtectedSwitch.name}')

    ufls.operateValue = operateValue
    ufls.usage = f'ufls_{operateValue}'
    ufls.enabled = enabled
    ufls.ProtectedSwitch = ProtectedSwitch
    ufls.ProtectionEquipment = ProtectionEquipment
 

    network.add_to_graph(ufls)


    #TODO: new_discrete()

    return ufls