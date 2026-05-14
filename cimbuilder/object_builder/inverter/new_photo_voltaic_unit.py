"""Create a CIM PhotoVoltaicUnit and attach it to a PowerElectronicsConnection."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_photo_voltaic_unit(
    network: GraphModel,
    pec: "cim.PowerElectronicsConnection",
    name: str,
    *,
    min_p_kW: float | None = None,
    max_p_kW: float | None = None,
) -> "cim.PhotoVoltaicUnit":
    """Create a PhotoVoltaicUnit and attach it to ``pec``.

    A PhotoVoltaicUnit is the DC-side PV array.  It does not have a Terminal
    of its own — power flows through the parent PowerElectronicsConnection.

    Args:
        network:    Graph model to add to.
        pec:        The PowerElectronicsConnection the unit attaches to.
        name:       Human-readable name; seeds the UUID.
        min_p_kW:   Minimum AC-side real power, in kW (typically 0).
        max_p_kW:   Maximum AC-side real power, in kW (the array's nameplate).

    Returns:
        The created ``cim.PhotoVoltaicUnit``.
    """
    cim = get_cim()

    unit = cim.PhotoVoltaicUnit(name=name)
    unit.uuid(name=name)
    unit.PowerElectronicsConnection = pec
    pec.PowerElectronicsUnit.append(unit)

    if min_p_kW is not None:
        unit.minP = cim.ActivePower(min_p_kW, "kW")
    if max_p_kW is not None:
        unit.maxP = cim.ActivePower(max_p_kW, "kW")

    network.add_to_graph(unit)
    return unit
