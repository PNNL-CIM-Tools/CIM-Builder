from __future__ import annotations

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import get_cim_profile
import cimgraph.data_profile.cimhub_2023 as cim  

import logging
_log = logging.getLogger(__name__)

def get_source_bus(feeder_network: GraphModel, feeder: cim.Feeder,) -> cim.ConnectivityNode:
    
    cim_profile, cim_module = get_cim_profile()
    cim: cim = cim_module
    sourcebus = None
    if not sourcebus:
        found = False
        feeder_network.get_all_edges(cim.EnergySource)
        feeder_network.get_all_edges(cim.Terminal)
        feeder_network.get_all_edges(cim.ConnectivityNode)
        # Check if the feeder network has a source bus
        if feeder.NormalHeadTerminal is not None:
            sourcebus = feeder.NormalHeadTerminal.ConnectivityNode
            found = True
        
        else:
            # Search for a source bus in the feeder network
            for source in feeder_network.graph.get(cim.EnergySource,{}).values():
                if source.Terminals[0].ConnectivityNode.name == 'sourcebus':
                    sourcebus = source.Terminals[0].ConnectivityNode
                    found = True
        if not found:
            _log.error(f'Could not find sourcebus for {feeder.name}')
    
    return sourcebus