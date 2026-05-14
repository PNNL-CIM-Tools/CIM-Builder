"""Double-bus single-breaker substation topology — pure free functions."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.databases import ConnectionInterface
from cimgraph.models import DistributedArea, GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch.new_breaker import new_breaker
from cimbuilder.object_builder.switch.new_disconnector import new_disconnector
from cimbuilder.object_builder.topology.new_bus_bar_section import new_bus_bar_section
from cimbuilder.utils.base_voltage import get_or_create_base_voltage
from cimbuilder.utils.source_bus import get_source_bus
from cimbuilder.topology_builder._bays import _new_bus_tie_trio

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_double_bus_single_breaker_substation(
    connection: ConnectionInterface,
    name: str,
    base_voltage: "int | float | cim.BaseVoltage",
    *,
    network: GraphModel | None = None,
) -> dict:
    """Create a double-bus single-breaker substation.

    Creates north bus, south bus, BusbarSections, and one bus-tie
    (disconnector—breaker—disconnector).

    Returns:
        dict with keys: ``network``, ``substation``, ``north_bus``, ``south_bus``,
        ``base_voltage``.
    """
    cim = get_cim()

    substation = cim.Substation(name=name)
    substation.uuid(name=name)

    if network is None:
        network = DistributedArea(connection=connection, container=substation, distributed=False)
    network.add_to_graph(substation)

    bv = get_or_create_base_voltage(network, base_voltage)

    north_bus = cim.ConnectivityNode(name=f"{name}_north_bus")
    north_bus.uuid(name=f"{name}_north_bus")
    north_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(north_bus)
    new_bus_bar_section(network, substation, f"{name}_north_bus", north_bus)

    south_bus = cim.ConnectivityNode(name=f"{name}_south_bus")
    south_bus.uuid(name=f"{name}_south_bus")
    south_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(south_bus)
    new_bus_bar_section(network, substation, f"{name}_south_bus", south_bus)

    _new_bus_tie_trio(network, substation, name, north_bus, south_bus, bv)

    return {
        "network": network,
        "substation": substation,
        "north_bus": north_bus,
        "south_bus": south_bus,
        "base_voltage": bv,
    }


def add_feeder_to_double_bus_single_breaker(
    network: GraphModel,
    substation: "cim.Substation",
    north_bus: "cim.ConnectivityNode",
    south_bus: "cim.ConnectivityNode",
    base_voltage: "cim.BaseVoltage",
    breaker_number: int,
    feeder_network: GraphModel,
    feeder: "cim.Feeder",
    sourcebus: "cim.ConnectivityNode | None" = None,
) -> dict:
    """Add a feeder bay to a double-bus single-breaker substation.

    Topology: north_bus — ag1 — j1 — brk — sourcebus
              south_bus — ag2 — j1  (ag1 or ag2 normally open based on breaker_number parity)

    Even breaker_number: ag1 (north) is normally open.
    Odd breaker_number:  ag2 (south) is normally open.

    Returns:
        dict with keys: ``breaker``, ``disconnectors`` [ag1, ag2], ``junction``.
    """
    cim = get_cim()

    if sourcebus is None:
        sourcebus = get_source_bus(feeder_network, feeder)

    j1 = cim.ConnectivityNode(name=f"{substation.name}_{breaker_number}_j1")
    j1.uuid(name=f"{substation.name}_{breaker_number}_j1")
    j1.ConnectivityNodeContainer = substation

    ag1 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d1",
                           node1=north_bus, node2=j1)
    ag1.BaseVoltage = base_voltage

    brk = new_breaker(network, substation, name=f"{substation.name}_{breaker_number}",
                      node1=j1, node2=sourcebus)
    brk.BaseVoltage = base_voltage

    ag2 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d2",
                           node1=j1, node2=south_bus)
    ag2.BaseVoltage = base_voltage

    if breaker_number % 2 == 0:
        ag1.open = True
        ag1.normalOpen = True
    else:
        ag2.open = True
        ag2.normalOpen = True

    network.add_to_graph(j1)
    network.add_to_graph(sourcebus)
    network.add_to_graph(feeder)

    feeder.NormalEnergizingSubstation = substation
    substation.NormalEnergizedFeeder.append(feeder)

    return {
        "breaker": brk,
        "disconnectors": [ag1, ag2],
        "junction": j1,
    }


def add_branch_to_double_bus_single_breaker(
    network: GraphModel,
    substation: "cim.Substation",
    north_bus: "cim.ConnectivityNode",
    south_bus: "cim.ConnectivityNode",
    base_voltage: "cim.BaseVoltage",
    breaker_number: int,
    branch_terminal: "cim.Terminal",
) -> dict:
    """Add a branch bay to a double-bus single-breaker substation.

    Topology: north_bus — ag1 — j1 — brk — j2 — ag2 — j3 — ag3 — south_bus
              branch_terminal wired to j3.

    Returns:
        dict with keys: ``breaker``, ``disconnectors`` [ag1, ag2, ag3],
        ``junctions`` [j1, j2, j3].
    """
    cim = get_cim()

    j1 = cim.ConnectivityNode(name=f"{substation.name}_{breaker_number}_j1")
    j1.uuid(name=f"{substation.name}_{breaker_number}_j1")
    j1.ConnectivityNodeContainer = substation

    j2 = cim.ConnectivityNode(name=f"{substation.name}_{breaker_number}_j2")
    j2.uuid(name=f"{substation.name}_{breaker_number}_j2")
    j2.ConnectivityNodeContainer = substation

    j3 = cim.ConnectivityNode(name=f"{substation.name}_{breaker_number}_j3")
    j3.uuid(name=f"{substation.name}_{breaker_number}_j3")
    j3.ConnectivityNodeContainer = substation

    ag1 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d1",
                           node1=north_bus, node2=j1)
    ag1.BaseVoltage = base_voltage

    brk = new_breaker(network, substation, name=f"{substation.name}_{breaker_number}",
                      node1=j1, node2=j2)
    brk.BaseVoltage = base_voltage

    ag2 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d2",
                           node1=j2, node2=j3)
    ag2.BaseVoltage = base_voltage

    ag3 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d3",
                           node1=j3, node2=south_bus)
    ag3.BaseVoltage = base_voltage

    branch_terminal.ConnectivityNode = j3

    network.add_to_graph(j1)
    network.add_to_graph(j2)
    network.add_to_graph(j3)

    return {
        "breaker": brk,
        "disconnectors": [ag1, ag2, ag3],
        "junctions": [j1, j2, j3],
    }
