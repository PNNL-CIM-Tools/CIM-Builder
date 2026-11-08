import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.transformer import (
    PowerTransformerBuilder,
    RatioTapChangerBuilder,
    TapChangerControlBuilder,
)


@pytest.fixture
def ends(network, container, base_voltage):
    """Three single-phase transformers, one end each to put a tap changer on."""
    builder = PowerTransformerBuilder(network=network, container=container)
    ends = []
    for phase in "ABC":
        xfmr = builder.create(mRID=f"xfmr_{phase}")
        builder.add_connectivity(xfmr)
        _, _, end = builder.add_power_transformer_end(
            xfmr, node=f"bus_{phase}", endNumber=1, BaseVoltage=base_voltage.mRID
        )
        ends.append(end)
    return ends


def test_ratio_tap_changer_add_electrical(network, container, ends):
    builder = RatioTapChangerBuilder(network=network, container=container)
    tap_changer = builder.create(mRID="tap_A")
    builder.add_connectivity(tap_changer, TransformerEnd=ends[0].mRID)
    builder.add_electrical(
        tap_changer, highStep=16, lowStep=-16, normalStep=0, stepVoltageIncrement=0.625
    )
    assert tap_changer.highStep == 16
    assert tap_changer.lowStep == -16
    assert float(tap_changer.stepVoltageIncrement) == pytest.approx(0.625)
    assert ends[0].RatioTapChanger is tap_changer


def test_manual_tap_changer_has_no_control(network, container, ends):
    builder = RatioTapChangerBuilder(network=network, container=container)
    tap_changer = builder.create(mRID="tap_A")
    builder.add_regulating_control(
        tap_changer, neutralStep=0, neutralU=Qty(12.47, "kV"), ltcFlag=False, ptPhase="A"
    )
    assert tap_changer.TapChangerControl is None
    assert tap_changer.ptPhase == network.cim.PhaseCode("A")


def test_one_control_for_three_tap_changers(network, container, ends):
    """Three single-phase regulators gang-controlled from one controller."""
    control_builder = TapChangerControlBuilder(network=network, container=container)
    control = control_builder.create(mRID="ctrl")
    control_builder.add_regulating_control(
        control,
        Terminal=ends[0].Terminal.mRID,
        mode="voltage",
        monitoredPhase="A",
        targetValue=7620,
        targetDeadband=127,
    )
    builder = RatioTapChangerBuilder(network=network, container=container)
    tap_changers = []
    for end in ends:
        tap_changer = builder.create(mRID=f"tap_{end.PowerTransformer.mRID}")
        builder.add_connectivity(tap_changer, TransformerEnd=end.mRID)
        builder.add_regulating_control(
            tap_changer, neutralStep=0, neutralU=Qty(7.62, "kV"), TapChangerControl=control.mRID
        )
        tap_changers.append(tap_changer)

    assert control.TapChanger == tap_changers
    assert all(tap_changer.TapChangerControl is control for tap_changer in tap_changers)
