"""Phase 5: ObjectBuilder ABC + builder_base mixin (design: CIMTBL_DESIGN.md §4.1)."""

from abc import ABC

from cimgraph.models import GraphModel

from cimbuilder.core import graph_write
from cimbuilder.core.binder import bind_row


class ObjectBuilder(ABC):
    """One CIM class, built one profile-part at a time (§4.1). Stateless
    except for the object under construction. Reads network.cim; never
    re-derives the profile."""

    cim_class_name: str  # set by subclass, e.g. 'EnergyConsumer'

    def __init__(self, network: GraphModel, container: object = None):
        self.network = network
        self.container = container
        self.cim = network.cim

    def create(self, *, name: str) -> object:
        cim_cls = getattr(self.network.cim, self.cim_class_name)
        return cim_cls(name=name)

    def from_table(self, row: object) -> object:
        """DSL/bulk entry point (§4.2): bind a validated <Class>Row onto a
        freshly create()'d object via the generic, reflective bind_row
        (core/binder.py) - no per-class field dispatch to maintain. Every
        class gets this for free; a subclass only needs cim_class_name.

        Returns the object already added to the graph (bind_row's own
        contract, matching bind_row's direct callers) - unlike the direct
        create()/add_<part>()/add() API, do not call .add() again on the
        result."""
        obj = self.create(name=row.name)
        return bind_row(self.network, row, obj=obj, container=self.container)

    def add(self, obj: object) -> object:
        graph_write.add_to_graph(self.network, obj)
        return obj
