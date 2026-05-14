"""Create a CIM Breaker (mechanical short-circuit-rated switch)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch._helpers import _build_switch

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_breaker(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node1: "str | cim.ConnectivityNode",
    node2: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    open: bool = False,
    normal_open: bool = False,
    retained: bool = True,
    breaking_capacity_A: float | None = None,
) -> "cim.Breaker":
    """Create a Breaker between ``node1`` and ``node2`` and add it to ``network``.

    A Breaker is a mechanical switching device capable of making, carrying,
    and breaking currents under normal and short-circuit conditions.

    Args:
        network:                Graph model to add the breaker to.
        container:              EquipmentContainer the breaker belongs to.
        name:                   Human-readable name; also seeds the UUID.
        node1:                  First ConnectivityNode (or its name).
        node2:                  Second ConnectivityNode (or its name).
        base_voltage:           Optional BaseVoltage; inherits from container if None.
        open:                   Current open/closed state. ``True`` = open.
        normal_open:            Normal (study-case) open/closed state.
        retained:               Whether the breaker is retained in topology
                                reduction. ``True`` for typical switching.
        breaking_capacity_A:    Maximum fault current the breaker can interrupt,
                                in amperes. Stored as ``cim.CurrentFlow``.

    Returns:
        The created ``cim.Breaker``.
    """
    cim = get_cim()
    breaker = _build_switch(
        network, container, name, node1, node2,
        cim.Breaker,
        base_voltage=base_voltage,
        open=open,
        normal_open=normal_open,
        retained=retained,
    )
    if breaking_capacity_A is not None:
        breaker.breakingCapacity = cim.CurrentFlow(breaking_capacity_A, "A")
    return breaker
