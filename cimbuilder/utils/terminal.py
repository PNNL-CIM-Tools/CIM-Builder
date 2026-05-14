"""Terminal-to-ConnectivityNode wiring helper."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def terminal_to_node(
    network: GraphModel,
    terminal: "cim.Terminal",
    node: "str | cim.ConnectivityNode",
) -> None:
    """Wire ``terminal`` to ``node`` (object or name).

    If ``node`` is a string, the matching ConnectivityNode is looked up in
    ``network.graph`` by ``name`` or ``aliasName``.  Either way, the terminal's
    ``ConnectivityNode`` field is set and the node's ``Terminals`` list is
    appended.

    Args:
        network:   GraphModel containing the ConnectivityNode if ``node`` is a string.
        terminal:  Terminal to wire.
        node:      ConnectivityNode object, or its name/aliasName as a string.
    """
    cim = get_cim()

    if isinstance(node, str):
        for node_obj in network.graph.get(cim.ConnectivityNode, {}).values():
            if node_obj.name == node or node_obj.aliasName == node:
                terminal.ConnectivityNode = node_obj
                node_obj.Terminals.append(terminal)
                return
        _log.warning("ConnectivityNode named %r not found in network", node)
    else:
        terminal.ConnectivityNode = node
        node.Terminals.append(terminal)
