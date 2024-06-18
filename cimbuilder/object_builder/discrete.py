from __future__ import annotations
import importlib
import logging

from cimgraph import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_discrete(network:GraphModel, equipment:object, measurementType:str) -> object:
    cim = utils.get_cim_profile(network.connection)  # Import CIM profile
    
    terminal = equipment.Terminals[0]
    # Create a new discrete for each terminal
    sequence = terminal.sequenceNumber
    name = f'{equipment.__class__.__name__}_{equipment.name}_t{sequence}_{measurementType}'
    meas = cim.Discrete(mRID = utils.new_mrid(class_type=cim.Discrete, name=name))
    meas.name = name
    meas.PowerSystemResource = equipment
    meas.Location = equipment.Location
    meas.measurementType = measurementType
    equipment.Measurements.append(meas)
    terminal.Measurements.append(meas)
    network.add_to_graph(meas)

    return meas

def create_all_discrete(network:GraphModel, equipment:object, measurementType:str) -> object:
    counter = 1
    meas_list = []
    cim = utils.get_cim_profile(network.connection)  # Import CIM profile

    for terminal in equipment.Terminals:
        # Create a new analog for each terminal
        sequence = terminal.sequenceNumber
        name = f'{equipment.__class__.__name__}_{equipment.name}_t{sequence}_{measurementType}'
        meas = cim.Discrete(mRID = utils.new_mrid(class_type=cim.Discrete, name=name))
        meas.name = name
        meas.Terminal = terminal
        meas.PowerSystemResource = equipment
        meas.Location = equipment.Location
        meas.measurementType = measurementType
        equipment.Measurements.append(meas)
        terminal.Measurements.append(meas)
        network.add_to_graph(meas)
        counter = counter + 1
        meas_list.append(meas)

    return meas