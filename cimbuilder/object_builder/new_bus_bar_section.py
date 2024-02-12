from __future__ import annotations
import importlib
import logging

from cimgraph import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_bus_bar_section(network:GraphModel, node:cim.ConnectivityNode) -> cim.BusbarSection:
    busbar = cim.BusbarSection(mRID=utils.new_mrid())
    busbar.name = node.name
    busbar.EquipmentContainer = node.ConnectivityNodeContainer
    
    terminal = cim.Terminal(mRID = utils.new_mrid())
    terminal.name = node.name + '.1'
    terminal.ConnectivityNode = node
    terminal.ConductingEquipment = busbar
    terminal.sequenceNumber = 1

    network.add_to_graph(busbar)
    network.add_to_graph(terminal)
    
    return busbar