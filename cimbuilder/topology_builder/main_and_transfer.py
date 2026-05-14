"""Main-and-transfer bus substation topology — pure free functions."""
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


def new_main_and_transfer_substation(
    connection: ConnectionInterface,
    name: str,
    base_voltage: "int | float | cim.BaseVoltage",
    *,
    network: GraphModel | None = None,
) -> dict:
    """Create a main-and-transfer bus substation.

    Creates main bus, transfer bus, BusbarSections, and a bus-tie
    (disconnector—breaker—disconnector) between them.

    Returns:
        dict with keys: ``network``, ``substation``, ``main_bus``, ``transfer_bus``,
        ``base_voltage``.
    """
    cim = get_cim()

    substation = cim.Substation(name=name)
    substation.uuid(name=name)

    if network is None:
        network = DistributedArea(connection=connection, container=substation, distributed=False)
    network.add_to_graph(substation)

    bv = get_or_create_base_voltage(network, base_voltage)

    main_bus = cim.ConnectivityNode(name=f"{name}_main_bus")
    main_bus.uuid(name=f"{name}_main_bus")
    main_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(main_bus)
    new_bus_bar_section(network, substation, f"{name}_main_bus", main_bus)

    transfer_bus = cim.ConnectivityNode(name=f"{name}_transfer_bus")
    transfer_bus.uuid(name=f"{name}_transfer_bus")
    transfer_bus.ConnectivityNodeContainer = substation
    network.add_to_graph(transfer_bus)
    new_bus_bar_section(network, substation, f"{name}_transfer_bus", transfer_bus)

    _new_bus_tie_trio(network, substation, name, main_bus, transfer_bus, bv)

    return {
        "network": network,
        "substation": substation,
        "main_bus": main_bus,
        "transfer_bus": transfer_bus,
        "base_voltage": bv,
    }


def add_feeder_to_main_and_transfer(
    network: GraphModel,
    substation: "cim.Substation",
    main_bus: "cim.ConnectivityNode",
    transfer_bus: "cim.ConnectivityNode",
    base_voltage: "cim.BaseVoltage",
    breaker_number: int,
    feeder_network: GraphModel,
    feeder: "cim.Feeder",
    sourcebus: "cim.ConnectivityNode | None" = None,
) -> dict:
    """Add a feeder bay to a main-and-transfer substation.

    Topology: main_bus — ag1 — j1 — brk — j2 — ag2 — sourcebus — ag3 — transfer_bus
              ag3 is normally open (transfer tie).

    Returns:
        dict with keys: ``breaker``, ``disconnectors`` [ag1, ag2, ag3],
        ``junctions`` [j1, j2].
    """
    cim = get_cim()

    if sourcebus is None:
        sourcebus = get_source_bus(feeder_network, feeder)

    j1 = cim.ConnectivityNode(name=f"{substation.name}_{breaker_number}_j1")
    j1.uuid(name=f"{substation.name}_{breaker_number}_j1")
    j1.ConnectivityNodeContainer = substation

    j2 = cim.ConnectivityNode(name=f"{substation.name}_{breaker_number}_j2")
    j2.uuid(name=f"{substation.name}_{breaker_number}_j2")
    j2.ConnectivityNodeContainer = substation

    ag1 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d1",
                           node1=main_bus, node2=j1)
    ag1.BaseVoltage = base_voltage

    brk = new_breaker(network, substation, name=f"{substation.name}_{breaker_number}",
                      node1=j1, node2=j2)
    brk.BaseVoltage = base_voltage

    ag2 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d2",
                           node1=j2, node2=sourcebus)
    ag2.BaseVoltage = base_voltage

    # Transfer tie: sourcebus to transfer bus, normally open
    ag3 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d3",
                           node1=sourcebus, node2=transfer_bus)
    ag3.BaseVoltage = base_voltage
    ag3.open = True
    ag3.normalOpen = True

    network.add_to_graph(j1)
    network.add_to_graph(j2)
    network.add_to_graph(sourcebus)
    network.add_to_graph(feeder)

    feeder.NormalEnergizingSubstation = substation
    substation.NormalEnergizedFeeder.append(feeder)

    return {
        "breaker": brk,
        "disconnectors": [ag1, ag2, ag3],
        "junctions": [j1, j2],
    }


def add_branch_to_main_and_transfer(
    network: GraphModel,
    substation: "cim.Substation",
    main_bus: "cim.ConnectivityNode",
    transfer_bus: "cim.ConnectivityNode",
    base_voltage: "cim.BaseVoltage",
    breaker_number: int,
    branch_terminal: "cim.Terminal",
) -> dict:
    """Add a branch bay to a main-and-transfer substation.

    Topology: main_bus — ag1 — j1 — brk — j2 — ag2 — j3 — ag3 — transfer_bus
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
                           node1=main_bus, node2=j1)
    ag1.BaseVoltage = base_voltage

    brk = new_breaker(network, substation, name=f"{substation.name}_{breaker_number}",
                      node1=j1, node2=j2)
    brk.BaseVoltage = base_voltage

    ag2 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d2",
                           node1=j2, node2=j3)
    ag2.BaseVoltage = base_voltage

    ag3 = new_disconnector(network, substation, name=f"{substation.name}_{breaker_number}d3",
                           node1=j3, node2=transfer_bus)
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
