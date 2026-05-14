"""Shared helpers for switch-family primitives.

All Switch subclasses (Breaker, Disconnector, Fuse, LoadBreakSwitch, ...)
share the same two-terminal wiring and the same set of base attributes from
the CIM ``Switch`` class.  ``_build_switch`` does that wiring once.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.terminal import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim


def _build_switch(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node1: "str | cim.ConnectivityNode",
    node2: "str | cim.ConnectivityNode",
    switch_class: type,
    *,
    base_voltage: "cim.BaseVoltage | None",
    open: bool,
    normal_open: bool,
    retained: bool,
) -> object:
    """Create a Switch subclass instance with two terminals wired up.

    Returns the constructed switch.  Caller is responsible for setting any
    attributes specific to the subclass (e.g. ``breakingCapacity`` on Breaker).
    """
    cim = get_cim()

    switch = switch_class(name=name)
    switch.uuid(name=name, seed=str(node1) + str(node2))

    switch.EquipmentContainer = container
    switch.open = open
    switch.normalOpen = normal_open
    switch.retained = retained
    if base_voltage is not None:
        switch.BaseVoltage = base_voltage

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.uuid(name=f"{name}_t1")
    t1.ConductingEquipment = switch
    terminal_to_node(network, t1, node1)
    switch.Terminals.append(t1)

    t2 = cim.Terminal(name=f"{name}_t2", sequenceNumber=2)
    t2.uuid(name=f"{name}_t2")
    t2.ConductingEquipment = switch
    terminal_to_node(network, t2, node2)
    switch.Terminals.append(t2)

    network.add_to_graph(switch)
    network.add_to_graph(t1)
    network.add_to_graph(t2)

    return switch
