"""Breaker-and-a-half substation topology — pure free functions."""
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

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def _new_breaker_and_half_bus_tie(
    network: GraphModel,
    substation: "cim.Substation",
    tie_number: int,
    main_bus_1: "cim.ConnectivityNode",
    main_bus_2: "cim.ConnectivityNode",
    base_voltage: "cim.BaseVoltage",
    name: str,
) -> list:
    """Build one breaker-and-a-half bus-tie column (8 junctions, 3 breakers, 6 disconnectors).

    The 8-junction ladder:
        bus1 — ag1 — j0 — ag2 — j1 — bt1 — j2 — ag3 — j3 — bt2 — j4 — ag4 — j5 — bt3 — j6 — ag5 — j7 — ag6 — bus2

    Standard layout (simplified from the class-based implementation):
        bus1 — ag1 — j[0] — bt1 — j[1]
                                    |
                               ag2 — j[2] — bt2 — j[3]
                                                    |
                                               ag3 — j[4] — bt3 — j[5]
                                                                    |
                                               bus2 — ag4 — j[6] — (unused j[7])

    Porting directly from the original class-based BreakerAndHalfSubstation.new_bus_tie().

    Returns the list of 8 junction ConnectivityNodes.
    """
    cim = get_cim()
    n = 8
    junctions = []
    for i in range(n):
        j = cim.ConnectivityNode(name=f"{substation.name}_{tie_number}_bt_j{i + 1}")
        j.uuid(name=f"{substation.name}_{tie_number}_bt_j{i + 1}")
        j.ConnectivityNodeContainer = substation
        junctions.append(j)

    t = tie_number * 10

    bt1 = new_breaker(network, substation, name=f"{name}_bt_{t}",
                      node1=junctions[0], node2=junctions[1])
    ag1 = new_disconnector(network, substation, name=f"{name}_bt_{10 + t + 1}",
                           node1=main_bus_1, node2=junctions[0])
    ag2 = new_disconnector(network, substation, name=f"{name}_bt_{10 + t + 2}",
                           node1=junctions[1], node2=junctions[2])

    bt2 = new_breaker(network, substation, name=f"{name}_bt_{2 * t}",
                      node1=junctions[3], node2=junctions[4])
    ag3 = new_disconnector(network, substation, name=f"{name}_bt_{20 + t + 1}",
                           node1=junctions[2], node2=junctions[3])
    ag4 = new_disconnector(network, substation, name=f"{name}_bt_{20 + t + 2}",
                           node1=junctions[4], node2=junctions[5])

    bt3 = new_breaker(network, substation, name=f"{name}_bt_{3 * t}",
                      node1=junctions[6], node2=junctions[7])
    ag5 = new_disconnector(network, substation, name=f"{name}_bt_{30 + t + 1}",
                           node1=junctions[5], node2=junctions[6])
    ag6 = new_disconnector(network, substation, name=f"{name}_bt_{30 + t + 2}",
                           node1=junctions[7], node2=main_bus_2)

    for eq in (bt1, bt2, bt3, ag1, ag2, ag3, ag4, ag5, ag6):
        eq.BaseVoltage = base_voltage

    for j in junctions:
        network.add_to_graph(j)

    return junctions


