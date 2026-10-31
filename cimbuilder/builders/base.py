"""Phase 5: ObjectBuilder ABC + builder_base mixin (design: CIMTBL_DESIGN.md §4.1)."""

from abc import ABC

from cimgraph.models import GraphModel

from cimtables import graph_write
from cimtables.binder import bind_row


class ObjectBuilder(ABC):
    """One CIM class, built one profile-part at a time (§4.1). Stateless
    except for the object under construction. Reads network.cim; never
    re-derives the profile."""

    cim_class_name: str  # set by subclass, e.g. 'EnergyConsumer'

    def __init__(self, network: GraphModel, container: object = None):
        self.network = network
        self.container = container
        self.cim = network.cim

    def create(self, *, mRID: str = None, name: str = None, identifier: str = None) -> object:
        """A new instance of cim_class_name, keyed on mRID (so a later rename
        of `name` - plain, optional data - never changes its UUID): mRID if
        given, else identifier seeded the same way, else a random UUID -
        mirrors cimtables.binder._new_object's order (MRID_MIGRATION.md).
        `name` is set after, independent of which key was used."""
        cim_cls = getattr(self.network.cim, self.cim_class_name)
        if mRID is not None:
            obj = cim_cls(mRID=mRID)
        else:
            obj = cim_cls()
            if identifier is not None:
                obj.uuid(mRID=identifier)
        if name is not None:
            obj.name = name
        return obj

    def from_table(self, row: object) -> object:
        """DSL/bulk entry point (§4.2): bind a validated <Class>Row onto a
        freshly create()'d object via the generic, reflective bind_row (the
        cimtables package - split out of this repo, see
        development/CIMTBL_DESIGN.md §8.1) - no per-class field dispatch to
        maintain. Every class gets this for free; a subclass only needs
        cim_class_name.

        Returns the object already added to the graph (bind_row's own
        contract, matching bind_row's direct callers) - unlike the direct
        create()/add_<part>()/add() API, do not call .add() again on the
        result. No `obj` is passed in: bind_row builds it itself (mRID,
        else identifier, else a random UUID) since a row is keyed by mRID,
        not name - create() is the name-seeded path for the direct API,
        not what from_table wants (MRID_MIGRATION.md)."""
        return bind_row(self.network, row, container=self.container)

    def add(self, obj: object) -> object:
        graph_write.add_to_graph(self.network, obj)
        return obj
