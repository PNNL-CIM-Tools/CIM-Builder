import pytest
import cimprofiles.cim18.cim18v17 as cim
from cimtables.units import Qty

from cimbuilder.object_builder.transformer import (
    PowerTransformerBuilder,
    RatioTapChangerBuilder,
    TapChangerControlBuilder,
)


def test_power_transformer_add_connectivity(network, container):
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    builder.add_connectivity(xfmr)
    assert xfmr.EquipmentContainer is container


def test_power_transformer_add_power_transformer_end(network, container, base_voltage):
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    builder.add_connectivity(xfmr)

    _, terminal, xfmr_end = builder.add_power_transformer_end(
        xfmr, node="bus1", endNumber=2, connectionKind="Yn", BaseVoltage=base_voltage.mRID
    )
    assert xfmr_end.mRID == "xfmr1_2"
    assert xfmr_end.PowerTransformer is xfmr
    assert xfmr_end.endNumber == 2
    assert xfmr_end.connectionKind == network.cim.WindingConnection("Yn")
    assert xfmr_end.BaseVoltage is base_voltage
    assert xfmr_end.Terminal is terminal
    assert terminal.mRID == "xfmr1_T2"
    assert terminal.sequenceNumber == 2
    assert terminal.ConductingEquipment is xfmr
    assert network.find_by_mRID(xfmr_end.mRID) is xfmr_end


def test_power_transformer_ltc(network, container, base_voltage):
    """115 / 12.47 kV substation step-down transformer with an LTC on the LV end,
    +/-10 % in 32 steps of 5/8 %, regulating to 124 V on a 7200/120 PT."""
    from cimbuilder.object_builder.base import BaseVoltageBuilder

    hv = BaseVoltageBuilder(network=network, container=container).create(
        mRID="bv_115kV", nominalVoltage=Qty(115, "kV")
    )
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    builder.add_connectivity(xfmr)
    builder.add_power_transformer_end(
        xfmr, node="hv_bus", endNumber=1, connectionKind="D", BaseVoltage=hv.mRID
    )
    _, lv_terminal, lv_end = builder.add_power_transformer_end(
        xfmr, node="lv_bus", endNumber=2, connectionKind="Yn", BaseVoltage=base_voltage.mRID
    )

    control_builder = TapChangerControlBuilder(network=network, container=container)
    control = control_builder.create(mRID="xfmr1_ctrl")
    control_builder.add_regulating_control(
        control,
        Terminal=lv_terminal.mRID,
        mode="voltage",
        monitoredPhase="A",
        targetValue=124 * 60,
        targetDeadband=2 * 60,
        discrete=True,
        enabled=True,
    )
    tap_builder = RatioTapChangerBuilder(network=network, container=container)
    tap_changer = tap_builder.create(mRID="xfmr1_ltc")
    tap_builder.add_connectivity(tap_changer, TransformerEnd=lv_end.mRID)
    tap_builder.add_electrical(
        tap_changer, highStep=16, lowStep=-16, normalStep=0, stepVoltageIncrement=0.625
    )
    tap_builder.add_regulating_control(
        tap_changer,
        neutralStep=0,
        neutralU=Qty(12.47, "kV"),
        TapChangerControl=control.mRID,
        ltcFlag=True,
        controlEnabled=True,
        ptRatio=60,
        initialDelay=Qty(30, "s"),
        subsequentDelay=Qty(5, "s"),
    )
    tap_builder.add_ssh(tap_changer, step=2)

    assert control.Terminal is lv_terminal
    assert control.mode == network.cim.RegulatingControlModeKind("voltage")
    assert tap_changer.TransformerEnd is lv_end
    assert lv_end.RatioTapChanger is tap_changer
    assert tap_changer.TapChangerControl is control
    assert tap_changer.ltcFlag is True
    assert float(tap_changer.neutralU.to("kV")) == pytest.approx(12.47)
    assert tap_changer.step == 2


def test_power_transformer_add_electrical(network, container):
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr_end = cim.PowerTransformerEnd(mRID="xfmr1_end1", endNumber=1)
    network.add_to_graph(xfmr_end)

    builder.add_electrical(
        xfmr_end, r=Qty(1, "ohm"), x=Qty(5, "ohm"), ratedS=Qty(1, "MVA"), ratedU=Qty(12.47, "kV")
    )
    assert float(xfmr_end.r.to("ohm")) == 1


def test_power_transformer_add_mesh_impedance(network, container):
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    end1 = cim.PowerTransformerEnd(mRID="end1", endNumber=1)
    end2 = cim.PowerTransformerEnd(mRID="end2", endNumber=2)
    network.add_to_graph(end1)
    network.add_to_graph(end2)

    xfmr, mesh = builder.add_mesh_impedance(
        xfmr, FromTransformerEnd="end1", ToTransformerEnd="end2", r=Qty(1, "ohm"), x=Qty(5, "ohm")
    )
    assert mesh.mRID == "xfmr1_mesh_12"
    assert float(mesh.r.to("ohm")) == 1


def test_power_transformer_three_winding_meshes_get_unique_mrids(network, container):
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    for n in (1, 2, 3):
        network.add_to_graph(cim.PowerTransformerEnd(mRID=f"end{n}", endNumber=n))

    meshes = [
        builder.add_mesh_impedance(xfmr, FromTransformerEnd=f"end{a}", ToTransformerEnd=f"end{b}")[1]
        for a, b in [(1, 2), (1, 3), (2, 3)]
    ]
    assert [mesh.mRID for mesh in meshes] == ["xfmr1_mesh_12", "xfmr1_mesh_13", "xfmr1_mesh_23"]


def test_power_transformer_add_short_circuit(network, container):
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr_end = cim.PowerTransformerEnd(mRID="xfmr1_end1", endNumber=1)
    network.add_to_graph(xfmr_end)

    builder.add_short_circuit(xfmr_end, r0=Qty(1, "ohm"), x0=Qty(5, "ohm"))
    assert float(xfmr_end.r0.to("ohm")) == 1
    assert float(xfmr_end.x0.to("ohm")) == 5
