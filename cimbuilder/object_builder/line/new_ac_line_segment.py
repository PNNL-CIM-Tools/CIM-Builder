"""Create a CIM ACLineSegment between two ConnectivityNodes."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.terminal import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_ac_line_segment(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node1: "str | cim.ConnectivityNode",
    node2: "str | cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    length_km: float | None = None,
    r_ohm: float | None = None,
    x_ohm: float | None = None,
    bch_S: float | None = None,
    gch_S: float | None = None,
    r0_ohm: float | None = None,
    x0_ohm: float | None = None,
    b0ch_S: float | None = None,
    g0ch_S: float | None = None,
    per_length_impedance: "cim.PerLengthImpedance | None" = None,
    is_underground: bool | None = None,
    template: "cim.OverheadWireInfo | cim.WireInfo | None" = None,
) -> "cim.ACLineSegment":
    """Create an ACLineSegment between ``node1`` and ``node2``.

    Impedance can be specified three ways, in order of precedence:

    1. ``per_length_impedance`` — reference to a shared
       ``PerLengthSequenceImpedance``.  Total impedance is computed from
       ``per_length × length_km``.
    2. ``r_ohm``, ``x_ohm``, ... — total impedance/admittance, set directly.
    3. ``template`` — TODO: Phase 6 will pull per-length impedance from a
       cim_asset_catalog ``OverheadWireInfo`` Parquet row.  Until then this
       parameter is accepted but does not currently populate any fields.

    Args:
        network:                Graph model to add to.
        container:              EquipmentContainer (typically a Feeder or Line).
        name:                   Human-readable name; seeds the UUID.
        node1, node2:           Endpoint ConnectivityNodes (or names).
        base_voltage:           Optional BaseVoltage; inherits from container.
        length_km:              Conductor length, in km.
        r_ohm, x_ohm:           Positive-sequence series impedance, in ohms.
        bch_S, gch_S:           Positive-sequence shunt admittance, in S.
        r0_ohm, x0_ohm:         Zero-sequence series impedance, in ohms.
        b0ch_S, g0ch_S:         Zero-sequence shunt admittance, in S.
        per_length_impedance:   Optional shared PerLengthImpedance.
        is_underground:         Whether the segment is undergrounded.
        template:               Optional cimhub_2026 ``WireInfo`` (typically
                                ``OverheadWireInfo``) to source per-length
                                impedance from.  Phase 6 wiring; currently a
                                no-op stub.

    Returns:
        The created ``cim.ACLineSegment``.
    """
    cim = get_cim()

    # TODO(Phase 6): pull per-length impedance from `template` once
    # cim-asset-catalog is wired up.  Today we accept the kwarg for forward
    # compatibility but do not consume it.
    if template is not None:
        _log.info(
            "ACLineSegment %r: template arg accepted but not yet consumed "
            "(Phase 6 will load impedance from cim-asset-catalog).",
            name,
        )

    line = cim.ACLineSegment(name=name)
    line.uuid(name=name)
    line.EquipmentContainer = container

    if base_voltage is not None:
        line.BaseVoltage = base_voltage
    if length_km is not None:
        line.length = cim.Length(length_km, "km")
    if is_underground is not None:
        line.isUnderground = is_underground

    if per_length_impedance is not None:
        line.PerLengthImpedance = per_length_impedance
    if r_ohm is not None:
        line.r = cim.Resistance(r_ohm, "ohm")
    if x_ohm is not None:
        line.x = cim.Reactance(x_ohm, "ohm")
    if bch_S is not None:
        line.bch = cim.Susceptance(bch_S, "S")
    if gch_S is not None:
        line.gch = cim.Conductance(gch_S, "S")
    if r0_ohm is not None:
        line.r0 = cim.Resistance(r0_ohm, "ohm")
    if x0_ohm is not None:
        line.x0 = cim.Reactance(x0_ohm, "ohm")
    if b0ch_S is not None:
        line.b0ch = cim.Susceptance(b0ch_S, "S")
    if g0ch_S is not None:
        line.g0ch = cim.Conductance(g0ch_S, "S")

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.uuid(name=f"{name}_t1")
    t1.ConductingEquipment = line
    terminal_to_node(network, t1, node1)
    line.Terminals.append(t1)

    t2 = cim.Terminal(name=f"{name}_t2", sequenceNumber=2)
    t2.uuid(name=f"{name}_t2")
    t2.ConductingEquipment = line
    terminal_to_node(network, t2, node2)
    line.Terminals.append(t2)

    network.add_to_graph(line)
    network.add_to_graph(t1)
    network.add_to_graph(t2)

    return line
