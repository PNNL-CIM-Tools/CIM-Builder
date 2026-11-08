import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.transformer import (
    PhaseTapChangerAsymmetricalBuilder,
    PhaseTapChangerLinearBuilder,
    PhaseTapChangerSymmetricalBuilder,
    PhaseTapChangerTableBuilder,
    PhaseTapChangerTabularBuilder,
    PowerTransformerBuilder,
)

# Remove once cim18v17 is rebuilt with the PhaseTapChanger subclasses in connectivity_unbalanced
# and steady_state_hypothesis, and their own fields plus PhaseTapChangerTable(Point) in
# electrical_balanced. strict: these XPASS (and fail) as soon as the profile lands.
PROFILE_PENDING = pytest.mark.xfail(
    raises=ValueError,
    strict=True,
    reason="PhaseTapChanger subclasses missing from CN/SSH and their fields from EL_BAL",
)


@pytest.fixture
def end(network, container, base_voltage):
    """End 1 of a 12.47 kV phase-shifting transformer."""
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr = builder.create(mRID="pst1")
    builder.add_connectivity(xfmr)
    _, _, end = builder.add_power_transformer_end(
        xfmr, node="pst_bus", endNumber=1, BaseVoltage=base_voltage.mRID
    )
    return end


def test_add_regulating_control(network, container, end):
    builder = PhaseTapChangerLinearBuilder(network=network, container=container)
    tap_changer = builder.create(mRID="pst1_tap")
    builder.add_regulating_control(
        tap_changer, neutralStep=0, neutralU=Qty(12.47, "kV"), ltcFlag=True
    )
    assert tap_changer.neutralStep == 0
    assert float(tap_changer.neutralU.to("kV")) == pytest.approx(12.47)


@PROFILE_PENDING
@pytest.mark.parametrize(
    "builder_class, electrical, expected",
    [
        (
            PhaseTapChangerLinearBuilder,
            {"stepPhaseShiftIncrement": Qty(1.5, "deg"), "xMax": Qty(10, "ohm")},
            {"stepPhaseShiftIncrement": ("deg", 1.5), "xMax": ("ohm", 10)},
        ),
        (
            PhaseTapChangerSymmetricalBuilder,
            {"voltageStepIncrement": 1.25, "xMax": Qty(10, "ohm")},
            {"voltageStepIncrement": (None, 1.25), "xMax": ("ohm", 10)},
        ),
        (
            PhaseTapChangerAsymmetricalBuilder,
            {"voltageStepIncrement": 1.25, "windingConnectionAngle": Qty(60, "deg")},
            {"voltageStepIncrement": (None, 1.25), "windingConnectionAngle": ("deg", 60)},
        ),
    ],
)
def test_phase_tap_changer(network, container, end, builder_class, electrical, expected):
    builder = builder_class(network=network, container=container)
    tap_changer = builder.create(mRID="pst1_tap")
    builder.add_connectivity(tap_changer, TransformerEnd=end.mRID)
    builder.add_electrical(tap_changer, highStep=32, lowStep=-32, normalStep=0, **electrical)
    builder.add_regulating_control(tap_changer, neutralStep=0, neutralU=Qty(12.47, "kV"))
    builder.add_ssh(tap_changer, step=4)

    assert end.PhaseTapChanger is tap_changer
    assert tap_changer.highStep == 32
    assert tap_changer.step == 4
    for attribute, (unit, value) in expected.items():
        stored = getattr(tap_changer, attribute)
        assert float(stored.to(unit) if unit else stored) == pytest.approx(value)


@PROFILE_PENDING
def test_phase_tap_changer_tabular(network, container, end):
    table_builder = PhaseTapChangerTableBuilder(network=network, container=container)
    table = table_builder.create(mRID="pst_table")
    for step in range(-2, 3):
        table_builder.add_table_point(table, step=step, angle=Qty(5 * step, "deg"), ratio=1.0, x=0.1 * abs(step))

    builder = PhaseTapChangerTabularBuilder(network=network, container=container)
    tap_changer = builder.create(mRID="pst1_tap")
    builder.add_connectivity(tap_changer, TransformerEnd=end.mRID)
    builder.add_electrical(
        tap_changer, highStep=2, lowStep=-2, normalStep=0, PhaseTapChangerTable=table.mRID
    )

    assert tap_changer.PhaseTapChangerTable is table
    assert table.PhaseTapChangerTabular == [tap_changer]
    angles = {point.step: float(point.angle.to("deg")) for point in table.PhaseTapChangerTablePoint}
    assert angles == {-2: -10, -1: -5, 0: 0, 1: 5, 2: 10}
