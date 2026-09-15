"""Phase 3: set_attr / link / add_to_graph / resolve (design: CIMTBL_DESIGN.md §12.3).

The graph-write core: the only place that actually mutates a live cimgraph
object or writes it into a GraphModel. Everything else (the binder, later
phases' synthesis code) calls through here rather than touching `setattr`/
`network.add_to_graph` directly, so unit-binding and name-indexing can never
be forgotten at a call site.
"""

import typing

from cimgraph.data_profile.units.units import CIMUnit
from cimgraph.models import GraphModel

from cimbuilder.core.name_index import NameIndex
from cimbuilder.core.units import Qty


def _cim_unit_type(obj: object, attr: str) -> type[CIMUnit] | None:
    """The CIMUnit subclass (Voltage, ActivePower, ...) a quantity attr's
    `float | <CIMUnitType>` union carries, or None if the attr isn't
    quantity-typed. Resolved off obj's own class, not `network.cim` - it's
    exactly the module type(obj) was defined in, and set_attr (§12.3) takes
    no network param."""
    hints = typing.get_type_hints(type(obj))
    union_args = typing.get_args(hints.get(attr))
    for arg in union_args:
        if isinstance(arg, type) and issubclass(arg, CIMUnit):
            return arg
    return None


def set_attr(obj: object, attr: str, value: object) -> None:
    """Set a plain scalar or Qty onto a live cim-graph object's attribute."""
    if value is None:
        setattr(obj, attr, None)
        return

    if isinstance(value, Qty):
        cim_unit_type = _cim_unit_type(obj, attr)
        if cim_unit_type is None:
            raise ValueError(
                f"{type(obj).__name__}.{attr} is not a CIMUnit-typed attribute, "
                f"but got a Qty ({value!r})"
            )
        if value.unit:
            setattr(obj, attr, cim_unit_type(value.value, value.unit))
        else:
            setattr(obj, attr, cim_unit_type(value.value))
        return

    setattr(obj, attr, value)


def link(obj: object, assoc: str, target: object) -> None:
    """Set an association attribute to a resolved target object."""
    setattr(obj, assoc, target)


def add_to_graph(network: GraphModel, obj: object) -> None:
    """The single call site (§12.3): add obj to the live graph and its
    NameIndex together, so the two can never drift out of sync."""
    network.add_to_graph(obj)
    network.name_index.add(obj)


def resolve(network: GraphModel, cim_cls: type, name: str) -> object | None:
    """O(1) name -> object lookup. Never raises; None means not found -
    callers decide whether that's an auto-vivify or an error."""
    return network.name_index.get(cim_cls, name)
