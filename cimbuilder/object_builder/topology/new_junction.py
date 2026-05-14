"""Create a CIM Junction (a Connector for joining two or more lines)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.terminal import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_junction(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
) -> "cim.Junction":
    """Create a Junction at ``node`` and add it to ``network``.

    A Junction is a one-terminal Connector used as an internal takeoff point in
    substation topologies (e.g. between a breaker bay and a feeder). It has no
    impedance and exists primarily to give the topology a stable named anchor.

    Args:
        network:        Graph model to add to.
        container:      EquipmentContainer.
        name:           Human-readable name; seeds the UUID.
        node:           ConnectivityNode (or its name).
        base_voltage:   Optional BaseVoltage; inherits from container if None.

    Returns:
        The created ``cim.Junction``.
    """
    cim = get_cim()

    junction = cim.Junction(name=name)
    junction.uuid(name=name)
    junction.EquipmentContainer = container
    if base_voltage is not None:
        junction.BaseVoltage = base_voltage

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.uuid(name=f"{name}_t1")
    t1.ConductingEquipment = junction
    terminal_to_node(network, t1, node)
    junction.Terminals.append(t1)

    network.add_to_graph(junction)
    network.add_to_graph(t1)

    return junction
