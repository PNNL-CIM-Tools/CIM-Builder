"""Locate the head/source ConnectivityNode for a Feeder."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def get_source_bus(
    feeder_network: GraphModel,
    feeder: "cim.Feeder",
) -> "cim.ConnectivityNode | None":
    """Return the source ConnectivityNode for ``feeder``.

    Resolution order:
        1. ``feeder.NormalHeadTerminal.ConnectivityNode`` if set.
        2. The ConnectivityNode named ``'sourcebus'`` attached to any
           ``EnergySource`` in ``feeder_network``.

    Args:
        feeder_network: Graph containing the feeder's equipment.
        feeder:         The Feeder being inspected.

    Returns:
        The source bus, or ``None`` if it cannot be found (an error is logged).
    """
    cim = get_cim()
    feeder_network.get_all_edges(cim.EnergySource)
    feeder_network.get_all_edges(cim.Terminal)
    feeder_network.get_all_edges(cim.ConnectivityNode)

    # cimhub_2026 uses a list for NormalHeadTerminal; cimhub_2023 uses a scalar.
    head = feeder.NormalHeadTerminal
    if isinstance(head, list):
        head = head[0] if head else None
    if head is not None:
        return head.ConnectivityNode

    for source in feeder_network.graph.get(cim.EnergySource, {}).values():
        if source.Terminals[0].ConnectivityNode.name == "sourcebus":
            return source.Terminals[0].ConnectivityNode

    _log.error("Could not find sourcebus for %s", feeder.name)
    return None
