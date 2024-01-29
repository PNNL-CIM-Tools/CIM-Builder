from __future__ import annotations
import uuid
import logging

from cimgraph import GraphModel
from cimgraph.databases import ConnectionInterface
from cimgraph.models.graph_model import new_mrid #TODO: replace with utils
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import

_log = logging.getLogger(__name__)


def new_mrid():
    mRID = str(uuid.uuid4())
    return mRID

def terminal_to_node(network:GraphModel, terminal:cim.Terminal, node:str|cim.ConnectivityNode):
    if node.__class__ == str:
        for node_obj in network.graph[cim.ConnectivityNode].values():
            if node_obj.name == node or node_obj.aliasName == node:
                terminal.ConnectivityNode = node_obj
                node_obj.Terminals.append(terminal)
    else:
        terminal.ConnectivityNode = node
        node.Terminals.append(terminal)