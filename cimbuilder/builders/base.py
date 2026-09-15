"""Phase 5: ObjectBuilder ABC + builder_base mixin (design: CIMTBL_DESIGN.md §4.1)."""

from abc import ABC, abstractmethod

from cimgraph.models import GraphModel

from cimbuilder.core import graph_write


class ObjectBuilder(ABC):
    """One CIM class, built one profile-part at a time (§4.1). Stateless
    except for the object under construction. Reads network.cim; never
    re-derives the profile."""

    cim_class_name: str  # set by subclass, e.g. 'EnergyConsumer'

    def __init__(self, network: GraphModel, container: object = None):
        self.network = network
        self.container = container

    def create(self, *, name: str) -> object:
        cim_cls = getattr(self.network.cim, self.cim_class_name)
        return cim_cls(name=name)

    @abstractmethod
    def from_table(self, row: object) -> object:
        """DSL/bulk entry point (§4.2): unpack a validated <Class>Row into
        this builder's create()/add_*() calls, returning the built object."""

    def add(self, obj: object) -> object:
        graph_write.add_to_graph(self.network, obj)
        return obj
