"""Phase 3/5: reflective column -> attr/assoc/connectivity binder
(design: CIMTBL_DESIGN.md §2.1, §4.2).

bind_row is the one generic entry point from a validated <Class>Row to a live
cim-graph object, for every class in the selected CIM profile - no per-class
from_table/add_<part> dispatch table to maintain. Every row field is
classified purely from the profile (dsl/validate.py), by name, into exactly
one of three buckets:

- a connectivity column (node*/bus*, per connectivity.py's naming rule) ->
  collected and passed to connectivity.add_connectivity in column order
- EquipmentContainer -> resolved via resolve_any_subclass (its range is
  always an abstract base: Feeder, Substation, ... - see dsl/validate.py's
  reference_target_class) and passed to add_connectivity as the container
  override, not set directly
- any other reference slot (FK) -> resolved via resolve() against the
  schema's own range class name and written with set_assc
- everything else -> a plain scalar/Qty, written with set_attr (unchanged
  from Phase 3)

set_attr/set_assc are called with network.cim as `part` throughout - the
documented no-op part-check (graph_write.py's module docstring) appropriate
at a genuinely reflective call site with no class-specific reference module
to check against. See development/PROFILE_RESOLUTION.md.
"""

import dataclasses

from cimgraph.models import GraphModel

from cimbuilder.core import connectivity, graph_write
from cimbuilder.dsl import synthetic, validate

_SKIP_FIELDS = {'name', 'source_file', 'source_line'}
_CONTAINER_FIELD = 'EquipmentContainer'


def bind_row(network: GraphModel, row: object, *, obj: object = None, container: object = None) -> object:
    """Validated <Class>Row -> live cim-graph object, added to network.

    `obj` lets a caller (ObjectBuilder.from_table) supply an already-created
    object instead of this function constructing one with cim_cls(name=...) -
    so a builder's own create() (which may do more than a bare constructor
    call, e.g. UUID seeding) stays the single place an object comes into
    being. `container` is an explicit EquipmentContainer override (a
    builder's self.container); a row's own EquipmentContainer column still
    takes precedence over it, matching add_connectivity's existing fallback
    order."""
    row_cls_name = type(row).__name__
    ref_slots = validate.reference_slots(row_cls_name)

    if obj is None:
        cim_cls_name = row_cls_name.removesuffix('Row')
        obj = getattr(network.cim, cim_cls_name)(name=row.name)

    node_cols: dict[str, str] = {}
    deferred_fks: list[tuple[str, str]] = []

    for f in dataclasses.fields(row):
        if f.name in _SKIP_FIELDS:
            continue
        value = getattr(row, f.name)
        if value is None:
            continue

        if synthetic.is_connectivity_column(f.name):
            node_cols[f.name] = value
        elif f.name == _CONTAINER_FIELD:
            container = graph_write.resolve_any_subclass(network, network.cim.EquipmentContainer, value)
            if container is None:
                raise ValueError(
                    f"{row.name!r}: {_CONTAINER_FIELD} {value!r} not found in graph "
                    f"(build containers before equipment that references them)"
                )
        elif f.name in ref_slots:
            deferred_fks.append((f.name, value))
        else:
            graph_write.set_attr(obj, network.cim, f.name, value)

    has_container_slot = _CONTAINER_FIELD in ref_slots
    if node_cols:
        connectivity.add_connectivity(network, obj, node_cols=node_cols, container=container)
    elif has_container_slot:
        resolved_container = container if container is not None else network.container
        if isinstance(resolved_container, network.cim.EquipmentContainer):
            graph_write.set_assc(obj, network.cim, _CONTAINER_FIELD, resolved_container)

    for attr, name in deferred_fks:
        target_cls_name = validate.reference_target_class(row_cls_name, attr)
        target = graph_write.resolve(network, getattr(network.cim, target_cls_name), name)
        graph_write.set_assc(obj, network.cim, attr, target)

    graph_write.add_to_graph(network, obj)
    return obj
