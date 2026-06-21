from __future__ import annotations


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID
from cimgraph.models import GraphModel


jsonld = dict['@id':str(UUID),'@type':str(type)]
Graph = dict[type, dict[UUID, object]]

@dataclass
class ObjectBuilder(ABC):
    network:GraphModel = field(default=None)

    @abstractmethod
    def create(self):
        raise RuntimeError('Must have implemented connect in inherited class')
    
    @abstractmethod
    def add_connectivity(self):
        raise RuntimeError('Must have implemented connect in inherited class')
    
    @abstractmethod
    def add_electrical(self):
        raise RuntimeError('Must have implemented connect in inherited class')
    
    @abstractmethod
    def add_dynamics(self):
        raise RuntimeError('Must have implemented connect in inherited class')
    
    @abstractmethod
    def add_short_circuit(self):
        raise RuntimeError('Must have implemented connect in inherited class')
    
    @abstractmethod
    def from_catalog(self):
        raise RuntimeError('Must have implemented connect in inherited class')