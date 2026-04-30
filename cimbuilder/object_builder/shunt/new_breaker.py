"""Create a CIM Breaker object.

Reference implementation of the Phase 0 signature pattern.  See
``.development/STYLE_GUIDE.md`` for the full specification.

Note: this primitive currently lives under ``shunt/`` because that is where
the pre-rewrite API put it.  Phase 1 moves it to ``switch/`` (its correct
CIM taxonomy location — Breaker is a Switch, not a Shunt) along with the
rest of the switch-family primitives.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.utils import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2023 as cim

_log = logging.getLogger(__name__)


def new_breaker(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node1: str | "cim.ConnectivityNode",
    node2: str | "cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    open: bool = False,
    normal_open: bool = False,
    retained: bool = True,
) -> "cim.Breaker":
    """Create a Breaker between ``node1`` and ``node2`` and add it to ``network``.

    A Breaker is a mechanical switching device capable of making, carrying,
    and breaking currents under normal circuit conditions and also under
    specified abnormal circuit conditions (such as a short circuit).

    Args:
        network:        Graph model to add the breaker to.
        container:      EquipmentContainer the breaker belongs to
                        (Substation, Feeder, VoltageLevel, ...).
        name:           Human-readable name; also used to seed the UUID.
        node1:          First ConnectivityNode, or its name as a string.
        node2:          Second ConnectivityNode, or its name as a string.
        base_voltage:   Optional BaseVoltage for the breaker.  If None, the
                        breaker inherits from its container.
        open:           Current open/closed state.  True = currently open.
        normal_open:    Normal (study-case) open/closed state.
        retained:       Whether the breaker is retained in bus-branch
                        topology reduction.  True for typical switching.

    Returns:
        The created ``cim.Breaker`` object.  Both terminals have already been
        created, wired to the nodes, and added to ``network``.
    """
    cim = get_cim()

    breaker = cim.Breaker(name=name)
    breaker.uuid(name=name, seed=str(node1) + str(node2))

    breaker.EquipmentContainer = container
    breaker.open = open
    breaker.normalOpen = normal_open
    breaker.retained = retained
    if base_voltage is not None:
        breaker.BaseVoltage = base_voltage

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.uuid(name=f"{name}_t1")
    t1.ConductingEquipment = breaker
    terminal_to_node(network, t1, node1)
    breaker.Terminals.append(t1)

    t2 = cim.Terminal(name=f"{name}_t2", sequenceNumber=2)
    t2.uuid(name=f"{name}_t2")
    t2.ConductingEquipment = breaker
    terminal_to_node(network, t2, node2)
    breaker.Terminals.append(t2)

    network.add_to_graph(breaker)
    network.add_to_graph(t1)
    network.add_to_graph(t2)

    return breaker
