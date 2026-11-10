import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.base import BaseVoltageBuilder
from cimbuilder.object_builder.transformer import (
    TransformerBankFromConfigurationBuilder,
    TransformerTankConfigurationBuilder,
)


@pytest.fixture
def template(network, container):
    """padmount_1ph_250kva tank configuration, lugs only (enough for an instance)"""
    builder = TransformerTankConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="xc_padmount_1ph_250kva")
    for designation, sequenceNumber in [("H1A", 1), ("H1B", 2), ("H2", 5), ("X1", 3), ("X2", 5), ("X3", 4)]:
        builder.add_transformer_lug(config, designation=designation, sequenceNumber=sequenceNumber)
    return config


@pytest.fixture
def bases(network, container):
    builder = BaseVoltageBuilder(network=network, container=container)
    return (
        builder.create(mRID="bv_12_47kv", nominalVoltage=Qty(12.47, "kV")),
        builder.create(mRID="bv_240v", nominalVoltage=Qty(240, "V")),
    )


def test_padmount_instance(network, container, template, bases):
    """padmount_example.cimtbl: one center-tap padmount built from its template"""
    hv, lv = bases
    builder = TransformerBankFromConfigurationBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xf_padmount_2341", name="padmount_2341")
    builder.add_connectivity(xfmr)
    _, t1, end1 = builder.add_power_transformer_end(
        xfmr, node="cn_2341_hv", endNumber=1, phases="AB", connectionKind="Y", BaseVoltage=hv.mRID
    )
    _, t2, end2 = builder.add_power_transformer_end(
        xfmr, node="cn_2341_lv", endNumber=2, phases="s1s2N", connectionKind="I", BaseVoltage=lv.mRID
    )
    _, tank = builder.add_transformer_tank(xfmr, TankConfiguration=template.mRID)
    phase_ends = [
        builder.add_transformer_phase_end(
            xfmr, endNumber=endNumber, sequenceNumber=sequenceNumber, phase=phase, phaseNeutralU=phaseNeutralU
        )[1]
        for endNumber, sequenceNumber, phase, phaseNeutralU in [
            (1, 1, "A", Qty(7200, "V")),
            (1, 2, "B", Qty(7200, "V")),
            (2, 3, "s1", Qty(120, "V")),
            (2, 4, "s2", Qty(120, "V")),
            (2, 5, "N", 0),
        ]
    ]

    assert [end1.mRID, end2.mRID] == ["xf_padmount_2341_1", "xf_padmount_2341_2"]
    assert t1.phases == network.cim.PhaseCode("AB")
    assert t2.phases == network.cim.PhaseCode("s12N")
    assert t2.sequenceNumber == 2
    assert tank.mRID == "xf_padmount_2341_tank"
    assert tank.PowerTransformer is xfmr
    assert tank.TankConfiguration is template
    assert tank.EquipmentContainer is container
    assert [pe.mRID for pe in phase_ends] == [
        "xf_padmount_2341_1_a",
        "xf_padmount_2341_1_b",
        "xf_padmount_2341_2_s1",
        "xf_padmount_2341_2_s2",
        "xf_padmount_2341_2_n",
    ]
    assert [pe.Terminal for pe in phase_ends] == [t1, t1, t2, t2, t2]
    assert phase_ends[2].phase == network.cim.SinglePhaseKind("s1")
    assert float(phase_ends[0].phaseNeutralU.to("V")) == 7200


def test_multi_tank_bank(network, container, template, bases):
    """open_wye_open_delta_example.cimtbl shape, but with templated tanks: two tanks on one
    PowerTransformer need their own mRIDs"""
    hv, _ = bases
    builder = TransformerBankFromConfigurationBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xf_ob1")
    builder.add_connectivity(xfmr)
    builder.add_power_transformer_end(
        xfmr, node="cn_ob1_pri", endNumber=1, phases="ABN", connectionKind="oY", BaseVoltage=hv.mRID
    )
    _, tank_l = builder.add_transformer_tank(xfmr, TankConfiguration=template.mRID, TransformerTank="xf_ob1_tank_l")
    _, tank_t = builder.add_transformer_tank(xfmr, TankConfiguration=template.mRID, TransformerTank="xf_ob1_tank_t")
    assert set(xfmr.TransformerTanks) == {tank_l, tank_t}


def test_add_transformer_tank_unknown_template(network, container):
    builder = TransformerBankFromConfigurationBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xf_1")
    builder.add_connectivity(xfmr)
    with pytest.raises(ValueError, match="TankConfiguration"):
        builder.add_transformer_tank(xfmr, TankConfiguration="xc_missing")