def new_breaker_and_half_substation(
    connection: ConnectionInterface,
    name: str,
    base_voltage: "int | float | cim.BaseVoltage",
    *,
    total_bus_ties: int = 2,
    network: GraphModel | None = None,
) -> dict:
    """Create a breaker-and-a-half substation.

    Creates two main buses and ``total_bus_ties`` bus-tie columns.

    Returns:
        dict with keys: ``network``, ``substation``, ``main_bus_1``, ``main_bus_2``,
        ``bus_tie_junctions`` (list of lists), ``base_voltage``.
    """
    cim = get_cim()

    substation = cim.Substation(name=name)
    substation.uuid(name=name)

    if network is None:
        network = DistributedArea(connection=connection, container=substation, distributed=False)
    network.add_to_graph(substation)

    bv = get_or_create_base_voltage(network, base_voltage)

    main_bus_1 = cim.ConnectivityNode(name=f"{name}_main_bus_1")
    main_bus_1.uuid(name=f"{name}_main_bus_1")
    main_bus_1.ConnectivityNodeContainer = substation
    network.add_to_graph(main_bus_1)
    new_bus_bar_section(network, substation, f"{name}_main_bus_1", main_bus_1)

    main_bus_2 = cim.ConnectivityNode(name=f"{name}_main_bus_2")
    main_bus_2.uuid(name=f"{name}_main_bus_2")
    main_bus_2.ConnectivityNodeContainer = substation
    network.add_to_graph(main_bus_2)
    new_bus_bar_section(network, substation, f"{name}_main_bus_2", main_bus_2)

    bus_tie_junctions = []
    for tie in range(total_bus_ties):
        junctions = _new_breaker_and_half_bus_tie(
            network, substation, tie, main_bus_1, main_bus_2, bv, name,
        )
        bus_tie_junctions.append(junctions)

    return {
        "network": network,
        "substation": substation,
        "main_bus_1": main_bus_1,
        "main_bus_2": main_bus_2,
        "bus_tie_junctions": bus_tie_junctions,
        "base_voltage": bv,
    }


def add_feeder_to_breaker_and_half(
    network: GraphModel,
    substation: "cim.Substation",
    bus_tie_junctions: "list[list[cim.ConnectivityNode]]",
    base_voltage: "cim.BaseVoltage",
    breaker_number: int,
    tie_number: int,
    feeder_network: GraphModel,
    feeder: "cim.Feeder",
    sourcebus: "cim.ConnectivityNode | None" = None,
) -> dict:
    """Add a feeder tap to a breaker-and-a-half substation.

    Connects sourcebus to the appropriate lateral junction of the specified tie column
    via a single disconnector.

    Even breaker_number attaches to j[5] (lower lateral); odd to j[2] (upper lateral).

    Returns:
        dict with keys: ``disconnector``.
    """
    if sourcebus is None:
        sourcebus = get_source_bus(feeder_network, feeder)

    junctions = bus_tie_junctions[tie_number]
    jcn = junctions[5] if breaker_number % 2 == 0 else junctions[2]

    ag = new_disconnector(network, substation,
                          name=f"{substation.name}_{10 * breaker_number}",
                          node1=jcn, node2=sourcebus)
    ag.BaseVoltage = base_voltage

    network.add_to_graph(sourcebus)
    network.add_to_graph(feeder)

    feeder.NormalEnergizingSubstation = substation
    substation.NormalEnergizedFeeder.append(feeder)

    return {"disconnector": ag}


def add_branch_to_breaker_and_half(
    network: GraphModel,
    substation: "cim.Substation",
    bus_tie_junctions: "list[list[cim.ConnectivityNode]]",
    base_voltage: "cim.BaseVoltage",
    breaker_number: int,
    tie_number: int,
    branch_terminal: "cim.Terminal",
) -> dict:
    """Add a branch tap to a breaker-and-a-half substation.

    Connects branch_terminal to the appropriate lateral junction via a disconnector
    and a new junction node.

    Returns:
        dict with keys: ``disconnector``, ``junction``.
    """
    cim = get_cim()

    junctions = bus_tie_junctions[tie_number]
    jcn_num = 2 if breaker_number % 2 == 0 else 1
    jcn = junctions[5] if breaker_number % 2 == 0 else junctions[2]

    j_new = cim.ConnectivityNode(name=f"{substation.name}_{breaker_number}_j{jcn_num}")
    j_new.uuid(name=f"{substation.name}_{breaker_number}_j{jcn_num}")
    j_new.ConnectivityNodeContainer = substation

    ag = new_disconnector(network, substation,
                          name=f"{substation.name}_{10 * breaker_number}",
                          node1=jcn, node2=j_new)
    ag.BaseVoltage = base_voltage

    branch_terminal.ConnectivityNode = j_new
    network.add_to_graph(j_new)

    return {"disconnector": ag, "junction": j_new}
