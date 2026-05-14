"""Create a CIM TapChangerControl (a RegulatingControl for tap changers)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_tap_changer_control(
    network: GraphModel,
    name: str,
    *,
    terminal: "cim.Terminal | None" = None,
    target_value_kV: float | None = None,
    target_deadband_kV: float | None = None,
    target_value_unit_multiplier: str | None = None,
    enabled: bool | None = None,
    discrete: bool | None = None,
    mode: "cim.RegulatingControlModeKind | None" = None,
    monitored_phase: "cim.PhaseCode | None" = None,
) -> "cim.TapChangerControl":
    """Create a TapChangerControl and add it to ``network``.

    A TapChangerControl is a RegulatingControl that governs one or more
    RatioTapChangers.  After creation, attach tap changers via
    ``new_ratio_tap_changer(..., control=tcc)``.

    Args:
        network:                        Graph model to add to.
        name:                           Human-readable name; seeds the UUID.
        terminal:                       Measuring terminal for the regulation.
        target_value_kV:                Regulation setpoint, in kV.
        target_deadband_kV:             Dead-band half-width, in kV.
        target_value_unit_multiplier:   SI prefix string (e.g. ``'k'``).
        enabled:                        Whether the regulator is active.
        discrete:                       True if discrete (step) control.
        mode:                           ``cim.RegulatingControlModeKind``.
        monitored_phase:                ``cim.PhaseCode`` being monitored.

    Returns:
        The created ``cim.TapChangerControl``.
    """
    cim = get_cim()

    tcc = cim.TapChangerControl(name=name)
    tcc.uuid(name=name)

    if terminal is not None:
        tcc.Terminal = terminal
    if target_value_kV is not None:
        tcc.targetValue = cim.Voltage(target_value_kV, "kV")
    if target_deadband_kV is not None:
        tcc.targetDeadband = cim.Voltage(target_deadband_kV, "kV")
    if target_value_unit_multiplier is not None:
        tcc.targetValueUnitMultiplier = target_value_unit_multiplier
    if enabled is not None:
        tcc.enabled = enabled
    if discrete is not None:
        tcc.discrete = discrete
    if mode is not None:
        tcc.mode = mode
    if monitored_phase is not None:
        tcc.monitoredPhase = monitored_phase

    network.add_to_graph(tcc)
    return tcc
