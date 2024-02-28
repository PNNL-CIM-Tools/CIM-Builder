from __future__ import annotations
import importlib
import logging

from cimgraph import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_discrete(network:GraphModel, equipment:object, measurementType:str) -> object:
    
    terminal = equipment.Terminals[0]
    # Create a new discrete for each terminal
    meas = cim.Discrete( mRID = utils.new_mrid())
    meas.name = f'{equipment.__class__.__name__}_{equipment.name}_{measurementType}'
    meas.Terminal = terminal
    meas.PowerSystemResource = equipment
    meas.Location = equipment.Location
    meas.measurementType = measurementType
    equipment.Measurements.append(meas)
    terminal.Measurements.append(meas)
    network.add_to_graph(meas)

    return meas