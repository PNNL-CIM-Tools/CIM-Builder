"""Phase 3: reflective column -> attr/assoc/synthesis binder (design: CIMTBL_DESIGN.md §2.1).

bind_row covers this phase's slice of §2.1's reflection table: plain scalar
attrs and units, resolved against `network.cim` with no per-class code. FK
resolution and hand-coded synthesis are later phases (Phase 4/5) - none of
this phase's four target classes carry either in the ieee13 sample.
"""

import dataclasses

from cimgraph.models import GraphModel

from cimbuilder.core import graph_write

_ROW_SUFFIX = 'Row'
_SKIP_FIELDS = {'name', 'source_file', 'source_line'}


def bind_row(network: GraphModel, row: object) -> object:
    """Validated <Class>Row -> live cim-graph object, added to network."""
    row_cls_name = type(row).__name__
    cim_cls_name = row_cls_name.removesuffix(_ROW_SUFFIX)
    cim_cls = getattr(network.cim, cim_cls_name)

    obj = cim_cls(name=row.name)

    for f in dataclasses.fields(row):
        if f.name in _SKIP_FIELDS:
            continue
        value = getattr(row, f.name)
        if value is None:
            continue
        graph_write.set_attr(obj, f.name, value)

    graph_write.add_to_graph(network, obj)
    return obj
