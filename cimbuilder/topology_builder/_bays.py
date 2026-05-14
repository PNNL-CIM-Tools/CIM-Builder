"""Shared internal helpers for substation bay construction."""
from __future__ import annotations

from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch.new_breaker import new_breaker
from cimbuilder.object_builder.switch.new_disconnector import new_disconnector

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim


def _new_feeder_bay(
    network: GraphModel,
    substation: "cim.Substation",
    name_prefix: str,
    bus: "cim.ConnectivityNode",
    sourcebus: "cim.ConnectivityNode",
    base_voltage: "cim.BaseVoltage",
) -> dict:
    """Build a feeder bay: bus—ag1—j1—brk—j2—sourcebus.

    Returns dict with keys: breaker, disconnectors [ag1, ag2], junctions [j1, j2].
    """
    cim = get_cim()

    j1 = cim.ConnectivityNode(name=f"{name_prefix}_j1")
    j1.uuid(name=f"{name_prefix}_j1")
    j1.ConnectivityNodeContainer = substation

    j2 = cim.ConnectivityNode(name=f"{name_prefix}_j2")
    j2.uuid(name=f"{name_prefix}_j2")
    j2.ConnectivityNodeContainer = substation

    ag1 = new_disconnector(network, substation, name=f"{name_prefix}d1", node1=bus, node2=j1)
    ag1.BaseVoltage = base_voltage

    brk = new_breaker(network, substation, name=name_prefix, node1=j1, node2=j2)
    brk.BaseVoltage = base_voltage

    ag2 = new_disconnector(network, substation, name=f"{name_prefix}d2", node1=j2, node2=sourcebus)
    ag2.BaseVoltage = base_voltage

    network.add_to_graph(j1)
    network.add_to_graph(j2)

    return {
        "breaker": brk,
        "disconnectors": [ag1, ag2],
        "junctions": [j1, j2],
    }


def _new_branch_bay(
    network: GraphModel,
    substation: "cim.Substation",
    name_prefix: str,
    bus: "cim.ConnectivityNode",
    branch_terminal: "cim.Terminal",
    base_voltage: "cim.BaseVoltage",
) -> dict:
    """Build a branch bay: bus—ag1—j1—brk—j2, wire branch_terminal to j2.

    Returns dict with keys: breaker, disconnector, junctions [j1, j2].
    """
    cim = get_cim()

    j1 = cim.ConnectivityNode(name=f"{name_prefix}_j1")
    j1.uuid(name=f"{name_prefix}_j1")
    j1.ConnectivityNodeContainer = substation

    j2 = cim.ConnectivityNode(name=f"{name_prefix}_j2")
    j2.uuid(name=f"{name_prefix}_j2")
    j2.ConnectivityNodeContainer = substation

    ag1 = new_disconnector(network, substation, name=f"{name_prefix}d1", node1=bus, node2=j1)
    ag1.BaseVoltage = base_voltage

    brk = new_breaker(network, substation, name=name_prefix, node1=j1, node2=j2)
    brk.BaseVoltage = base_voltage

    branch_terminal.ConnectivityNode = j2

    network.add_to_graph(j1)
    network.add_to_graph(j2)

    return {
        "breaker": brk,
        "disconnector": ag1,
        "junctions": [j1, j2],
    }


def _new_bus_tie_trio(
    network: GraphModel,
    substation: "cim.Substation",
    name_prefix: str,
    from_bus: "str | cim.ConnectivityNode",
    to_bus: "str | cim.ConnectivityNode",
    base_voltage: "cim.BaseVoltage",
) -> dict:
    """Build a disconnector—breaker—disconnector bus-tie: from_bus—ag1—j1—brk—j2—ag2—to_bus.

    Returns dict with keys: bus_tie, disconnectors [ag1, ag2], junctions [j1, j2].
    """
    cim = get_cim()

    j1 = cim.ConnectivityNode(name=f"{name_prefix}_bt_j1")
    j1.uuid(name=f"{name_prefix}_bt_j1")
    j1.ConnectivityNodeContainer = substation

    j2 = cim.ConnectivityNode(name=f"{name_prefix}_bt_j2")
    j2.uuid(name=f"{name_prefix}_bt_j2")
    j2.ConnectivityNodeContainer = substation

    ag1 = new_disconnector(network, substation, name=f"{name_prefix}_bt_d1", node1=from_bus, node2=j1)
    ag1.BaseVoltage = base_voltage

    brk = new_breaker(network, substation, name=f"{name_prefix}_bus_tie", node1=j1, node2=j2)
    brk.BaseVoltage = base_voltage

    ag2 = new_disconnector(network, substation, name=f"{name_prefix}_bt_d2", node1=j2, node2=to_bus)
    ag2.BaseVoltage = base_voltage

    network.add_to_graph(j1)
    network.add_to_graph(j2)

    return {
        "bus_tie": brk,
        "disconnectors": [ag1, ag2],
        "junctions": [j1, j2],
    }
