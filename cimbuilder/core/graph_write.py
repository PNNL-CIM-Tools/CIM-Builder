"""Phase 3/5: set_attr / set_assc / add_to_graph / resolve
(design: CIMTBL_DESIGN.md §12.3, cimbuilder/development/GRAPH_WRITE_CONTRACT.md).

The graph-write core: the only place that actually mutates a live cimgraph
object or writes it into a GraphModel. Everything else (the binder, the
connectivity backend, builder add_<part> methods) calls through here rather
than touching `setattr`/`network.add_to_graph` directly, so unit-binding,
profile-part checking, reverse-association writes, and name-indexing can
never be forgotten at a call site.

set_attr/set_assc's `part` argument is a reference profile-part module (e.g.
cimgraph.data_profile.cim18gmdm.connectivity) checked purely by name against
type(obj).__name__ - never by isinstance/inheritance. `obj` need not (and
usually won't) be an instance of any class in `part`; `part` is a shape
reference, not `obj`'s actual runtime profile. See GRAPH_WRITE_CONTRACT.md §2
for why this is the right decoupling. Passing the merged `network.cim` module
itself as `part` is a documented no-op check (every field passes, since a
merged profile has no restricted attribute set) - the right choice at a call
site with no genuine part-scoped reference available yet (Phase 3/4 code).
"""

import dataclasses
import typing
from types import ModuleType

from cimgraph.data_profile.units.units import CIMUnit
from cimgraph.models import GraphModel

from cimbuilder.core.name_index import NameIndex
from cimbuilder.core.units import Qty


def _cim_unit_type(obj: object, attr: str) -> type[CIMUnit] | None:
    """The CIMUnit subclass (Voltage, ActivePower, ...) a quantity attr's
    `float | <CIMUnitType>` union carries, or None if the attr isn't
    quantity-typed. Resolved off obj's own class, not `network.cim` - it's
    exactly the module type(obj) was defined in, and set_attr takes no
    network param."""
    hints = typing.get_type_hints(type(obj))
    union_args = typing.get_args(hints.get(attr))
    for arg in union_args:
        if isinstance(arg, type) and issubclass(arg, CIMUnit):
            return arg
    return None


def _part_field(part: ModuleType, obj: object, attr: str) -> dataclasses.Field:
    """The dataclasses.Field for `attr` on part's class of the same name as
    type(obj) - the one runtime check standing in for Pylance's static
    narrowing (GRAPH_WRITE_CONTRACT.md §2). Raises ValueError, naming the
    part module and class, if `attr` isn't a real field there at all."""
    cls_name = type(obj).__name__
    part_cls = getattr(part, cls_name, None)
    if part_cls is None:
        raise ValueError(
            f"{part.__name__} has no class named {cls_name!r} "
            f"(wrong reference part module for this object's type)"
        )
    try:
        return part_cls.__dataclass_fields__[attr]
    except KeyError:
        raise ValueError(
            f"{attr!r} is not a field of {part.__name__}.{cls_name} - "
            f"wrong profile part for this attribute"
        ) from None


def set_attr(obj: object, part: ModuleType, attr: str, value: object) -> None:
    """Set a plain scalar or Qty onto a live cim-graph object's attribute.

    Raises ValueError if `attr` is not a real field of part's same-named
    class, or if it IS a field but an association (has metadata['inverse'])
    - use set_assc for that."""
    field = _part_field(part, obj, attr)
    if field.metadata.get('inverse') is not None:
        raise ValueError(
            f"{attr!r} is an association on {part.__name__}.{type(obj).__name__} "
            f"(inverse={field.metadata['inverse']!r}) - use set_assc, not set_attr"
        )

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


def _set_side(obj: object, attr: str, field: dataclasses.Field, target: object) -> None:
    """One side of an association write - list-append (dedup by identity,
    matching cimgraph's own create_edge) or singular overwrite, per field.type."""
    if 'list' in field.type:
        obj_list = getattr(obj, attr)
        if not any(x is target for x in obj_list):
            obj_list.append(target)
    else:
        setattr(obj, attr, target)


def set_assc(obj: object, part: ModuleType, assc: str, target: object) -> None:
    """Set obj.<assc> = target AND write the reverse side onto target,
    resolved from part's field metadata['inverse'] - the one call site for
    establishing any association, so the graph is never one-sided.

    Raises ValueError if `assc` is not a real field of part's same-named
    class, or if it IS a field but a plain scalar (metadata['inverse'] is
    None) - use set_attr for that."""
    field = _part_field(part, obj, assc)
    inverse = field.metadata.get('inverse')
    if inverse is None:
        raise ValueError(
            f"{assc!r} is a plain attribute on {part.__name__}.{type(obj).__name__} "
            f"(not an association) - use set_attr, not set_assc"
        )

    reverse_cls_name, reverse_attr = inverse.split('.')
    reverse_field = getattr(part, reverse_cls_name).__dataclass_fields__[reverse_attr]

    _set_side(obj, assc, field, target)
    if target is not None:
        _set_side(target, reverse_attr, reverse_field, obj)


def add_to_graph(network: GraphModel, obj: object) -> None:
    """The single call site (§12.3): add obj to the live graph and its
    NameIndex together, so the two can never drift out of sync."""
    network.add_to_graph(obj)
    network.name_index.add(obj)


def resolve(network: GraphModel, cim_cls: type, name: str) -> object | None:
    """O(1) name -> object lookup. Never raises; None means not found -
    callers decide whether that's an auto-vivify or an error."""
    return network.name_index.get(cim_cls, name)


def resolve_any_subclass(network: GraphModel, base_cls: type, name: str) -> object | None:
    """Like resolve(), but for an FK slot typed as an abstract base (e.g.
    EquipmentContainer) whose NameIndex entries are keyed by the concrete
    subclass actually built (Feeder, Substation, ...) - NameIndex.add binds
    under type(obj), never a supertype. Checks every concrete subclass bound
    so far; never raises."""
    for bound_cls, by_name in network.name_index.by_class.items():
        if issubclass(bound_cls, base_cls) and name in by_name:
            return by_name[name]
    return None
