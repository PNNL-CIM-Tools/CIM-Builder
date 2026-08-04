from __future__ import annotations
from cimgraph.models import GraphModel
from cimgraph.databases import get_cim_profile
import cimgraph.data_profile.cimhub_2023 as cim 

import logging
_log = logging.getLogger(__name__)

def new_base_voltage(network:GraphModel, base_voltage:int|float, name:str = None) -> cim.BaseVoltage:
    """
    Create a new BaseVoltage object in the network graph.

    Parameters
    ----------
    network : GraphModel
        The network graph model.
    base_voltage : int|float
        The nominal voltage of the base voltage.
    name : str, optional
        The name of the base voltage object. If not provided, a default name will be generated.

    Returns
    -------
    cim.BaseVoltage
        The created BaseVoltage object.
    """
    cim_profile, cim_module = get_cim_profile()
    cim:cim = cim_module

    # Check if a BaseVoltage with the same nominal voltage already exists
    if cim.BaseVoltage in network.graph:
        network.get_all_attributes(cim.BaseVoltage)
        for bv in network.graph[cim.BaseVoltage].values():
            if bv.nominalVoltage == base_voltage or bv.nominalVoltage == base_voltage*1000:
                _log.info(f'BaseVoltage with nominal voltage {base_voltage} already exists.')
                return bv

    # Create a new BaseVoltage object
    if name is None:
        name = f'BaseV_{base_voltage}'
    
    base_voltage_obj = cim.BaseVoltage(name=name, nominalVoltage=base_voltage)
    network.add_to_graph(base_voltage_obj)

    return base_voltage_obj


def get_base_voltage(network:GraphModel, base_voltage:int|cim.BaseVoltage) -> cim.BaseVoltage:
    cim_profile, cim_module = get_cim_profile()
    cim:cim = cim_module

    if base_voltage.__class__ == float or base_voltage.__class__ == int:
        # If numeric value given, search graph for a matching BaseVoltage object
        found = False
        if cim.BaseVoltage in network.graph:
            network.get_all_attributes(cim.BaseVoltage)
            for bv in network.graph[cim.BaseVoltage].values(): 
                if bv.nominalVoltage == base_voltage or bv.nominalVoltage == base_voltage*1000 :
                    found = True
                    base_voltage_obj = bv
        if not found: # If not found, create a new BaseVoltage object
            _log.info(f'Could not find a BaseVoltage with nominalVoltage {base_voltage}. Creating new object')
            base_voltage_obj = cim.BaseVoltage(name = f'BaseV_{base_voltage}', nominalVoltage = base_voltage)
            network.add_to_graph(base_voltage_obj)
    else:
        base_voltage_obj = base_voltage

    return base_voltage_obj