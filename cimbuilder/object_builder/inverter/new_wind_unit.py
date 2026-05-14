"""Create a CIM PowerElectronicsWindUnit and attach to a PowerElectronicsConnection."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_wind_unit(
    network: GraphModel,
    pec: "cim.PowerElectronicsConnection",
    name: str,
    *,
    min_p_kW: float | None = None,
    max_p_kW: float | None = None,
) -> "cim.PowerElectronicsWindUnit":
    """Create a PowerElectronicsWindUnit and attach it to ``pec``.

    Used for type 4 (full-converter) wind generators.  Type 1-3 doubly-fed
    induction generators are modeled with a SynchronousMachine instead.

    Args:
        network:                Graph model to add to.
        pec:                    Parent PowerElectronicsConnection.
        name:                   Human-readable name; seeds the UUID.
        min_p_kW, max_p_kW:     AC-side real-power range, in kW.

    Returns:
        The created ``cim.PowerElectronicsWindUnit``.
    """
    cim = get_cim()

    unit = cim.PowerElectronicsWindUnit(name=name)
    unit.uuid(name=name)
    unit.PowerElectronicsConnection = pec
    pec.PowerElectronicsUnit.append(unit)

    if min_p_kW is not None:
        unit.minP = cim.ActivePower(min_p_kW, "kW")
    if max_p_kW is not None:
        unit.maxP = cim.ActivePower(max_p_kW, "kW")

    network.add_to_graph(unit)
    return unit
