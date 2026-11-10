def tap_steps_from_boost_buck(
    number_of_taps: int, max_boost_pct: float, max_buck_pct: float
) -> tuple[int, int, float]:
    """
    Converts a regulator's total tap count and +-range (CYME NumberOfTaps, MaximumBoost,
    MaximumBuck; GDM total_taps, max_tap_pu, min_tap_pu converted to percent) into
    TapChangerInfo's highStep/lowStep/stepVoltageIncrement.

    Splits the taps evenly across boost and buck: 32 taps at +-10% -> (16, -16, 0.625).
    Returns (highStep, lowStep, stepVoltageIncrement).
    """
    if number_of_taps % 2 != 0:
        raise ValueError(f"number_of_taps must be even (split across boost and buck), got {number_of_taps}")
    half_taps = number_of_taps // 2
    high_step = half_taps
    low_step = -half_taps
    step_voltage_increment = max_boost_pct / half_taps
    if step_voltage_increment != max_buck_pct / half_taps:
        raise ValueError(
            f"boost {max_boost_pct}% and buck {max_buck_pct}% give different step sizes over "
            f"{half_taps} steps each - this regulator is not symmetrical, pass highStep/lowStep/"
            f"stepVoltageIncrement to TapChangerInfoBuilder directly instead"
        )
    return high_step, low_step, step_voltage_increment
