from __future__ import annotations
import json
import logging

from cimgraph.models import GraphModel

_log = logging.getLogger(__name__)


def catalog_parser(catalog_file, network):
    file = open(catalog_file)
    catalog = json.load(file)
    data = catalog['catalog']
    obj = item_parser(data, network, network.cim)
    file.close()
    return obj

def item_parser(data:dict, network: GraphModel, cim):
    class_type = edge_class = eval(f'cim.{data["@type"]}')
    obj = class_type()
    network.add_to_graph(obj)

    for attribute in data:
        if type(data[attribute]) == str:
            if attribute in class_type.__dataclass_fields__:
                setattr(obj, attribute, data[attribute])
            else:
                _log.warning(f'Attribute {attribute} not found')
        elif type(data[attribute]) == list:
            if attribute in class_type.__dataclass_fields__:
                values = getattr(obj, attribute)
                for item in data[attribute]:
                    value = item_parser(item, network, cim)
                    values.append(value)
                setattr(obj, attribute, values)
    return obj


### Goes through json and validates fields are valid