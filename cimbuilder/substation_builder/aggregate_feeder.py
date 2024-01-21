from __future__ import annotations
import logging

from cimgraph.models import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

import cimbuilder.object_builder as builder
import cimbuilder.utils as utils

_log = logging.getLogger(__name__)


def new_aggregate_feeder(network:GraphModel, feeder_name:str, breaker_name:str, substation:cim.Substation, 
                         node:cim.ConnectivityNode|str, base_voltage:cim.BaseVoltage|float,
                         total_load_mw:float, total_load_mvar:float, total_pv_mw:float) -> None:
    
    # get base voltage
    found == False
    if base_voltage.__class__ == float or base_voltage.__class__ == int:
        # If numeric value given, search graph for a matching BaseVoltage object
        for bv in network.graph[cim.BaseVoltage].values(): 
            if bv.nominalVoltage == base_voltage or bv.nominalVoltage == base_voltage*1000 :
                found = True
                base_voltage_obj = bv
        if not found: # If not found, create a new BaseVoltage object
            _log.warning(f'Could not find a BaseVoltage with nominalVoltage {base_voltage}. Creating new object')
            base_voltage_obj = cim.BaseVoltage(name = f'BaseV_{base_voltage}', mRID = utils.new_mrid(), nominalVoltage = base_voltage)

    
    # create feeder container
    feeder_mrid = utils.new_mrid()
    feeder = cim.Feeder(mRID = feeder_mrid, name=feeder_name)
    feeder.NormalEnergizingSubstation = substation
    network.add_to_graph(feeder)

    # create aggregate Node
    feeder_node = cim.ConnectivityNode(name='name', mRID=utils.new_mrid())
    feeder_node.ConnectivityNodeContainer = feeder
    network.add_to_graph(feeder_node)

    # create breaker
    breaker = builder.new_two_terminal_object(network, container=substation, class_type=cim.Breaker, 
                                              name=breaker_name, node1 = node, node2 = feeder_node)
    breaker.AdditionalEquipmentContainer = feeder
    breaker.BaseVoltage = base_voltage_obj

    # create energy consumer
    load = builder.new_one_terminal_object(network, container=feeder, class_type=cim.EnergyConsumer,
                                           name=f'{feeder_name}_aggr_load', node=feeder_node)                          
    load.p = total_load_mw*1000000
    load.q = total_load_mvar*1000000
    load.BaseVoltage = base_voltage_obj

    # create PV objects
    inverter = builder.new_one_terminal_object(network, container=feeder, class_type=cim.EnergyConsumer,
                                               name=f'{feeder_name}_aggr_pv', node = feeder_node)
    inverter.p = total_pv_mw*1000000
    inverter.BaseVoltage = base_voltage_obj
    pv_unit = cim.PhotovoltaicUnit(name=f'{feeder_name}_aggr_pv', mRID = utils.new_mrid())
    pv_unit.minP = 0.0
    pv_unit.maxP = inverter.p
    pv_unit.PowerElectronicsConnection = inverter
    inverter.PowerElectronicsUnit.append(pv_unit)
    network.add_to_graph(pv_unit)




