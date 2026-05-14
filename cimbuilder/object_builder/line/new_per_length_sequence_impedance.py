"""Create a CIM PerLengthSequenceImpedance for AC line segments."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_per_length_sequence_impedance(
    network: GraphModel,
    name: str,
    *,
    r_ohm_per_km: float | None = None,
    x_ohm_per_km: float | None = None,
    bch_S_per_km: float | None = None,
    gch_S_per_km: float | None = None,
    r0_ohm_per_km: float | None = None,
    x0_ohm_per_km: float | None = None,
    b0ch_S_per_km: float | None = None,
    g0ch_S_per_km: float | None = None,
) -> "cim.PerLengthSequenceImpedance":
    """Create a PerLengthSequenceImpedance and add it to ``network``.

    A PerLengthSequenceImpedance carries the positive- and zero-sequence
    impedance and shunt admittance of an AC line, on a per-length basis.  Many
    ACLineSegments may reference the same PerLengthSequenceImpedance.

    Args:
        network:        Graph model to add to.
        name:           Human-readable name; seeds the UUID.
        r_ohm_per_km:   Positive-sequence resistance, in ohm/km.
        x_ohm_per_km:   Positive-sequence reactance, in ohm/km.
        bch_S_per_km:   Positive-sequence shunt charging susceptance, in S/km.
        gch_S_per_km:   Positive-sequence shunt conductance, in S/km.
        r0_ohm_per_km:  Zero-sequence resistance, in ohm/km.
        x0_ohm_per_km:  Zero-sequence reactance, in ohm/km.
        b0ch_S_per_km:  Zero-sequence shunt charging susceptance, in S/km.
        g0ch_S_per_km:  Zero-sequence shunt conductance, in S/km.

    Returns:
        The created ``cim.PerLengthSequenceImpedance``.
    """
    cim = get_cim()

    impedance = cim.PerLengthSequenceImpedance(name=name)
    impedance.uuid(name=name)

    if r_ohm_per_km is not None:
        impedance.r = cim.ResistancePerLength(r_ohm_per_km, "ohm/km")
    if x_ohm_per_km is not None:
        impedance.x = cim.ReactancePerLength(x_ohm_per_km, "ohm/km")
    if bch_S_per_km is not None:
        impedance.bch = cim.SusceptancePerLength(bch_S_per_km, "S/km")
    if gch_S_per_km is not None:
        impedance.gch = cim.ConductancePerLength(gch_S_per_km, "S/km")
    if r0_ohm_per_km is not None:
        impedance.r0 = cim.ResistancePerLength(r0_ohm_per_km, "ohm/km")
    if x0_ohm_per_km is not None:
        impedance.x0 = cim.ReactancePerLength(x0_ohm_per_km, "ohm/km")
    if b0ch_S_per_km is not None:
        impedance.b0ch = cim.SusceptancePerLength(b0ch_S_per_km, "S/km")
    if g0ch_S_per_km is not None:
        impedance.g0ch = cim.ConductancePerLength(g0ch_S_per_km, "S/km")

    network.add_to_graph(impedance)
    return impedance
