from __future__ import annotations
import logging

from cimgraph import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typing import
import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_switch_area(network:GraphModel, feeder_area:cim.FeederArea) -> object:

    area = cim.SwitchArea()
    area.uuid()
    
    network.add_to_graph(meas)

    return area