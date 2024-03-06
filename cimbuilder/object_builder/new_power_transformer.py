import logging
import json

from cimgraph import GraphModel
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typing import

import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

def new_power_transformer(network:GraphModel, container:cim.EquipmentContainer, name:str,
                node1:str|cim.ConnectivityNode, node2:str|cim.ConnectivityNode,
                catalog_file:str = None) -> cim.PowerTransformer:
    
    if catalog_file is not None:
        xfmr = utils.catalog_parser(catalog_file, network)
        # xfmr = cim.PowerTransformer()
        xfmr.name = name
        xfmr.EquipmentContainer = container

        for end in xfmr.PowerTransformerEnd:
            end.PowerTransformer = xfmr
            number = int(end.endNumber)
            terminal = cim.Terminal(name=f"{xfmr.name}_t{number}", mRID = utils.new_mrid(), sequenceNumber=number)
            end.Terminal = terminal
            xfmr.Terminals.append(terminal)
            network.add_to_graph(terminal)

            # TODO: make generalized
            if number == 1:
                utils.terminal_to_node(network, terminal, node1)
            if number == 2:
                utils.terminal_to_node(network, terminal, node2)

    return xfmr