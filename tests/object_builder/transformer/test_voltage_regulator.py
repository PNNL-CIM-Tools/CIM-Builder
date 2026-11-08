"""Builds CIMTBL-Models/distribution/regulator_example.cimtbl: one single-phase
ANSI type A step-voltage regulator, 7620 V, 100 A, 76.2 kVA, +/-10 % in 32 steps."""
import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.transformer import (
    RatioTapChangerBuilder,
    TapChangerControlBuilder,
    VoltageRegulatorBuilder,
)


@pytest.fixture
def builder(network, container):
    return VoltageRegulatorBuilder(network=network, container=container)


@pytest.fixture
def regulator(builder):
    regulator = builder.create(mRID="vr_reg1a", name="reg1a")
    builder.add_connectivity(regulator, construction="typeA")
    return regulator


@pytest.fixture
def ends(builder, regulator, base_voltage):
    nodes = {1: "cn_reg1_src", 2: "cn_reg1_load"}
    ends = {}
    for endNumber, node in nodes.items():
        _, _, end = builder.add_auto_transformer_end(
            regulator, node=node, endNumber=endNumber, phase="AN", BaseVoltage=base_voltage.mRID
        )
        builder.add_electrical(end, baseU=Qty(7.62, "kV"), ratedS=Qty(762, "kVA"))
        ends[endNumber] = end
    return ends


@pytest.fixture
def winding(builder, regulator, ends):
    builder.add_transformer_lug(regulator, designation="S", sequenceNumber=1, TransformerEnd=ends[1].mRID)
    builder.add_transformer_lug(regulator, designation="L", sequenceNumber=2, TransformerEnd=ends[2].mRID)
    builder.add_transformer_lug(regulator, designation="SL", sequenceNumber=3)
    _, winding = builder.add_transformer_winding(
        regulator,
        FromTransformerEnd=ends[1].mRID,
        ToTransformerEnd=ends[2].mRID,
        FromTransformerLug="vr_reg1a_lug_s",
        ToTransformerLug="vr_reg1a_lug_sl",
        AutoTransformerLug="vr_reg1a_lug_l",
        ratedS=Qty(76.2, "kVA"),
        baseU=Qty(7.62, "kV"),
    )
    return winding


def test_add_connectivity(network, regulator, container):
    assert regulator.construction == network.cim.RegulatorConstructionKind("typeA")
    assert regulator.EquipmentContainer is container


def test_add_auto_transformer_end(network, regulator, ends, base_voltage):
    end2 = ends[2]
    assert end2.mRID == "vr_reg1a_end2"
    assert end2.AutoTransformer is regulator
    assert end2.BaseVoltage is base_voltage
    assert end2.phase == network.cim.PhaseCode("AN")
    assert float(end2.baseU.to("kV")) == pytest.approx(7.62)
    assert float(end2.ratedS.to("kVA")) == pytest.approx(762)

    terminal = end2.Terminal
    assert terminal.mRID == "vr_reg1a_T2"
    assert terminal.sequenceNumber == 2
    assert terminal.ConductingEquipment is regulator
    assert terminal.phases == network.cim.PhaseCode("AN")
    assert terminal.ConnectivityNode.mRID == "cn_reg1_load"
    assert len(regulator.Terminals) == 2


def test_add_transformer_winding(regulator, ends, winding):
    assert winding.mRID == "vr_reg1a_wdg"
    assert regulator.AutoTransformerWinding is winding
    assert winding.AutoTransformer is regulator
    assert winding.FromTransformerEnd is ends[1]
    assert winding.ToTransformerEnd is ends[2]
    assert winding.FromTransformerLug.designation == "S"
    assert winding.ToTransformerLug.designation == "SL"
    assert winding.AutoTransformerLug.designation == "L"
    assert winding.AutoTransformerLug.TransformerEnd is ends[2]
    assert float(winding.ratedS.to("kVA")) == pytest.approx(76.2)


def test_add_transformer_winding_missing_lug(builder, regulator, ends):
    with pytest.raises(ValueError, match="FromTransformerLug 'vr_reg1a_lug_s' not found"):
        builder.add_transformer_winding(
            regulator,
            FromTransformerEnd=ends[1].mRID,
            ToTransformerEnd=ends[2].mRID,
            FromTransformerLug="vr_reg1a_lug_s",
            ToTransformerLug="vr_reg1a_lug_sl",
            AutoTransformerLug="vr_reg1a_lug_l",
        )


def test_tap_changer_control_and_ratio_tap_changer(network, container, ends, winding):
    """Type A: tap changer on end 2 (L), controlled from the end 2 Terminal."""
    control_builder = TapChangerControlBuilder(network=network, container=container)
    control = control_builder.create(mRID="vr_reg1a_ctrl", name="reg1a_ctrl")
    control_builder.add_regulating_control(
        control,
        Terminal="vr_reg1a_T2",
        mode="voltage",
        monitoredPhase="A",
        targetValue=7620,
        targetDeadband=127,
        discrete=True,
        enabled=True,
        lineDropCompensation=False,
    )

    tap_builder = RatioTapChangerBuilder(network=network, container=container)
    tap_changer = tap_builder.create(mRID="vr_reg1a_tap", name="reg1a_tap")
    tap_builder.add_connectivity(tap_changer, TransformerEnd=ends[2].mRID)
    tap_builder.add_electrical(
        tap_changer, highStep=16, lowStep=-16, normalStep=0, stepVoltageIncrement=0.625
    )
    tap_builder.add_regulating_control(
        tap_changer,
        neutralStep=0,
        neutralU=Qty(7.62, "kV"),
        TapChangerControl=control.mRID,
        ltcFlag=True,
        controlEnabled=True,
        ptRatio=63.5,
        ctRating=100,
        initialDelay=Qty(30, "s"),
        subsequentDelay=Qty(2, "s"),
    )
    tap_builder.add_ssh(tap_changer, step=0)

    assert control.Terminal is ends[2].Terminal
    assert control.mode == network.cim.RegulatingControlModeKind("voltage")
    assert control.targetValue == 7620
    assert tap_changer.TransformerEnd is ends[2]
    assert ends[2].RatioTapChanger is tap_changer
    assert tap_changer.TapChangerControl is control
    assert float(tap_changer.stepVoltageIncrement) == pytest.approx(0.625)
    assert float(tap_changer.neutralU.to("kV")) == pytest.approx(7.62)
    assert float(tap_changer.initialDelay.to("s")) == pytest.approx(30)
    assert tap_changer.step == 0
