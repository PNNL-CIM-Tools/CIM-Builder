"""Build a front-of-meter (utility-scale) PV unit (PowerElectronicsConnection + PhotoVoltaicUnit)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder.object_builder.inverter.new_power_electronics_connection import (
    new_power_electronics_connection,
)
from cimbuilder.object_builder.inverter.new_photo_voltaic_unit import new_photo_voltaic_unit
from cimbuilder.object_builder.measurement.new_analog import new_analog

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_ftm_pv_unit(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    p_kW: float | None = None,
    rated_S_kVA: float | None = None,
    max_p_kW: float | None = None,
    min_q_kVAr: float | None = None,
    max_q_kVAr: float | None = None,
    add_measurements: bool = False,
) -> dict:
    """Create a FTM (utility-scale) PV unit: PowerElectronicsConnection + PhotoVoltaicUnit.

    Front-of-meter PV connects at the substation/feeder head and may specify
    reactive-power capability limits.

    Args:
        network:            Graph model to add to.
        container:          EquipmentContainer.
        name:               Human-readable name; seeds sub-object UUIDs.
        node:               ConnectivityNode (or name string).
        base_voltage:       Optional BaseVoltage.
        p_kW:               Current real-power injection, kW.
        rated_S_kVA:        Inverter nameplate, kVA.
        max_p_kW:           Array nameplate active power, kW.
        min_q_kVAr:         Minimum reactive power, kVAr.
        max_q_kVAr:         Maximum reactive power, kVAr.
        add_measurements:   Create VA Analog on the PEC terminal.

    Returns:
        dict with keys: ``pec``, ``pv_unit``.
    """
    pec = new_power_electronics_connection(
        network, container, name, node,
        base_voltage=base_voltage,
        p_kW=p_kW,
        rated_S_kVA=rated_S_kVA,
        min_q_kVAr=min_q_kVAr,
        max_q_kVAr=max_q_kVAr,
    )

    pv = new_photo_voltaic_unit(
        network, pec, f"{name}_pv",
        min_p_kW=0.0,
        max_p_kW=max_p_kW if max_p_kW is not None else p_kW,
    )

    if add_measurements:
        from cimbuilder._profile import get_cim
        cim = get_cim()
        new_analog(
            network, equipment=pec,
            terminal=pec.Terminals[0],
            phase=cim.PhaseCode.ABC,
            measurementType="VA",
            name=f"{name}_VA",
            check_duplicate=False,
        )

    return {"pec": pec, "pv_unit": pv}
