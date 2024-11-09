from __future__ import annotations
import logging

from cimgraph.models import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

import cimbuilder.object_builder as builder
import cimbuilder.utils as utils

_log = logging.getLogger(__name__)


def new_aggregate_feeder(network:GraphModel, feeder_name:str, breaker_name:str, substation:cim.Substation, 
                         node:cim.ConnectivityNode|str, base_voltage:cim.BaseVoltage|float,
                         total_load_kw:float=0, total_load_kvar:float=0, total_btm_pv_kw:float=0, total_ftm_pv_kw:float=0,
                         total_btm_wind_kw:float=0, total_ftm_wind_kw:float=0, distributed = True) -> tuple[cim.Feeder, cim.EnergyConsumer, cim.Breaker]:
    cim = network.connection.cim
    # get base voltage
    if base_voltage.__class__ == float or base_voltage.__class__ == int:
        # If numeric value given, search graph for a matching BaseVoltage object
        found = False
        if cim.BaseVoltage in network.graph:
            for bv in network.graph[cim.BaseVoltage].values(): 
                if bv.nominalVoltage == base_voltage or bv.nominalVoltage == base_voltage*1000 :
                    found = True
                    base_voltage_obj = bv
        if not found: # If not found, create a new BaseVoltage object
            _log.warning(f'Could not find a BaseVoltage with nominalVoltage {base_voltage}. Creating new object')
            base_voltage_obj = cim.BaseVoltage()
            base_voltage_obj.uuid(name = f'BaseV_{base_voltage}')
            base_voltage_obj.nominalVoltage = base_voltage
            network.add_to_graph(base_voltage_obj)
    else:
        base_voltage_obj = base_voltage

    
    # create feeder container
    feeder = cim.Feeder()
    feeder.uuid(name = feeder_name)
    feeder.NormalEnergizingSubstation = substation
    network.add_to_graph(feeder)

    

    # create aggregate Node
    feeder_node = cim.ConnectivityNode()
    feeder_node.uuid(name=f'{feeder_name}_node_1')
    feeder_node.ConnectivityNodeContainer = feeder
    network.add_to_graph(feeder_node)

    # create breaker
    breaker = builder.new_two_terminal_object(network, container=substation, class_type=cim.Breaker, 
                                              name=breaker_name, node1 = node, node2 = feeder_node)
    
    breaker.AdditionalEquipmentContainer = feeder
    breaker.BaseVoltage = base_voltage_obj
    feeder.NormalHeadTerminal = breaker.Terminals[1]

    if distributed:
        feeder_area = cim.FeederArea()
        feeder_area.uuid(name = 'feeder_area_'+ feeder.name)
        feeder_area.Feeder = feeder
        feeder_area.BoundaryTerminals.append(breaker.Terminals[1])

        feeder.FeederArea = feeder_area
        breaker.Terminals[1].BoundedSchedulingArea = feeder_area
        network.add_to_graph(feeder_area)


    builder.new_discrete(network, equipment=breaker, measurementType='Pos', 
                         terminal=breaker.Terminals[1], phase=cim.PhaseCode.ABC)

    meas = builder.new_analog(network, equipment=breaker, measurementType='VA',
                              terminal=breaker.Terminals[1], phase=cim.PhaseCode.ABC,
                              check_duplicate=False)
    meas.name = f'NetLoad(MW)_{feeder_name}'

    meas = builder.new_analog(network, equipment=breaker, measurementType='VA', 
                              terminal=breaker.Terminals[1], phase=cim.PhaseCode.ABC,
                              check_duplicate=False)
    meas.name = f'ExcessGeneration(MW)_{feeder_name}'

    meas = builder.new_analog(network, equipment=breaker, measurementType='VA',
                              terminal=breaker.Terminals[1], phase=cim.PhaseCode.ABC,
                              check_duplicate=False)
    meas.name = f'TotalGeneration(MW)_{feeder_name}'
  

    # create energy consumer
    load = builder.new_one_terminal_object(network, container=feeder, class_type=cim.EnergyConsumer,
                                           name=f'{feeder_name}_aggr_load', node=feeder_node)                          
    load.p = total_load_kw*1000
    load.q = total_load_kvar*1000
    load.BaseVoltage = base_voltage_obj
    if distributed:
            load.SubSchedulingArea = feeder_area
    # feeder.Equipments.append(load)
    # builder.new_analog(network, equipment=load, measurementType='PNV')
    meas = builder.new_analog(network, equipment=load, measurementType='VA', 
                              terminal=load.Terminals[0], phase=cim.PhaseCode.ABC)
    meas.name = f'GrossLoad(MW)_{feeder_name}'

    # create BTM PV objects
    
    btm_inverter = builder.new_one_terminal_object(network, container=feeder, class_type=cim.PowerElectronicsConnection,
                                               name=f'{feeder_name}_aggr_btm_pv', node = feeder_node)
    btm_inverter.p = total_btm_pv_kw*1000 + total_btm_wind_kw*1000
    btm_inverter.q = 0
    btm_inverter.BaseVoltage = base_voltage_obj
    if distributed:
        btm_inverter.SubSchedulingArea = feeder_area
    network.add_to_graph(btm_inverter)
    pv_unit = cim.PhotovoltaicUnit()
    pv_unit.uuid(name=f'{feeder_name}_aggr_btm_pv')
    pv_unit.minP = 0.0
    pv_unit.maxP = total_btm_pv_kw*1000
    pv_unit.PowerElectronicsConnection = btm_inverter
    if distributed:
        pv_unit.SubSchedulingArea = feeder_area
    btm_inverter.PowerElectronicsUnit.append(pv_unit)
    network.add_to_graph(pv_unit)
    
    if total_btm_wind_kw:
        wind_unit = cim.PowerElectronicsWindUnit()
        wind_unit.uuid(name=f'{feeder_name}_aggr_btm_wind')
        wind_unit.minP = 0.0
        wind_unit.maxP = total_btm_wind_kw*1000
        wind_unit.PowerElectronicsConnection = btm_inverter
        if distributed:
            wind_unit.SubSchedulingArea = feeder_area
        btm_inverter.PowerElectronicsUnit.append(wind_unit)
        network.add_to_graph(wind_unit)

    # builder.new_analog(network, equipment=inverter, measurementType='PNV')
    meas = builder.new_analog(network, equipment=btm_inverter, measurementType='VA',
                              terminal=btm_inverter.Terminals[0], phase=cim.PhaseCode.ABC,
                              check_duplicate=False)
    meas.name = f'BTMGeneration(MW)_{feeder_name}'

    # create FTM PV objects
    ftm_inverter = builder.new_one_terminal_object(network, container=feeder, class_type=cim.PowerElectronicsConnection,
                                               name=f'{feeder_name}_aggr_ftm_pv', node = feeder_node)
    ftm_inverter.p = total_ftm_pv_kw*1000 + total_ftm_wind_kw*1000
    ftm_inverter.q = 0
    ftm_inverter.BaseVoltage = base_voltage_obj
    if distributed:
        ftm_inverter.SubSchedulingArea = feeder_area
    pv_unit = cim.PhotovoltaicUnit()
    pv_unit.uuid(name=f'{feeder_name}_aggr_ftm_pv')
    pv_unit.minP = 0.0
    pv_unit.maxP = ftm_inverter.p
    pv_unit.PowerElectronicsConnection = ftm_inverter
    if distributed:
        pv_unit.SubSchedulingArea = feeder_area
    network.add_to_graph(pv_unit)
    ftm_inverter.PowerElectronicsUnit.append(pv_unit)
    if total_ftm_wind_kw:
        wind_unit = cim.PowerElectronicsWindUnit()
        wind_unit.uuid(name=f'{feeder_name}_aggr_ftm_wind')
        wind_unit.minP = 0.0
        wind_unit.maxP = total_ftm_wind_kw*1000
        wind_unit.PowerElectronicsConnection = ftm_inverter
        if distributed:
            wind_unit.SubSchedulingArea = feeder_area
        ftm_inverter.PowerElectronicsUnit.append(wind_unit)
        network.add_to_graph(wind_unit)

    # feeder.Equipments.append(ftm_inverter)
    # builder.new_analog(network, equipment=inverter, measurementType='PNV')
    meas = builder.new_analog(network, equipment=ftm_inverter, measurementType='VA',
                              terminal=ftm_inverter.Terminals[0], phase=cim.PhaseCode.ABC,
                              check_duplicate=False)
    meas.name = f'FTMGeneration(MW)_{feeder_name}'

    


        

    return feeder, load, breaker


