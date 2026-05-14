"""Create a CIM ConnectivityNode."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_connectivity_node(
    network: GraphModel,
    container: "cim.ConnectivityNodeContainer",
    name: str,
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
) -> "cim.ConnectivityNode":
    """Create a ConnectivityNode in ``container`` and add it to ``network``.

    A ConnectivityNode is a physical bus point where Terminals connect.

    Args:
        network:        Graph model to add to.
        container:      The ConnectivityNodeContainer (Substation, VoltageLevel,
                        Feeder, ...) the node belongs to.
        name:           Human-readable name; seeds the UUID.
        base_voltage:   Optional BaseVoltage for the node.

    Returns:
        The created ``cim.ConnectivityNode``.
    """
    cim = get_cim()

    node = cim.ConnectivityNode(name=name)
    node.uuid(name=name)
    node.ConnectivityNodeContainer = container
    if base_voltage is not None:
        node.BaseVoltage = base_voltage

    network.add_to_graph(node)
    return node
