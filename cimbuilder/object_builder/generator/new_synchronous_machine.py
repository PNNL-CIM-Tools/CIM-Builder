"""Create a CIM SynchronousMachine (synchronous generator/condenser/motor)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.terminal import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_synchronous_machine(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    p_MW: float | None = None,
    q_MVAr: float | None = None,
    rated_S_MVA: float | None = None,
    rated_U_kV: float | None = None,
    rated_power_factor: float | None = None,
    min_q_MVAr: float | None = None,
    max_q_MVAr: float | None = None,
) -> "cim.SynchronousMachine":
    """Create a SynchronousMachine at ``node``.

    SynchronousMachine covers both generators and synchronous condensers.
    Per CIM convention, terminal-positive ``p`` means power flowing INTO the
    equipment, so a generator delivering 50 MW to the bus is modeled with
    ``p_MW = -50`` if you want CIM Terminal sign convention; this primitive
    stores the value you pass directly into the machine's ``p`` attribute and
    leaves the sign convention to the caller.

    Args:
        network:                Graph model to add to.
        container:              EquipmentContainer.
        name:                   Human-readable name; seeds the UUID.
        node:                   ConnectivityNode (or its name).
        base_voltage:           Optional BaseVoltage; inherits from container.
        p_MW:                   Active power, in MW.
        q_MVAr:                 Reactive power, in MVAr.
        rated_S_MVA:            Nameplate apparent power, in MVA.
        rated_U_kV:             Nameplate voltage, in kV.
        rated_power_factor:     Nameplate power factor (0.0-1.0, dimensionless).
        min_q_MVAr:             Lower reactive-power limit, in MVAr.
        max_q_MVAr:             Upper reactive-power limit, in MVAr.

    Returns:
        The created ``cim.SynchronousMachine``.
    """
    cim = get_cim()

    machine = cim.SynchronousMachine(name=name)
    machine.uuid(name=name)
    machine.EquipmentContainer = container

    if base_voltage is not None:
        machine.BaseVoltage = base_voltage
    if p_MW is not None:
        machine.p = cim.ActivePower(p_MW, "MW")
    if q_MVAr is not None:
        machine.q = cim.ReactivePower(q_MVAr, "MVAr")
    if rated_S_MVA is not None:
        machine.ratedS = cim.ApparentPower(rated_S_MVA, "MVA")
    if rated_U_kV is not None:
        machine.ratedU = cim.Voltage(rated_U_kV, "kV")
    if rated_power_factor is not None:
        machine.ratedPowerFactor = float(rated_power_factor)
    if min_q_MVAr is not None:
        machine.minQ = cim.ReactivePower(min_q_MVAr, "MVAr")
    if max_q_MVAr is not None:
        machine.maxQ = cim.ReactivePower(max_q_MVAr, "MVAr")

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.uuid(name=f"{name}_t1")
    t1.ConductingEquipment = machine
    terminal_to_node(network, t1, node)
    machine.Terminals.append(t1)

    network.add_to_graph(machine)
    network.add_to_graph(t1)

    return machine
