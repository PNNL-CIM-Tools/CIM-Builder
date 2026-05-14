"""Create a CIM LoadBreakSwitch (load-rated, non-fault-rated switch)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch._helpers import _build_switch

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_load_break_switch(
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
) -> "cim.LoadBreakSwitch":
    """Create a LoadBreakSwitch between ``node1`` and ``node2``.

    A LoadBreakSwitch can interrupt normal load current but is not rated to
    interrupt fault current.

    Args:
        network:                Graph model to add to.
        container:              EquipmentContainer.
        name:                   Human-readable name; seeds the UUID.
        node1, node2:           Endpoint ConnectivityNodes (or names).
        base_voltage:           Optional BaseVoltage.
        open:                   Current open/closed state.
        normal_open:            Normal open/closed state.
        retained:               Retained in topology reduction.
        breaking_capacity_A:    Max load current the switch can interrupt, in A.

    Returns:
        The created ``cim.LoadBreakSwitch``.
    """
    cim = get_cim()
    switch = _build_switch(
        network, container, name, node1, node2,
        cim.LoadBreakSwitch,
        base_voltage=base_voltage,
        open=open,
        normal_open=normal_open,
        retained=retained,
    )
    if breaking_capacity_A is not None:
        switch.breakingCapacity = cim.CurrentFlow(breaking_capacity_A, "A")
    return switch
