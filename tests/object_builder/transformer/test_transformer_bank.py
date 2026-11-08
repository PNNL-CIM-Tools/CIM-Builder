import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.base import BaseVoltageBuilder
from cimbuilder.object_builder.transformer import TransformerBankBuilder


@pytest.fixture
def builder(network, container):
    return TransformerBankBuilder(network=network, container=container)


@pytest.fixture
def ob1(network, container, builder):
    """open-wye open-delta bank xf_ob1 (open_wye_open_delta_example.cimtbl), ends and phase ends only"""
    bv_builder = BaseVoltageBuilder(network=network, container=container)
    hv = bv_builder.create(mRID="bv_12_47kv", nominalVoltage=Qty(12.47, "kV"))
    lv = bv_builder.create(mRID="bv_240v", nominalVoltage=Qty(240, "V"))
    xfmr = builder.create(mRID="xf_ob1", name="ob1")
    builder.add_connectivity(xfmr)
    builder.add_power_transformer_end(
        xfmr, node="cn_ob1_pri", endNumber=1, phases="ABN", connectionKind="oY", BaseVoltage=hv.mRID
    )
    builder.add_power_transformer_end(
        xfmr, node="cn_ob1_sec", endNumber=2, phases="ABCN", connectionKind="oD", BaseVoltage=lv.mRID
    )
    for endNumber, sequenceNumber, phase, phaseNeutralU in [
        (1, 1, "A", Qty(7200, "V")),
        (1, 2, "B", Qty(7200, "V")),
        (1, 3, "N", 0),
        (2, 4, "A", Qty(120, "V")),
        (2, 5, "B", Qty(120, "V")),
        (2, 6, "C", Qty(207.8, "V")),
        (2, 7, "N", 0),
    ]:
        builder.add_transformer_phase_end(
            xfmr, endNumber=endNumber, sequenceNumber=sequenceNumber, phase=phase, phaseNeutralU=phaseNeutralU
        )
    return xfmr


def test_ends_and_phase_ends(network, ob1):
    end1, end2 = sorted(ob1.PowerTransformerEnd, key=lambda end: end.endNumber)
    assert [end1.mRID, end2.mRID] == ["xf_ob1_1", "xf_ob1_2"]
    assert end1.Terminal.phases == network.cim.PhaseCode("ABN")
    assert end2.Terminal.sequenceNumber == 2
    phase_end = network.find_by_mRID("xf_ob1_2_c")
    assert phase_end.Terminal is end2.Terminal
    assert phase_end.phase == network.cim.SinglePhaseKind("C")
    assert float(phase_end.phaseNeutralU.to("V")) == pytest.approx(207.8)


def test_lighting_tank(builder, ob1, container):
    """the 50 kVA lighting tank L: H1-H2 primary, X1-X2-X3 center-tapped secondary"""
    _, tank = builder.add_transformer_tank(
        ob1,
        TransformerTank="xf_ob1_tank_l",
        noLoadLoss=Qty(90, "W"),
        loadLoss=Qty(540, "W"),
        percentImpedance=2.0,
    )
    lugs = {}
    for designation, sequenceNumber, phase_end in [
        ("H1", 1, "xf_ob1_1_a"),
        ("H2", 3, "xf_ob1_1_n"),
        ("X1", 4, "xf_ob1_2_a"),
        ("X2", 7, "xf_ob1_2_n"),
        ("X3", 5, "xf_ob1_2_b"),
    ]:
        _, lugs[designation] = builder.add_transformer_lug(
            ob1, TransformerTank=tank.mRID, designation=designation,
            sequenceNumber=sequenceNumber, TransformerEnd=phase_end,
        )
    _, core = builder.add_transformer_core(ob1, TransformerTank=tank.mRID, form="shellForm")
    windings = {}
    for from_lug, to_lug, ratedU, baseU, ratedS in [
        ("H1", "H2", Qty(12470, "V"), Qty(7200, "V"), Qty(50, "kVA")),
        ("X1", "X2", Qty(240, "V"), Qty(120, "V"), Qty(25, "kVA")),
        ("X2", "X3", Qty(240, "V"), Qty(120, "V"), Qty(25, "kVA")),
    ]:
        _, windings[from_lug + to_lug] = builder.add_transformer_winding(
            ob1,
            TransformerTank=tank.mRID,
            FromTransformerLug=lugs[from_lug].mRID,
            ToTransformerLug=lugs[to_lug].mRID,
            TransformerCore=core.mRID,
            connection="I",
            ratedU=ratedU,
            baseU=baseU,
            ratedS=ratedS,
            baseS=Qty(50, "kVA"),
        )
    _, mesh = builder.add_mesh_impedance(
        ob1,
        FromWinding=windings["H1H2"].mRID,
        ToWinding=windings["X1X2"].mRID,
        r=Qty(1.62, "percent"),
        x=Qty(2.02, "percent"),
    )

    assert tank.PowerTransformer is ob1
    assert tank.EquipmentContainer is container
    assert float(tank.loadLoss.to("W")) == 540
    assert lugs["X2"].mRID == "xf_ob1_tank_l_lug_x2"
    assert lugs["X2"].TransformerTank is tank
    assert lugs["X2"].TransformerEnd.mRID == "xf_ob1_2_n"
    assert core.mRID == "xf_ob1_tank_l_core"
    assert core.TransformerTank is tank
    assert core.form.name == "shellForm"
    winding = windings["X1X2"]
    assert winding.mRID == "xf_ob1_tank_l_wdg_x1x2"
    assert winding.FromTransformerLug is lugs["X1"]
    assert winding.ToTransformerLug is lugs["X2"]
    assert winding.TransformerTank is tank
    assert winding.TransformerCore is core
    # 1.62 % on the H1-H2 winding's 7200 V / 50 kVA base
    assert float(mesh.r.to("ohm")) == pytest.approx(0.0162 * 7200**2 / 50e3)
    assert mesh.FromWinding is windings["H1H2"]


def test_multi_tank_bank(builder, ob1):
    _, tank_l = builder.add_transformer_tank(ob1, TransformerTank="xf_ob1_tank_l")
    _, tank_t = builder.add_transformer_tank(ob1, TransformerTank="xf_ob1_tank_t")
    assert set(ob1.TransformerTanks) == {tank_l, tank_t}


def test_lug_on_another_transformers_tank(builder, ob1):
    other = builder.create(mRID="xf_other")
    builder.add_connectivity(other)
    builder.add_transformer_tank(other)
    with pytest.raises(ValueError, match="not a tank of this transformer"):
        builder.add_transformer_lug(ob1, TransformerTank="xf_other_tank", designation="H1")


def test_add_transformer_phase_end_needs_its_end(builder):
    xfmr = builder.create(mRID="xf_1")
    builder.add_connectivity(xfmr)
    with pytest.raises(ValueError, match="endNumber 2"):
        builder.add_transformer_phase_end(xfmr, endNumber=2, sequenceNumber=1, phase="A")
