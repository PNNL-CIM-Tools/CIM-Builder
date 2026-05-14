"""Create a CIM RatioTapChanger attached to a TransformerEnd."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_ratio_tap_changer(
    network: GraphModel,
    transformer_end: "cim.TransformerEnd",
    name: str,
    *,
    high_step: int,
    low_step: int,
    neutral_step: int,
    normal_step: int,
    step: float | None = None,
    step_voltage_increment_pct: float | None = None,
    neutral_U_kV: float | None = None,
    initial_delay_s: float | None = None,
    subsequent_delay_s: float | None = None,
    ltc_flag: bool | None = None,
    control: "cim.TapChangerControl | None" = None,
) -> "cim.RatioTapChanger":
    """Create a RatioTapChanger and attach it to ``transformer_end``.

    A RatioTapChanger represents an on-load or off-load tap changer that
    adjusts the turn ratio of a single TransformerEnd.  It must be associated
    with exactly one TransformerEnd; that end's ``RatioTapChanger`` field is
    set automatically.

    Args:
        network:                    Graph model to add to.
        transformer_end:            The TransformerEnd this tap changer
                                    operates on.
        name:                       Human-readable name; seeds the UUID.
        high_step, low_step:        Tap range bounds.
        neutral_step:               Step at which turn ratio = 1.
        normal_step:                Normal operating step.
        step:                       Current step position.  Defaults to
                                    ``normal_step`` if not provided.
        step_voltage_increment_pct: Per-tap voltage increment, as percent of
                                    ``neutral_U_kV``.
        neutral_U_kV:               Voltage at the neutral step, in kV.
        initial_delay_s:            Initial action delay, in seconds.
        subsequent_delay_s:         Subsequent action delay, in seconds.
        ltc_flag:                   Whether the changer can operate under load.
        control:                    Optional TapChangerControl.  When provided,
                                    the controller's ``TapChanger`` list is
                                    updated automatically.

    Returns:
        The created ``cim.RatioTapChanger``.
    """
    cim = get_cim()

    rtc = cim.RatioTapChanger(name=name)
    rtc.uuid(name=name)
    rtc.TransformerEnd = transformer_end
    transformer_end.RatioTapChanger = rtc

    rtc.highStep = int(high_step)
    rtc.lowStep = int(low_step)
    rtc.neutralStep = int(neutral_step)
    rtc.normalStep = int(normal_step)
    rtc.step = float(step) if step is not None else float(normal_step)

    if step_voltage_increment_pct is not None:
        rtc.stepVoltageIncrement = cim.PerCent(step_voltage_increment_pct, "percent")
    if neutral_U_kV is not None:
        rtc.neutralU = cim.Voltage(neutral_U_kV, "kV")
    if initial_delay_s is not None:
        rtc.initialDelay = cim.Seconds(initial_delay_s, "s")
    if subsequent_delay_s is not None:
        rtc.subsequentDelay = cim.Seconds(subsequent_delay_s, "s")
    if ltc_flag is not None:
        rtc.ltcFlag = ltc_flag

    if control is not None:
        rtc.TapChangerControl = control
        control.TapChanger.append(rtc)

    network.add_to_graph(rtc)
    return rtc
