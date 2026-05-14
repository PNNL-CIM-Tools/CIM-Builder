"""Create a CIM Fuse (overcurrent protective device)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.switch._helpers import _build_switch

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_fuse(
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
    rated_current_A: float | None = None,
) -> "cim.Fuse":
    """Create a Fuse between ``node1`` and ``node2``.

    A Fuse is an overcurrent protective device with a fusible part severed by
    overcurrent.  It is modelled as a Switch because it breaks current.

    Args:
        network:            Graph model to add to.
        container:          EquipmentContainer.
        name:               Human-readable name; seeds the UUID.
        node1, node2:       Endpoint ConnectivityNodes (or names).
        base_voltage:       Optional BaseVoltage.
        open:               Current open/closed state.  ``True`` if blown.
        normal_open:        Normal open/closed state.
        retained:           Retained in topology reduction.
        rated_current_A:    Continuous current rating, in amperes.

    Returns:
        The created ``cim.Fuse``.
    """
    cim = get_cim()
    fuse = _build_switch(
        network, container, name, node1, node2,
        cim.Fuse,
        base_voltage=base_voltage,
        open=open,
        normal_open=normal_open,
        retained=retained,
    )
    if rated_current_A is not None:
        fuse.ratedCurrent = cim.CurrentFlow(rated_current_A, "A")
    return fuse
