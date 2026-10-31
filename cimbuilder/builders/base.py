"""Phase 5: ObjectBuilder ABC + builder_base mixin (design: CIMTBL_DESIGN.md §4.1)."""

from abc import ABC

from cimgraph.models import GraphModel
from cimgraph.core import get_system_mva_base
from cimtables import graph_write, impedance
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
        # Resolved once here, same as self.cim above - never re-read inside a
        # leaf add_<part> method (PROFILE_RESOLUTION.md's rule). None if
        # CIMG_SYSTEM_MVA_BASE is unset; only equipment with no self-contained
        # rating pair (ACLineSegment) needs this at all.
        self.system_mva = get_system_mva_base()

    def create(self, *, mRID: str = None, name: str = None, identifier: str = None) -> object:
        """A new, NOT-yet-graph-added instance of cim_class_name (call
        `.add()` once it's built, or let `add_connectivity`/etc. do it).
        Keyed on mRID (so a later rename of `name` - plain, optional data -
        never changes its UUID): mRID if given, else identifier seeded the
        same way, else a random UUID - mirrors cimtables.binder._new_object's
        order (MRID_MIGRATION.md).
        * mRID: plain string, used verbatim as the object's identity key.
        * name: plain string, set on the object as-is (no identity role).
        * identifier: plain string seed for a deterministic UUID (used only
          when mRID is not given); ignored if mRID is given.

        Returns the new, unadded object."""
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

        * row: an already-validated `<Class>Row` dataclass instance (not a
          dict or raw CIM object) - bind_row reflects over its fields to
          populate the built object, including unit conversion for any Qty
          fields and FK resolution for any mRID-reference fields.

        Returns the object already added to the graph (bind_row's own
        contract, matching bind_row's direct callers) - unlike the direct
        create()/add_<part>()/add() API, do not call .add() again on the
        result. No `obj` is passed in: bind_row builds it itself (mRID,
        else identifier, else a random UUID) since a row is keyed by mRID,
        not name - create() is the name-seeded path for the direct API,
        not what from_table wants (MRID_MIGRATION.md)."""
        return bind_row(self.network, row, container=self.container)

    def add(self, obj: object) -> object:
        """Adds `obj` (a live CIM object, already built via `create()` and
        any `add_<part>()` calls) to the graph and indexes it by mRID.
        Returns `obj` unchanged, so this can be chained at the end of a
        builder call sequence."""
        graph_write.add_to_graph(self.network, obj)
        return obj
