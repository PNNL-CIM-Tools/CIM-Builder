import logging

from cimgraph import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_discrete(network:GraphModel, equipment:cim.Equipment, terminal:cim.ACDCTerminal,
                  phase:cim.PhaseCode, measurementType:str, mRID: str = None) -> cim.Discrete:
    
    meas_exists = False
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
        terminal = equipment.Terminals[0]
        # Create a new discrete for each terminal
        name = f'{equipment.__class__.__name__}_{equipment.name}_{measurementType}_{terminal.sequenceNumber}_'
        name += f'{phase.value}'
        meas = cim.Discrete()
        meas.uuid(name = name, mRID = mRID)
        meas.Terminal = terminal
        meas.PowerSystemResource = equipment
        meas.measurementType = measurementType
        meas.phases = phase
        equipment.Measurements.append(meas)
        terminal.Measurements.append(meas)
        network.add_to_graph(meas)
    return meas