from cimtables.units import Qty

from cimbuilder.object_builder.transformer import TapChangerInfoBuilder


def test_tap_changer_info_add_asset_info(network, container):
    builder = TapChangerInfoBuilder(network=network, container=container)
    info = builder.create(mRID="tci_reg1", name="tci_reg1")

    builder.add_asset_info(
        info,
        phaseCount="singlePhase",
        ratedApparentPower=Qty(50, "kVA"),
        ratedVoltage=Qty(7.2, "kV"),
        ratedCurrent=Qty(100, "A"),
        ctRating=Qty(100, "A"),
        ptRatio=60.0,
        highStep=16,
        lowStep=-16,
        neutralStep=0,
        stepVoltageIncrement=0.625,
    )
    assert info.phaseCount.name == "singlePhase"
    assert float(info.ratedApparentPower.to("kVA")) == 50
    assert info.highStep == 16
    assert info.lowStep == -16
    assert float(info.stepVoltageIncrement) == 0.625
