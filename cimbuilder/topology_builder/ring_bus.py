"""Ring-bus substation topology — pure free functions."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.databases import ConnectionInterface
from cimgraph.models import DistributedArea, GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch.new_disconnector import new_disconnector
from cimbuilder.object_builder.topology.new_bus_bar_section import new_bus_bar_section
from cimbuilder.utils.base_voltage import get_or_create_base_voltage
from cimbuilder.utils.source_bus import get_source_bus
from cimbuilder.topology_builder._bays import _new_bus_tie_trio

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_ring_bus_substation(
    connection: ConnectionInterface,
    name: str,
    base_voltage: "int | float | cim.BaseVoltage",
    *,
    total_sections: int = 4,
    network: GraphModel | None = None,
) -> dict:
    """Create a ring-bus substation.

    Creates ``total_sections`` bus ConnectivityNodes with BusbarSections and
    ring-section breaker-and-disconnector trios connecting each adjacent pair
    (including last→first to close the ring).

    Returns:
        dict with keys: ``network``, ``substation``, ``buses`` (list of
        ConnectivityNodes, 1-indexed by position), ``base_voltage``.
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

    # Connect adjacent buses with a trio, including wrap-around
    for i in range(total_sections):
        from_bus = buses[i]
        to_bus = buses[(i + 1) % total_sections]
        series = (i + 1) * 10
        _new_bus_tie_trio(network, substation, f"{name}_{series}", from_bus, to_bus, bv)

    return {
        "network": network,
        "substation": substation,
        "buses": buses,
        "base_voltage": bv,
    }


def add_feeder_to_ring_bus(
    network: GraphModel,
    substation: "cim.Substation",
    buses: "list[cim.ConnectivityNode]",
    base_voltage: "cim.BaseVoltage",
    bus_number: int,
    feeder_network: GraphModel,
    feeder: "cim.Feeder",
    sourcebus: "cim.ConnectivityNode | None" = None,
) -> dict:
    """Add a feeder tap to a ring-bus substation via a single disconnector.

    Attaches: buses[bus_number-1] — ag1 — sourcebus

    Args:
        bus_number: 1-based index into the ``buses`` list.

    Returns:
        dict with keys: ``disconnector``.
    """
    if sourcebus is None:
        sourcebus = get_source_bus(feeder_network, feeder)

    bus = buses[bus_number - 1]
    ag1 = new_disconnector(network, substation, name=f"{substation.name}_d{bus_number}",
                           node1=bus, node2=sourcebus)
    ag1.BaseVoltage = base_voltage

    network.add_to_graph(sourcebus)
    network.add_to_graph(feeder)

    feeder.NormalEnergizingSubstation = substation
    substation.NormalEnergizedFeeder.append(feeder)

    return {"disconnector": ag1}


def add_branch_to_ring_bus(
    network: GraphModel,
    substation: "cim.Substation",
    buses: "list[cim.ConnectivityNode]",
    base_voltage: "cim.BaseVoltage",
    bus_number: int,
    branch_terminal: "cim.Terminal",
) -> dict:
    """Add a branch tap to a ring-bus substation via a single disconnector and junction.

    Attaches: buses[bus_number-1] — ag1 — j1, branch_terminal wired to j1.

    Args:
        bus_number: 1-based index into the ``buses`` list.

    Returns:
        dict with keys: ``disconnector``, ``junction``.
    """
    cim = get_cim()

    bus = buses[bus_number - 1]

    j1 = cim.ConnectivityNode(name=f"{substation.name}_{bus_number}_j1")
    j1.uuid(name=f"{substation.name}_{bus_number}_j1")
    j1.ConnectivityNodeContainer = substation

    ag1 = new_disconnector(network, substation, name=f"{substation.name}_d{bus_number}",
                           node1=bus, node2=j1)
    ag1.BaseVoltage = base_voltage

    branch_terminal.ConnectivityNode = j1
    network.add_to_graph(j1)

    return {"disconnector": ag1, "junction": j1}
