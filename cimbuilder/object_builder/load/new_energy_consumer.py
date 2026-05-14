"""Create a CIM EnergyConsumer (load)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.terminal import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_energy_consumer(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    p_kW: float | None = None,
    q_kVAr: float | None = None,
    pfixed_kW: float | None = None,
    qfixed_kVAr: float | None = None,
    customer_count: int | None = None,
    grounded: bool = False,
) -> "cim.EnergyConsumer":
    """Create an EnergyConsumer at ``node``.

    EnergyConsumer is the CIM class for any electrical load — single load,
    aggregate load, or zonal load model.

    Args:
        network:        Graph model to add to.
        container:      EquipmentContainer (typically a Feeder).
        name:           Human-readable name; seeds the UUID.
        node:           ConnectivityNode (or its name).
        base_voltage:   Optional BaseVoltage; inherits from container if None.
        p_kW:           Active power demand at nominal voltage, in kW.
        q_kVAr:         Reactive power demand at nominal voltage, in kVAr.
        pfixed_kW:      Active-power constant-power component, in kW.
        qfixed_kVAr:    Reactive-power constant-power component, in kVAr.
        customer_count: Number of individual customers represented by this load.
        grounded:       Whether the load's neutral is grounded.

    Returns:
        The created ``cim.EnergyConsumer``.
    """
    cim = get_cim()

    load = cim.EnergyConsumer(name=name)
    load.uuid(name=name)
    load.EquipmentContainer = container

    if base_voltage is not None:
        load.BaseVoltage = base_voltage
    if p_kW is not None:
        load.p = cim.ActivePower(p_kW, "kW")
    if q_kVAr is not None:
        load.q = cim.ReactivePower(q_kVAr, "kVAr")
    if pfixed_kW is not None:
        load.pfixed = cim.ActivePower(pfixed_kW, "kW")
    if qfixed_kVAr is not None:
        load.qfixed = cim.ReactivePower(qfixed_kVAr, "kVAr")
    if customer_count is not None:
        load.customerCount = int(customer_count)
    load.grounded = grounded

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.uuid(name=f"{name}_t1")
    t1.ConductingEquipment = load
    terminal_to_node(network, t1, node)
    load.Terminals.append(t1)

    network.add_to_graph(load)
    network.add_to_graph(t1)

    return load
