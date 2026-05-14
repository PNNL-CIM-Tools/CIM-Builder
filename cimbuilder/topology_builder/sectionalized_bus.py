"""Sectionalized-bus substation topology — pure free functions."""
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


def new_sectionalized_bus_substation(
    connection: ConnectionInterface,
    name: str,
    base_voltage: "int | float | cim.BaseVoltage",
    *,
    total_sections: int = 2,
    network: GraphModel | None = None,
) -> dict:
    """Create a sectionalized-bus substation.

    Creates ``total_sections`` bus ConnectivityNodes with BusbarSections, and
    ``total_sections - 1`` bus-tie trios connecting adjacent sections.

    Returns:
        dict with keys: ``network``, ``substation``, ``buses`` (list, 1-indexed
        by position), ``base_voltage``.
    """
    cim = get_cim()
    total_sections = int(total_sections)

    substation = cim.Substation(name=name)
    substation.uuid(name=name)

    if network is None:
        network = DistributedArea(connection=connection, container=substation, distributed=False)
    network.add_to_graph(substation)

    bv = get_or_create_base_voltage(network, base_voltage)

    buses = []
    for i in range(1, total_sections + 1):
        bus = cim.ConnectivityNode(name=f"{name}_bus_{i}")
        bus.uuid(name=f"{name}_bus_{i}")
        bus.ConnectivityNodeContainer = substation
        network.add_to_graph(bus)
        new_bus_bar_section(network, substation, f"{name}_bus_{i}", bus)
        buses.append(bus)

    for i in range(total_sections - 1):
        series = (i + 1) * 10
        _new_bus_tie_trio(network, substation, f"{name}_{series}", buses[i], buses[i + 1], bv)

    return {
        "network": network,
        "substation": substation,
        "buses": buses,
        "base_voltage": bv,
    }


def add_feeder_to_sectionalized_bus(
    network: GraphModel,
    substation: "cim.Substation",
    buses: "list[cim.ConnectivityNode]",
    base_voltage: "cim.BaseVoltage",
    section_number: int,
    breaker_number: int,
    feeder_network: GraphModel,
    feeder: "cim.Feeder",
    sourcebus: "cim.ConnectivityNode | None" = None,
) -> dict:
    """Add a feeder bay to a sectionalized-bus substation.

    Topology: buses[section_number-1] — ag1 — j1 — brk — j2 — ag2 — sourcebus

    Args:
        section_number: 1-based index selecting which bus section to connect to.
        breaker_number: Integer identifier; seeds equipment names.

    Returns:
        dict with keys: ``breaker``, ``disconnectors`` [ag1, ag2], ``junctions`` [j1, j2].
    """
    cim = get_cim()

    if sourcebus is None:
        sourcebus = get_source_bus(feeder_network, feeder)

    bus = buses[section_number - 1]

    j1 = cim.ConnectivityNode(name=f"{substation.name}_{breaker_number}_j1")
    j1.uuid(name=f"{substation.name}_{breaker_number}_j1")
    j1.ConnectivityNodeContainer = substation

    j2 = cim.ConnectivityNode(name=f"{substation.name}_{breaker_number}_j2")
    j2.uuid(name=f"{substation.name}_{breaker_number}_j2")
    j2.ConnectivityNodeContainer = substation

    ag1 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d1",
                           node1=bus, node2=j1)
    ag1.BaseVoltage = base_voltage

    brk = new_breaker(network, substation, name=f"{substation.name}_{breaker_number}",
                      node1=j1, node2=j2)
    brk.BaseVoltage = base_voltage

    ag2 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d2",
                           node1=j2, node2=sourcebus)
    ag2.BaseVoltage = base_voltage

    network.add_to_graph(j1)
    network.add_to_graph(j2)
    network.add_to_graph(sourcebus)
    network.add_to_graph(feeder)

    feeder.NormalEnergizingSubstation = substation
    substation.NormalEnergizedFeeder.append(feeder)

    return {
        "breaker": brk,
        "disconnectors": [ag1, ag2],
        "junctions": [j1, j2],
    }


def add_branch_to_sectionalized_bus(
    network: GraphModel,
    substation: "cim.Substation",
    buses: "list[cim.ConnectivityNode]",
    base_voltage: "cim.BaseVoltage",
    section_number: int,
    breaker_number: int,
    branch_terminal: "cim.Terminal",
) -> dict:
    """Add a branch bay to a sectionalized-bus substation.

    Topology: buses[section_number-1] — ag1 — j1 — brk — j2
              branch_terminal wired to j2.

    Returns:
        dict with keys: ``breaker``, ``disconnector``, ``junctions`` [j1, j2].
    """
    cim = get_cim()

    bus = buses[section_number - 1]

    j1 = cim.ConnectivityNode(name=f"{substation.name}_{breaker_number}_j1")
    j1.uuid(name=f"{substation.name}_{breaker_number}_j1")
    j1.ConnectivityNodeContainer = substation

    j2 = cim.ConnectivityNode(name=f"{substation.name}_{breaker_number}_j2")
    j2.uuid(name=f"{substation.name}_{breaker_number}_j2")
    j2.ConnectivityNodeContainer = substation

    ag1 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d1",
                           node1=bus, node2=j1)
    ag1.BaseVoltage = base_voltage

    brk = new_breaker(network, substation, name=f"{substation.name}_{breaker_number}",
                      node1=j1, node2=j2)
    brk.BaseVoltage = base_voltage

    branch_terminal.ConnectivityNode = j2

    network.add_to_graph(j1)
    network.add_to_graph(j2)

    return {
        "breaker": brk,
        "disconnector": ag1,
        "junctions": [j1, j2],
    }
