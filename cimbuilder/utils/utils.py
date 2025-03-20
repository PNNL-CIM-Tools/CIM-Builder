from __future__ import annotations
from random import Random
from uuid import UUID, uuid4
import logging
import importlib
import json

from cimgraph import GraphModel
from cimgraph.databases import ConnectionInterface
from cimgraph.models.graph_model import new_mrid #TODO: replace with utils
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import


_log = logging.getLogger(__name__)

def get_cim_profile(connection:ConnectionInterface) -> type:
    cim_profile = connection.connection_params.cim_profile
    cim = importlib.import_module(f'cimgraph.data_profile.{cim_profile}')
    return cim

def new_mrid(class_type:type = cim.IdentifiedObject, name:str = None) -> str:
    if name:
        seedStr = f"{class_type.__name__}:{name}"
        randomGenerator = Random(seedStr)
        mRID = str(UUID(int=randomGenerator.getrandbits(128), version=4))
    else:
        mRID = str(uuid4())
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

def get_base_voltage(network:GraphModel, base_voltage:int|cim.BaseVoltage) -> cim.BaseVoltage:
    cim = get_cim_profile(network.connection) # Import CIM profile

    if base_voltage.__class__ == float or base_voltage.__class__ == int:
        # If numeric value given, search graph for a matching BaseVoltage object
        found = False
        if cim.BaseVoltage in network.graph:
            network.get_all_attributes(cim.BaseVoltage)
            for bv in network.graph[cim.BaseVoltage].values(): 
                if bv.nominalVoltage == base_voltage or bv.nominalVoltage == base_voltage*1000 :
                    found = True
                    base_voltage_obj = bv
        if not found: # If not found, create a new BaseVoltage object
            _log.info(f'Could not find a BaseVoltage with nominalVoltage {base_voltage}. Creating new object')
            base_voltage_obj = cim.BaseVoltage(name = f'BaseV_{base_voltage}', mRID = new_mrid(), nominalVoltage = base_voltage)
            network.add_to_graph(base_voltage_obj)
    else:
        base_voltage_obj = base_voltage

    return base_voltage_obj


def catalog_parser(catalog_file, network):
    file = open(catalog_file)
    catalog = json.load(file)
    data = catalog['catalog']
    cim = get_cim_profile(network.connection) # Import CIM profile
    obj = item_parser(data, network, cim)
    file.close()
    return obj

def item_parser(data, network, cim):
    class_type = edge_class = eval(f'cim.{data["@type"]}')
    obj = class_type()
    setattr(obj, 'mRID', new_mrid())
    network.add_to_graph(obj)

    for attribute in data:
        if type(data[attribute]) == str:
            if attribute in class_type.__dataclass_fields__:
                setattr(obj, attribute, data[attribute])
            # else:
            #     _log.warning(f'Attribute {attribute} not found')
        elif type(data[attribute]) == list:
            if attribute in class_type.__dataclass_fields__:
                values = getattr(obj, attribute)
                for item in data[attribute]:
                    value = item_parser(item, network, cim)
                    values.append(value)
                setattr(obj, attribute, values)
    return obj