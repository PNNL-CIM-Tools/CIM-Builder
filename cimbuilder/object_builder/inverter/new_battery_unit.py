"""Create a CIM BatteryUnit and attach it to a PowerElectronicsConnection."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_battery_unit(
    network: GraphModel,
    pec: "cim.PowerElectronicsConnection",
    name: str,
    *,
    min_p_kW: float | None = None,
    max_p_kW: float | None = None,
    rated_E_kWh: float | None = None,
    stored_E_kWh: float | None = None,
    minimum_E_kWh: float | None = None,
    charging_efficiency_pct: float | None = None,
    discharging_efficiency_pct: float | None = None,
) -> "cim.BatteryUnit":
    """Create a BatteryUnit and attach it to ``pec``.

    Args:
        network:                    Graph model to add to.
        pec:                        Parent PowerElectronicsConnection.
        name:                       Human-readable name; seeds the UUID.
        min_p_kW, max_p_kW:         AC-side real-power range, in kW.  ``min_p_kW``
                                    is negative for charging.
        rated_E_kWh:                Battery's nameplate energy capacity, in kWh.
        stored_E_kWh:               Currently stored energy, in kWh.
        minimum_E_kWh:              Minimum allowed stored energy (cycling
                                    floor), in kWh.
        charging_efficiency_pct:    Charging efficiency, 0-100.
        discharging_efficiency_pct: Discharging efficiency, 0-100.

    Returns:
        The created ``cim.BatteryUnit``.
    """
    cim = get_cim()

    unit = cim.BatteryUnit(name=name)
    unit.uuid(name=name)
    unit.PowerElectronicsConnection = pec
    pec.PowerElectronicsUnit.append(unit)

    if min_p_kW is not None:
        unit.minP = cim.ActivePower(min_p_kW, "kW")
    if max_p_kW is not None:
        unit.maxP = cim.ActivePower(max_p_kW, "kW")
    if rated_E_kWh is not None:
        unit.ratedE = cim.RealEnergy(rated_E_kWh, "kWh")
    if stored_E_kWh is not None:
        unit.storedE = cim.RealEnergy(stored_E_kWh, "kWh")
    if minimum_E_kWh is not None:
        unit.minimumE = cim.RealEnergy(minimum_E_kWh, "kWh")
    if charging_efficiency_pct is not None:
        unit.chargingEfficiency = cim.PerCent(charging_efficiency_pct, "percent")
    if discharging_efficiency_pct is not None:
        unit.dischargingEfficiency = cim.PerCent(discharging_efficiency_pct, "percent")

    network.add_to_graph(unit)
    return unit
