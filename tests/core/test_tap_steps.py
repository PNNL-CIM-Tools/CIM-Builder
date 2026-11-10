import pytest

from cimbuilder.core.tap_steps import tap_steps_from_boost_buck


def test_32_taps_10_percent():
    """B17's worked example: 32 taps, +-10% -> +-16, 0.625%"""
    high_step, low_step, step_voltage_increment = tap_steps_from_boost_buck(32, 10, 10)
    assert high_step == 16
    assert low_step == -16
    assert step_voltage_increment == pytest.approx(0.625)


def test_odd_tap_count_rejected():
    with pytest.raises(ValueError, match="even"):
        tap_steps_from_boost_buck(33, 10, 10)


def test_asymmetric_boost_buck_rejected():
    with pytest.raises(ValueError, match="not symmetrical"):
        tap_steps_from_boost_buck(32, 10, 7.5)
