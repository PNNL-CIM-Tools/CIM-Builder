"""Build a feeder head: Breaker + feeder ConnectivityNode + ConnectivityArea + boundary measurements."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch.new_breaker import new_breaker
from cimbuilder.object_builder.measurement.new_analog import new_analog
from cimbuilder.object_builder.measurement.new_discrete import new_discrete

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_feeder_head_breaker(
    network: GraphModel,
    feeder: "cim.Feeder",
    name: str,
    substation_node: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    distributed: bool = True,
    add_measurements: bool = True,
) -> dict:
    """Create a feeder head: Breaker between the substation bus and the feeder.

    Creates:
    - A ``ConnectivityNode`` inside the feeder (``{name}_node``)
    - A ``Breaker`` between ``substation_node`` and the feeder node
    - Sets ``feeder.NormalHeadTerminal`` to terminal 2 of the breaker
    - Optionally wraps the feeder in a ``ConnectivityArea`` for distributed scheduling
    - Optionally adds boundary measurements (Pos discrete + VA/NetLoad analogs)

    Args:
        network:            Graph model to add to.
        feeder:             The Feeder container the breaker belongs to.
        name:               Breaker name; seeds all sub-object UUIDs.
        substation_node:    ConnectivityNode on the substation side.
        base_voltage:       Optional BaseVoltage for the breaker.
        distributed:        Create a ConnectivityArea and bind the boundary terminal.
        add_measurements:   Create Pos, VA, ExcessGen, TotalGen analogs at the
                            boundary terminal.

    Returns:
        dict with keys: ``breaker``, ``feeder_node``, ``feeder_area`` (or None).
    """
    cim = get_cim()

    # feeder-side connectivity node
    feeder_node = cim.ConnectivityNode(name=f"{name}_node")
    feeder_node.uuid(name=f"{name}_node")
    feeder_node.ConnectivityNodeContainer = feeder
    network.add_to_graph(feeder_node)

    breaker = new_breaker(
        network, feeder, name,
        node1=substation_node, node2=feeder_node,
        base_voltage=base_voltage,
    )

    boundary_terminal = breaker.Terminals[1]
    feeder.NormalHeadTerminal = boundary_terminal

    feeder_area = None
    if distributed:
        # cimhub_2026 uses ConnectivityArea (replaces cimhub_2023 FeederArea).
        # ConnectivityArea marks the feeder as a schedulable boundary region;
        # the Feeder's SubSchedulingArea back-ref links them.
        feeder_area = cim.ConnectivityArea(name=f"feeder_area_{feeder.name}")
        feeder_area.uuid(name=f"feeder_area_{feeder.name}")
        feeder.SubSchedulingArea = feeder_area
        network.add_to_graph(feeder_area)

    if add_measurements:
        new_discrete(
            network, equipment=breaker,
            terminal=boundary_terminal,
            phase=cim.PhaseCode.ABC,
            measurementType="Pos",
        )
        new_analog(
            network, equipment=breaker,
            terminal=boundary_terminal,
            phase=cim.PhaseCode.ABC,
            measurementType="VA",
            name=f"NetLoad(MW)_{feeder.name}",
            check_duplicate=False,
        )
        new_analog(
            network, equipment=breaker,
            terminal=boundary_terminal,
            phase=cim.PhaseCode.ABC,
            measurementType="VA",
            name=f"ExcessGeneration(MW)_{feeder.name}",
            check_duplicate=False,
        )
        new_analog(
            network, equipment=breaker,
            terminal=boundary_terminal,
            phase=cim.PhaseCode.ABC,
            measurementType="VA",
            name=f"TotalGeneration(MW)_{feeder.name}",
            check_duplicate=False,
        )

    return {"breaker": breaker, "feeder_node": feeder_node, "feeder_area": feeder_area}
