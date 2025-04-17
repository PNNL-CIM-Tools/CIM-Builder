from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID
from cimgraph.models import GraphModel, DistributedArea
from cimgraph.data_profile.identity import Identity
from cimgraph.databases import ConnectionInterface
from cimgraph import utils as cim_utils

_log = logging.getLogger(__name__)

jsonld = dict['@id':str(UUID),'@type':str(type)]
Graph = dict[type, dict[UUID, object]]

@dataclass
class SubstationBuilder(ABC):
    connection:ConnectionInterface
    network:GraphModel = field(default=None)

    @abstractmethod
    def new_branch(self):
        raise RuntimeError('Must have implemented connect in inherited class')
    
    @abstractmethod
    def new_feeder(self):
        raise RuntimeError('Must have implemented connect in inherited class')
    
    def upload(self):
        """Upload the network to the database"""
        if not self.network:
            raise RuntimeError('Network is not defined')
        if not self.connection:
            raise RuntimeError('Connection is not defined')
        self.network.upload()

    def write_json_ld(self, filename:str):
        """Write the network to a JSON file"""
        if not self.network:
            raise RuntimeError('Network is not defined')
        cim_utils.write_json_ld(self.network, filename)

    def write_xml(self, filename:str):
        """Write the network to a XML file"""
        if not self.network:
            raise RuntimeError('Network is not defined')
        cim_utils.write_xml(self.network, filename)

    def pprint(self, cim_class: type, show_empty: bool = False,
               json_ld: bool = False, use_names: bool = False) -> None:
        """Pretty print all instances of a CIM class type in the network"""
        if not self.network:
            raise RuntimeError('Network is not defined')
        self.network.pprint(cim_class, show_empty, json_ld, use_names)
    