"""Create a CIM PowerElectronicsConnection (inverter / converter)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.terminal import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_power_electronics_connection(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    p_kW: float | None = None,
    q_kVAr: float | None = None,
    rated_S_kVA: float | None = None,
    rated_U_V: float | None = None,
    min_q_kVAr: float | None = None,
    max_q_kVAr: float | None = None,
    is_grid_forming: bool | None = None,
) -> "cim.PowerElectronicsConnection":
    """Create a PowerElectronicsConnection at ``node``.

    A PowerElectronicsConnection (PEC) is the AC-side terminal of any
    inverter-based resource (PV, BESS, wind, EVSE).  Attach Photovoltaic /
    Battery / Wind units to it via ``PowerElectronicsUnit`` to complete the DER.

    Args:
        network:                Graph model to add to.
        container:              EquipmentContainer.
        name:                   Human-readable name; seeds the UUID.
        node:                   ConnectivityNode (or its name).
        base_voltage:           Optional BaseVoltage; inherits from container if None.
        p_kW:                   Real-power injection at the AC terminal, in kW.
        q_kVAr:                 Reactive-power injection, in kVAr.
        rated_S_kVA:            Inverter nameplate apparent power, in kVA.
        rated_U_V:              Inverter nameplate AC voltage, in V.
        min_q_kVAr, max_q_kVAr: Reactive-power limits, in kVAr.
        is_grid_forming:        Whether the inverter operates in grid-forming
                                mode (vs. grid-following).

    Returns:
        The created ``cim.PowerElectronicsConnection``.
    """
    cim = get_cim()

    pec = cim.PowerElectronicsConnection(name=name)
    pec.uuid(name=name)
    pec.EquipmentContainer = container

    if base_voltage is not None:
        pec.BaseVoltage = base_voltage
    if p_kW is not None:
        pec.p = cim.ActivePower(p_kW, "kW")
    if q_kVAr is not None:
        pec.q = cim.ReactivePower(q_kVAr, "kVAr")
    if rated_S_kVA is not None:
        pec.ratedS = cim.ApparentPower(rated_S_kVA, "kVA")
    if rated_U_V is not None:
        pec.ratedU = cim.Voltage(rated_U_V, "V")
    if min_q_kVAr is not None:
        pec.minQ = cim.ReactivePower(min_q_kVAr, "kVAr")
    if max_q_kVAr is not None:
        pec.maxQ = cim.ReactivePower(max_q_kVAr, "kVAr")
    if is_grid_forming is not None:
        pec.isGridForming = is_grid_forming

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.uuid(name=f"{name}_t1")
    t1.ConductingEquipment = pec
    terminal_to_node(network, t1, node)
    pec.Terminals.append(t1)

    network.add_to_graph(pec)
    network.add_to_graph(t1)

    return pec
