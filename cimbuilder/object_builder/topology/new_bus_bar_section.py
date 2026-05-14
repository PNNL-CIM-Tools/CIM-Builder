"""Create a CIM BusbarSection (the physical busbar at a node)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.terminal import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_bus_bar_section(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    ip_max_A: float | None = None,
) -> "cim.BusbarSection":
    """Create a BusbarSection at ``node`` and add it to ``network``.

    A BusbarSection is a fixed-impedance Connector that represents a section of
    a substation busbar.  It is one-terminal — the Terminal anchors the section
    to the bus's ConnectivityNode.

    Args:
        network:        Graph model to add to.
        container:      EquipmentContainer.
        name:           Human-readable name; seeds the UUID.
        node:           ConnectivityNode (or its name) the busbar attaches to.
        base_voltage:   Optional BaseVoltage; inherits from container if None.
        ip_max_A:       Maximum short-circuit current the bus can carry, in A.

    Returns:
        The created ``cim.BusbarSection``.
    """
    cim = get_cim()

    busbar = cim.BusbarSection(name=name)
    busbar.uuid(name=name)
    busbar.EquipmentContainer = container
    if base_voltage is not None:
        busbar.BaseVoltage = base_voltage
    if ip_max_A is not None:
        busbar.ipMax = cim.CurrentFlow(ip_max_A, "A")

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.uuid(name=f"{name}_t1")
    t1.ConductingEquipment = busbar
    terminal_to_node(network, t1, node)
    busbar.Terminals.append(t1)

    network.add_to_graph(busbar)
    network.add_to_graph(t1)

    return busbar
