"""Create a CIM PowerTransformerEnd and attach it to a PowerTransformer."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.terminal import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_power_transformer_end(
    network: GraphModel,
    transformer: "cim.PowerTransformer",
    name: str,
    end_number: int,
    node: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    rated_S_MVA: float | None = None,
    rated_U_kV: float | None = None,
    connection_kind: "cim.WindingConnection | None" = None,
    phase_angle_clock: int | None = None,
    r_ohm: float | None = None,
    x_ohm: float | None = None,
    b_S: float | None = None,
    g_S: float | None = None,
    r0_ohm: float | None = None,
    x0_ohm: float | None = None,
    b0_S: float | None = None,
    g0_S: float | None = None,
    grounded: bool | None = None,
) -> "cim.PowerTransformerEnd":
    """Create a PowerTransformerEnd, attach it to ``transformer``, and wire its terminal.

    A PowerTransformerEnd represents one winding.  It owns a Terminal that
    connects to a ConnectivityNode in the network.

    Args:
        network:                Graph model to add to.
        transformer:            Parent PowerTransformer.
        name:                   Human-readable name; seeds the UUID.  Also used
                                to seed the terminal UUID.
        end_number:             1-based winding number (1 = HV, 2 = LV, 3 = TV).
        node:                   ConnectivityNode (or its name) the end's
                                terminal attaches to.
        base_voltage:           Optional BaseVoltage for the winding.
        rated_S_MVA:            Rated apparent power, in MVA.
        rated_U_kV:             Rated line-line voltage, in kV.
        connection_kind:        Winding connection (``cim.WindingConnection``).
        phase_angle_clock:      Phase-angle-clock notation (0-11 hours).
        r_ohm, x_ohm:           Positive-sequence series impedance, in ohms,
                                referred to this winding.
        b_S, g_S:               Positive-sequence shunt admittance, in S,
                                referred to this winding.
        r0_ohm, x0_ohm,
        b0_S, g0_S:             Zero-sequence equivalents.
        grounded:               Whether the winding is grounded.

    Returns:
        The created ``cim.PowerTransformerEnd``.
    """
    cim = get_cim()

    end = cim.PowerTransformerEnd(name=name)
    end.uuid(name=name)
    end.PowerTransformer = transformer
    end.endNumber = int(end_number)
    transformer.PowerTransformerEnd.append(end)

    if base_voltage is not None:
        end.BaseVoltage = base_voltage
    if rated_S_MVA is not None:
        end.ratedS = cim.ApparentPower(rated_S_MVA, "MVA")
    if rated_U_kV is not None:
        end.ratedU = cim.Voltage(rated_U_kV, "kV")
    if connection_kind is not None:
        end.connectionKind = connection_kind
    if phase_angle_clock is not None:
        end.phaseAngleClock = int(phase_angle_clock)
    if r_ohm is not None:
        end.r = cim.Resistance(r_ohm, "ohm")
    if x_ohm is not None:
        end.x = cim.Reactance(x_ohm, "ohm")
    if b_S is not None:
        end.b = cim.Susceptance(b_S, "S")
    if g_S is not None:
        end.g = cim.Conductance(g_S, "S")
    if r0_ohm is not None:
        end.r0 = cim.Resistance(r0_ohm, "ohm")
    if x0_ohm is not None:
        end.x0 = cim.Reactance(x0_ohm, "ohm")
    if b0_S is not None:
        end.b0 = cim.Susceptance(b0_S, "S")
    if g0_S is not None:
        end.g0 = cim.Conductance(g0_S, "S")
    if grounded is not None:
        end.grounded = grounded

    terminal = cim.Terminal(name=f"{transformer.name}_t{end_number}", sequenceNumber=int(end_number))
    terminal.uuid(name=f"{transformer.name}_t{end_number}")
    terminal.ConductingEquipment = transformer
    end.Terminal = terminal
    transformer.Terminals.append(terminal)
    terminal_to_node(network, terminal, node)

    network.add_to_graph(end)
    network.add_to_graph(terminal)

    return end
