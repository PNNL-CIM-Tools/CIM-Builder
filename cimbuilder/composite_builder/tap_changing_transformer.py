"""Build a complete tap-changing transformer (PowerTransformer + ends + RatioTapChanger)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder.object_builder.transformer.new_power_transformer import new_power_transformer
from cimbuilder.object_builder.transformer.new_power_transformer_end import new_power_transformer_end
from cimbuilder.object_builder.transformer.new_ratio_tap_changer import new_ratio_tap_changer
from cimbuilder.object_builder.transformer.new_tap_changer_control import new_tap_changer_control

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_tap_changing_transformer(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node1: "str | cim.ConnectivityNode",
    node2: "str | cim.ConnectivityNode",
    *,
    # HV winding (end 1)
    rated_U1_kV: float | None = None,
    rated_S_MVA: float | None = None,
    connection_kind1: "cim.WindingConnection | None" = None,
    r_ohm: float | None = None,
    x_ohm: float | None = None,
    # LV winding (end 2)
    rated_U2_kV: float | None = None,
    connection_kind2: "cim.WindingConnection | None" = None,
    # tap changer (attached to end 1 by default)
    high_step: int = 16,
    low_step: int = -16,
    neutral_step: int = 0,
    normal_step: int = 0,
    step: float | None = None,
    step_voltage_increment_pct: float | None = None,
    neutral_U_kV: float | None = None,
    ltc_flag: bool | None = None,
    # regulating control
    add_control: bool = True,
    target_value_kV: float | None = None,
    target_deadband_kV: float | None = None,
    # optional template (Phase 6 TODO — not yet consumed)
    template: "cim.PowerTransformerInfo | None" = None,
) -> dict:
    """Create a two-winding tap-changing transformer.

    Builds a PowerTransformer + two PowerTransformerEnds + a RatioTapChanger on
    end 1 + an optional TapChangerControl.

    Args:
        network:                    Graph model to add to.
        container:                  EquipmentContainer (Substation, VoltageLevel, etc.).
        name:                       Human-readable name; seeds all sub-object UUIDs.
        node1:                      HV ConnectivityNode (or name string).
        node2:                      LV ConnectivityNode (or name string).
        rated_U1_kV:                HV rated voltage, kV.
        rated_S_MVA:                Rated apparent power, MVA (applied to end 1).
        connection_kind1:           HV winding connection.
        r_ohm, x_ohm:              Positive-sequence series impedance, ohms, HV-referred.
        rated_U2_kV:                LV rated voltage, kV.
        connection_kind2:           LV winding connection.
        high_step, low_step:        Tap range bounds.
        neutral_step:               Step at which ratio = 1.
        normal_step:                Normal operating step.
        step:                       Current step (defaults to normal_step).
        step_voltage_increment_pct: Per-tap voltage increment, %.
        neutral_U_kV:               Voltage at neutral step, kV.
        ltc_flag:                   Whether load-tap-changing is enabled.
        add_control:                Create a TapChangerControl (default True).
        target_value_kV:            Control setpoint, kV.
        target_deadband_kV:         Control dead-band, kV.
        template:                   PowerTransformerInfo — accepted but not yet
                                    consumed (Phase 6 will plumb nameplate data).

    Returns:
        dict with keys: ``transformer``, ``end1``, ``end2``, ``tap_changer``,
        ``control`` (None if add_control=False).
    """
    if template is not None:
        _log.info(
            "tap_changing_transformer %r: template not yet consumed (Phase 6).", name
        )

    xfmr = new_power_transformer(network, container, name)

    end1 = new_power_transformer_end(
        network, xfmr, f"{name}_end1", 1, node1,
        rated_S_MVA=rated_S_MVA,
        rated_U_kV=rated_U1_kV,
        connection_kind=connection_kind1,
        r_ohm=r_ohm,
        x_ohm=x_ohm,
    )

    end2 = new_power_transformer_end(
        network, xfmr, f"{name}_end2", 2, node2,
        rated_U_kV=rated_U2_kV,
        connection_kind=connection_kind2,
    )

    control = None
    if add_control:
        control = new_tap_changer_control(
            network, f"{name}_ctrl",
            target_value_kV=target_value_kV,
            target_deadband_kV=target_deadband_kV,
        )

    rtc = new_ratio_tap_changer(
        network, end1, f"{name}_rtc",
        high_step=high_step,
        low_step=low_step,
        neutral_step=neutral_step,
        normal_step=normal_step,
        step=step,
        step_voltage_increment_pct=step_voltage_increment_pct,
        neutral_U_kV=neutral_U_kV,
        ltc_flag=ltc_flag,
        control=control,
    )

    return {
        "transformer": xfmr,
        "end1": end1,
        "end2": end2,
        "tap_changer": rtc,
        "control": control,
    }
