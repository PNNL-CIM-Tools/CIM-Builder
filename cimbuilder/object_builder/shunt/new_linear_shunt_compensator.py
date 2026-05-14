"""Create a CIM LinearShuntCompensator (shunt capacitor or reactor)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.terminal import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_linear_shunt_compensator(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    b_per_section: float | None = None,
    g_per_section: float | None = None,
    b0_per_section: float | None = None,
    g0_per_section: float | None = None,
    nominal_voltage_kV: float | None = None,
    sections: int = 1,
    maximum_sections: int = 1,
    normal_sections: int | None = None,
    grounded: bool = False,
) -> "cim.LinearShuntCompensator":
    """Create a LinearShuntCompensator at ``node`` and add it to ``network``.

    A LinearShuntCompensator is a shunt-connected bank of identical sections
    used as a capacitor (positive ``b_per_section``) or reactor (negative
    ``b_per_section``).  This primitive takes admittances directly in SI units
    (siemens).  Higher-level builders accept Mvar/MW and convert via
    ``Q = V^2 * b``.

    Args:
        network:            Graph model to add to.
        container:          EquipmentContainer.
        name:               Human-readable name; seeds the UUID.
        node:               ConnectivityNode (or its name).
        base_voltage:       Optional BaseVoltage; inherits from container if None.
        b_per_section:      Positive-sequence susceptance per section, in S.
        g_per_section:      Positive-sequence conductance per section, in S.
        b0_per_section:     Zero-sequence susceptance per section, in S.
        g0_per_section:     Zero-sequence conductance per section, in S.
        nominal_voltage_kV: Nominal line-to-line voltage at which susceptance is
                            specified, in kV.  Optional.
        sections:           Currently energized sections.
        maximum_sections:   Maximum number of sections.
        normal_sections:    Normally energized sections; defaults to ``sections``.
        grounded:           Whether the bank's neutral point is grounded.

    Returns:
        The created ``cim.LinearShuntCompensator``.
    """
    cim = get_cim()

    obj = cim.LinearShuntCompensator(name=name)
    obj.uuid(name=name)
    obj.EquipmentContainer = container

    if base_voltage is not None:
        obj.BaseVoltage = base_voltage
    if b_per_section is not None:
        obj.bPerSection = cim.Susceptance(b_per_section, "S")
    if g_per_section is not None:
        obj.gPerSection = cim.Conductance(g_per_section, "S")
    if b0_per_section is not None:
        obj.b0PerSection = cim.Susceptance(b0_per_section, "S")
    if g0_per_section is not None:
        obj.g0PerSection = cim.Conductance(g0_per_section, "S")
    if nominal_voltage_kV is not None:
        obj.nomU = cim.Voltage(nominal_voltage_kV, "kV")

    obj.sections = float(sections)
    obj.maximumSections = int(maximum_sections)
    obj.normalSections = int(normal_sections) if normal_sections is not None else int(sections)
    obj.grounded = grounded

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.uuid(name=f"{name}_t1")
    t1.ConductingEquipment = obj
    terminal_to_node(network, t1, node)
    obj.Terminals.append(t1)

    network.add_to_graph(obj)
    network.add_to_graph(t1)

    return obj
