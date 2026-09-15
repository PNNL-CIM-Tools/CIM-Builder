"""Phase 4: the connectivity backend - node/bus/terminal/phase (design: CIMTBL_DESIGN.md §5, §12.4).

The one place that knows §3.5's node*/bus* vocabulary and §3.6's phase-child
synthesis. Every Builder's add_connectivity (Phase 5) is a thin wrapper around
these two functions - no per-class node-vs-bus or phase logic anywhere else.
"""

import typing

from cimgraph.models import GraphModel

from cimbuilder.core import graph_write


def _node_cls(network: GraphModel, col_name: str) -> type:
    """§3.5's one non-reflective naming rule: node* -> ConnectivityNode,
    bus* -> TopologicalNode. Fails fast on anything else - no silent
    fallback for a column that isn't part of the fixed vocabulary."""
    if col_name.startswith('node'):
        return network.cim.ConnectivityNode
    if col_name.startswith('bus'):
        return network.cim.TopologicalNode
    raise ValueError(
        f"{col_name!r} is not a connectivity column (must start with "
        f"'node' or 'bus', per CIMTBL_DESIGN.md §3.5)"
    )


def _parent_assoc_field(phase_cls: type, parent: object) -> str:
    """The field on phase_cls whose type is the parent's class (or a base of
    it) - not always type(parent).__name__ (e.g. LinearShuntCompensatorPhase's
    field is 'ShuntCompensator', the base class name, not
    'LinearShuntCompensator'). Same typing.get_type_hints resolution
    graph_write._cim_unit_type uses for CIMUnit, applied to find the
    parent-association field instead."""
    hints = typing.get_type_hints(phase_cls)
    for field_name, hint in hints.items():
        for arg in typing.get_args(hint) or (hint,):
            if isinstance(arg, type) and isinstance(parent, arg):
                return field_name
    raise ValueError(
        f"{phase_cls.__name__} has no field whose type matches "
        f"{type(parent).__name__}"
    )


def add_connectivity(network: GraphModel, obj: object, *, node_cols: dict[str, str],
                      container: object = None) -> list[object]:
    """node_cols is the already-disambiguated {'node1': 'busA', 'bus2': 'busB', ...}
    slice of a <Class>Row - the caller picks which of the row's fields are
    connectivity columns. Auto-vivifies any name not found via resolve().
    Returns Terminals in column order (sequenceNumber = list index + 1).

    Sets obj.EquipmentContainer from `container`, falling back to
    network.container when not given - the one unambiguous container
    available today (.cimtbl has no per-row/per-table container syntax yet).
    Propagates the same container onto every node touched
    (ConnectivityNodeContainer), without overwriting one already set."""
    cim = network.cim
    resolved_container = container if container is not None else network.container
    has_container = isinstance(resolved_container, cim.EquipmentContainer)

    terminals = []
    for i, (col_name, node_name) in enumerate(node_cols.items(), start=1):
        node_cls = _node_cls(network, col_name)
        node_obj = graph_write.resolve(network, node_cls, node_name)
        if node_obj is None:
            node_obj = node_cls(name=node_name)
            graph_write.add_to_graph(network, node_obj)

        if has_container and node_obj.ConnectivityNodeContainer is None:
            graph_write.set_assc(node_obj, cim, 'ConnectivityNodeContainer', resolved_container)

        terminal = cim.Terminal(name=f'{obj.name}_T{i}', sequenceNumber=i)
        graph_write.set_assc(terminal, cim, 'ConductingEquipment', obj)

        if node_cls is cim.ConnectivityNode:
            graph_write.set_assc(terminal, cim, 'ConnectivityNode', node_obj)
        else:
            graph_write.set_assc(terminal, cim, 'TopologicalNode', node_obj)

        graph_write.add_to_graph(network, terminal)
        terminals.append(terminal)

    if has_container:
        graph_write.set_assc(obj, cim, 'EquipmentContainer', resolved_container)

    return terminals


def add_phase_children(network: GraphModel, obj: object, terminals: list[object],
                        *, phases: str, phase_cls: type) -> list[object]:
    """phases='ABCN' -> phase_cls (e.g. ACLineSegmentPhase) instances per §3.6,
    wired to obj and given correct SinglePhaseKind + sequenceNumber."""
    cim = network.cim
    parent_field = _parent_assoc_field(phase_cls, obj)
    has_sequence_number = 'sequenceNumber' in typing.get_type_hints(phase_cls)

    children = []
    for i, letter in enumerate(phases, start=1):
        child = phase_cls(name=f'{obj.name}_{letter}', phase=cim.SinglePhaseKind(letter))
        if has_sequence_number:
            child.sequenceNumber = i
        graph_write.set_assc(child, cim, parent_field, obj)
        graph_write.add_to_graph(network, child)
        children.append(child)

    return children
