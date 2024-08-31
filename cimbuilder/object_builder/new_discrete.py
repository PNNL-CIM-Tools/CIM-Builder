import logging

from cimgraph import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_discrete(network:GraphModel, equipment:cim.Equipment, terminal:cim.ACDCTerminal,
                  phase:cim.PhaseCode, measurementType:str) -> cim.Discrete:
    
    terminal = equipment.Terminals[0]
    # Create a new discrete for each terminal
    name = f'{equipment.__class__.__name__}_{equipment.name}_{measurementType}'
    name += f'_{terminal.sequenceNumber}_phase_{phase.value}'
    meas = cim.Discrete()
    meas.uuid(name = name)
    meas.Terminal = terminal
    meas.PowerSystemResource = equipment
    meas.measurementType = measurementType
    meas.phases = phase
    equipment.Measurements.append(meas)
    terminal.Measurements.append(meas)
    network.add_to_graph(meas)

    return meas