"""Build a battery energy storage system (PowerElectronicsConnection + BatteryUnit)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder.object_builder.inverter.new_power_electronics_connection import (
    new_power_electronics_connection,
)
from cimbuilder.object_builder.inverter.new_battery_unit import new_battery_unit as _new_battery_unit
from cimbuilder.object_builder.measurement.new_analog import new_analog

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_battery_unit(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    p_kW: float | None = None,
    q_kVAr: float | None = None,
    rated_S_kVA: float | None = None,
    rated_E_kWh: float | None = None,
    stored_E_kWh: float | None = None,
    max_p_kW: float | None = None,
    min_p_kW: float | None = None,
    min_q_kVAr: float | None = None,
    max_q_kVAr: float | None = None,
    charging_efficiency_pct: float | None = None,
    discharging_efficiency_pct: float | None = None,
    add_measurements: bool = False,
) -> dict:
    """Create a BESS: PowerElectronicsConnection + BatteryUnit.

    Args:
        network:                    Graph model to add to.
        container:                  EquipmentContainer.
        name:                       Human-readable name; seeds sub-object UUIDs.
        node:                       ConnectivityNode (or name string).
        base_voltage:               Optional BaseVoltage.
        p_kW:                       Current real-power injection (+ = discharge), kW.
        q_kVAr:                     Reactive-power injection, kVAr.
        rated_S_kVA:                Inverter nameplate, kVA.
        rated_E_kWh:                Usable energy capacity, kWh.
        stored_E_kWh:               Current state-of-charge energy, kWh.
        max_p_kW, min_p_kW:         Real-power capability limits, kW.
        min_q_kVAr, max_q_kVAr:    Reactive-power limits, kVAr.
        charging_efficiency_pct:    Round-trip charging efficiency, %.
        discharging_efficiency_pct: Discharging efficiency, %.
        add_measurements:           Create VA + SoC Analogs on the PEC terminal.

    Returns:
        dict with keys: ``pec``, ``battery``.
    """
    pec = new_power_electronics_connection(
        network, container, name, node,
        base_voltage=base_voltage,
        p_kW=p_kW,
        q_kVAr=q_kVAr,
        rated_S_kVA=rated_S_kVA,
        min_q_kVAr=min_q_kVAr,
        max_q_kVAr=max_q_kVAr,
    )

    battery = _new_battery_unit(
        network, pec, f"{name}_bess",
        rated_E_kWh=rated_E_kWh,
        stored_E_kWh=stored_E_kWh,
        max_p_kW=max_p_kW,
        min_p_kW=min_p_kW,
        charging_efficiency_pct=charging_efficiency_pct,
        discharging_efficiency_pct=discharging_efficiency_pct,
    )

    if add_measurements:
        from cimbuilder._profile import get_cim
        cim = get_cim()
        terminal = pec.Terminals[0]
        new_analog(
            network, equipment=pec, terminal=terminal,
            phase=cim.PhaseCode.ABC, measurementType="VA",
            name=f"{name}_VA", check_duplicate=False,
        )
        new_analog(
            network, equipment=pec, terminal=terminal,
            phase=cim.PhaseCode.none, measurementType="SoC",
            name=f"{name}_SoC", check_duplicate=False,
        )

    return {"pec": pec, "battery": battery}
