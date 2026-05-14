"""Create a CIM Disconnector (no-load isolating switch)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch._helpers import _build_switch

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_disconnector(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node1: "str | cim.ConnectivityNode",
    node2: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    open: bool = False,
    normal_open: bool = False,
    retained: bool = False,
) -> "cim.Disconnector":
    """Create a Disconnector between ``node1`` and ``node2``.

    A Disconnector provides an isolating distance in the open position.  It
    cannot break load current — it is only operated under no-load conditions.

    Args:
        network:        Graph model to add to.
        container:      EquipmentContainer the disconnector belongs to.
        name:           Human-readable name; also seeds the UUID.
        node1:          First ConnectivityNode (or its name).
        node2:          Second ConnectivityNode (or its name).
        base_voltage:   Optional BaseVoltage; inherits from container if None.
        open:           Current open/closed state.
        normal_open:    Normal (study-case) open/closed state.
        retained:       Whether retained in topology reduction.  ``False`` for
                        most disconnectors (they collapse to a node in studies).

    Returns:
        The created ``cim.Disconnector``.
    """
    cim = get_cim()
    return _build_switch(
        network, container, name, node1, node2,
        cim.Disconnector,
        base_voltage=base_voltage,
        open=open,
        normal_open=normal_open,
        retained=retained,
    )
