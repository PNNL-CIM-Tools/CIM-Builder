"""Generic two-terminal CIM object factory."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.terminal import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_two_terminal_object(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node1: "str | cim.ConnectivityNode",
    node2: "str | cim.ConnectivityNode",
    class_type: type,
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
) -> object:
    """Create a two-terminal CIM ConductingEquipment of ``class_type``.

    Useful for ad-hoc series equipment that doesn't yet have a dedicated
    primitive.  Prefer the dedicated primitives where available.

    Args:
        network:        Graph model to add to.
        container:      EquipmentContainer.
        name:           Human-readable name; seeds the UUID.
        node1, node2:   Endpoint ConnectivityNodes (or names).
        class_type:     CIM class to instantiate (must be a ConductingEquipment).
        base_voltage:   Optional BaseVoltage; inherits from container if None.

    Returns:
        The created object of type ``class_type``.
    """
    cim = get_cim()

    obj = class_type(name=name)
    obj.uuid(name=name)
    obj.EquipmentContainer = container
    if base_voltage is not None:
        obj.BaseVoltage = base_voltage

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.uuid(name=f"{name}_t1")
    t1.ConductingEquipment = obj
    terminal_to_node(network, t1, node1)
    obj.Terminals.append(t1)

    t2 = cim.Terminal(name=f"{name}_t2", sequenceNumber=2)
    t2.uuid(name=f"{name}_t2")
    t2.ConductingEquipment = obj
    terminal_to_node(network, t2, node2)
    obj.Terminals.append(t2)

    network.add_to_graph(obj)
    network.add_to_graph(t1)
    network.add_to_graph(t2)

    return obj
