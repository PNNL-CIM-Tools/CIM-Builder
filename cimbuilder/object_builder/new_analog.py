from __future__ import annotations
import importlib
import logging

from cimgraph import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_analog(network:GraphModel, equipment:cim.Equipment, terminal:cim.Terminal,
               phase:cim.PhaseCode, measurementType:str, mRID: str = None, name:str = None,
               check_duplicate = True) -> object:
    cim = network.connection.cim
    meas_exists = False
    if measurementType == 'PNV' and not isinstance(equipment, 
                                                   (cim.EnergyConsumer, cim.PowerElectronicsConnection, 
                                                    cim.LinearShuntCompensator)):
        for far_terminal in terminal.ConnectivityNode.Terminals:
            for far_meas in far_terminal.Measurements:
                if far_meas.measurementType == 'PNV':
                    meas_exists = True
                    break
            if meas_exists:
                break
    elif check_duplicate:
        for meas in equipment.Measurements:
            if (
                terminal.identifier == meas.Terminal.identifier and
                phase == meas.phases and
                measurementType == meas.measurementType
            ):
                meas_exists = True
                break
    meas = None
    if not meas_exists:
        # Create a new analog for specified terminal
        meas = cim.Analog()
        seed = f'{equipment.__class__.__name__}_{equipment.name}_{measurementType}'
        if measurementType != 'SoC':
            seed += f'_{terminal.sequenceNumber}_{phase.value}'
        if name is not None:
            meas.uuid(name = seed + name)
            meas.name = name
        else:
            meas.uuid(name = seed)
        meas.Terminal = terminal
        meas.PowerSystemResource = equipment
        meas.measurementType = measurementType
        meas.phases = phase
        equipment.Measurements.append(meas)
        terminal.Measurements.append(meas)
        network.add_to_graph(meas)
        # _log.warning(meas.name)
    return meas

def create_all_analog(network:GraphModel, equipment:object, measurementType:str) -> object:
    counter = 1
    meas_list = []
    for terminal in equipment.Terminals:
        # Create a new analog for each terminal
        meas = cim.Analog(mRID = utils.new_mrid())
        meas.name = f'{equipment.__class__.__name__}_{equipment.name}_{measurementType}_{counter}'
        meas.Terminal = terminal
        meas.PowerSystemResource = equipment
        meas.measurementType = measurementType
        equipment.Measurements.append(meas)
        terminal.Measurements.append(meas)
        network.add_to_graph(meas)
        counter = counter + 1
        meas_list.append(meas)

    return meas