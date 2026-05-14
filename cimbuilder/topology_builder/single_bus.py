"""Single-bus substation topology — pure free functions."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.databases import ConnectionInterface
from cimgraph.models import DistributedArea, GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.topology.new_bus_bar_section import new_bus_bar_section
from cimbuilder.utils.base_voltage import get_or_create_base_voltage
from cimbuilder.utils.source_bus import get_source_bus
from cimbuilder.topology_builder._bays import _new_feeder_bay, _new_branch_bay

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_single_bus_substation(
    connection: ConnectionInterface,
    name: str,
    base_voltage: "int | float | cim.BaseVoltage",
    *,
    network: GraphModel | None = None,
) -> dict:
    """Create a single-bus substation: Substation + main bus ConnectivityNode + BusbarSection.

    Args:
        connection:     ConnectionInterface for the new network (used if network is None).
        name:           Substation name.
        base_voltage:   Nominal voltage (V or kV float) or an existing BaseVoltage object.
        network:        Optional existing GraphModel; a new DistributedArea is created if None.

    Returns:
        dict with keys: ``network``, ``substation``, ``main_bus``, ``base_voltage``.
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

    return {
        "network": network,
        "substation": substation,
        "main_bus": main_bus,
        "base_voltage": bv,
    }


def add_feeder_to_single_bus(
    network: GraphModel,
    substation: "cim.Substation",
    main_bus: "cim.ConnectivityNode",
    base_voltage: "cim.BaseVoltage",
    breaker_number: int,
    feeder_network: GraphModel,
    feeder: "cim.Feeder",
    sourcebus: "cim.ConnectivityNode | None" = None,
) -> dict:
    """Add a feeder bay to a single-bus substation.

    Topology: main_bus — ag1 — j1 — brk — j2 — sourcebus

    Args:
        network:        Substation GraphModel.
        substation:     Substation container.
        main_bus:       Main bus ConnectivityNode.
        base_voltage:   BaseVoltage for switching equipment.
        breaker_number: Integer identifier; seeds equipment names.
        feeder_network: GraphModel containing the feeder.
        feeder:         Feeder to connect.
        sourcebus:      Feeder head ConnectivityNode; resolved automatically if None.

    Returns:
        dict with keys: ``breaker``, ``disconnectors`` [ag1, ag2], ``junctions`` [j1, j2].
    """
    if sourcebus is None:
        sourcebus = get_source_bus(feeder_network, feeder)

    prefix = f"{substation.name}_{breaker_number}"
    bay = _new_feeder_bay(network, substation, prefix, main_bus, sourcebus, base_voltage)

    feeder.NormalEnergizingSubstation = substation
    substation.NormalEnergizedFeeder.append(feeder)
    network.add_to_graph(sourcebus)
    network.add_to_graph(feeder)

    return bay


def add_branch_to_single_bus(
    network: GraphModel,
    substation: "cim.Substation",
    main_bus: "cim.ConnectivityNode",
    base_voltage: "cim.BaseVoltage",
    breaker_number: int,
    branch_terminal: "cim.Terminal",
) -> dict:
    """Add a branch bay to a single-bus substation.

    Topology: main_bus — ag1 — j1 — brk — j2, branch_terminal wired to j2.

    Args:
        network:         Substation GraphModel.
        substation:      Substation container.
        main_bus:        Main bus ConnectivityNode.
        base_voltage:    BaseVoltage for switching equipment.
        breaker_number:  Integer identifier; seeds equipment names.
        branch_terminal: Terminal of the branch equipment to wire into the bay.

    Returns:
        dict with keys: ``breaker``, ``disconnector``, ``junctions`` [j1, j2].
    """
    prefix = f"{substation.name}_{breaker_number}"
    return _new_branch_bay(network, substation, prefix, main_bus, branch_terminal, base_voltage)
