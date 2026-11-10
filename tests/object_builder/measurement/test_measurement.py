"""AnalogBuilder/DiscreteBuilder on builder-made equipment, and on the IEEE13 feeder."""

import logging

import cimprofiles.cim18.cim18v17 as cim
import pytest
from cimgraph.databases import XMLFile
from cimgraph.models import FeederModel

from cimbuilder.object_builder import (
    AnalogBuilder,
    BaseVoltageBuilder,
    BreakerBuilder,
    DiscreteBuilder,
    DisconnectorBuilder,
    EnergyConsumerBuilder,
    FuseBuilder,
    RatioTapChangerBuilder,
    TransformerBankBuilder,
    VoltageRegulatorBuilder,
)
from cimtables.units import Qty
from cimbuilder.object_builder.measurement.measurement import single_phases

IEEE13 = "49AD8E07-3BF9-A4E2-CB8F-C3722F837B62"


def new_load(network, container, base_voltage, phases=None):
    builder = EnergyConsumerBuilder(network, container)
    load = builder.create(mRID="load_1", name="load_1")
    builder.add_connectivity(load, node="bus_1", phases=phases, BaseVoltage=base_voltage.mRID)
    return load


def new_switch(builder_class, network, container, base_voltage, mRID):
    builder = builder_class(network, container)
    switch = builder.create(mRID=mRID, name=mRID)
    builder.add_connectivity(switch, node1="bus_1", node2="bus_2", BaseVoltage=base_voltage.mRID)
    return switch


def test_single_phases():
    assert single_phases("ABCN") == ["A", "B", "C"]
    assert single_phases("BN") == ["B"]
    assert single_phases("s12N") == ["s1", "s2"]
    assert single_phases("none") == []


def test_add_measurement(network, container, base_voltage):
    load = new_load(network, container, base_voltage)
    builder = AnalogBuilder(network, container)
    analog = builder.create(mRID="meas_1", description="MMXU.PNV.phsA")

    builder.add_measurement(
        analog,
        measurementType="PhaseToNeutralVoltage",
        PowerSystemResource=load.mRID,
        Terminal=load.Terminals[0].mRID,
        phases="A",
        unitSymbol="V",
    )

    assert isinstance(analog, cim.Analog)
    assert analog in load.Measurements
    assert analog in load.Terminals[0].Measurements
    assert analog.phases == cim.PhaseCode.A
    assert analog.unitSymbol == cim.UnitSymbol.V


def test_add_measurement_unknown_resource(network, container):
    builder = DiscreteBuilder(network, container)
    discrete = builder.create(mRID="meas_1")
    with pytest.raises(ValueError, match="PowerSystemResource"):
        builder.add_measurement(
            discrete, measurementType="SwitchPosition", PowerSystemResource="missing"
        )


def test_load_analogs_follow_terminal_phases(network, container, base_voltage):
    load = new_load(network, container, base_voltage, phases="BN")

    _, analogs = AnalogBuilder(network, container).add_load_analogs(load)

    assert {(a.measurementType, a.description) for a in analogs} == {
        ("PhaseToNeutralVoltage", "MMXU.PNV.phsB"),
        ("ApparentPower", "MMXU.VA.phsB"),
    }
    for analog in analogs:
        assert analog.phases == cim.PhaseCode.B
        assert analog.Terminal is load.Terminals[0]


def test_rebuild_returns_existing(network, container, base_voltage):
    load = new_load(network, container, base_voltage)
    builder = AnalogBuilder(network, container)

    _, first = builder.add_load_analogs(load)
    _, second = builder.add_load_analogs(load)

    assert len(first) == 6  # voltage and power on A, B, C
    assert second == first
    assert len(network.graph[cim.Analog]) == 6


def test_switch_analogs_measure_each_node_voltage_once(network, container, base_voltage):
    builder = AnalogBuilder(network, container)
    breaker = new_switch(BreakerBuilder, network, container, base_voltage, "brk_1")
    disconnector = new_switch(DisconnectorBuilder, network, container, base_voltage, "dis_1")

    _, breaker_analogs = builder.add_switch_analogs(breaker)
    _, disconnector_analogs = builder.add_switch_analogs(disconnector)

    assert [a.measurementType for a in breaker_analogs].count("PhaseToNeutralVoltage") == 6
    assert [a.measurementType for a in disconnector_analogs] == ["PhaseCurrent"] * 3


def test_switch_discretes_logical_node(network, container, base_voltage):
    builder = DiscreteBuilder(network, container)
    for builder_class, mRID, logical_node in [
        (BreakerBuilder, "brk_1", "XCBR"),
        (DisconnectorBuilder, "dis_1", "XSWI"),
        (FuseBuilder, "fuse_1", "XFUS"),
    ]:
        switch = new_switch(builder_class, network, container, base_voltage, mRID)
        _, discretes = builder.add_switch_discretes(switch)

        assert len(discretes) == 3
        for discrete in discretes:
            assert isinstance(discrete, cim.Discrete)
            assert discrete.measurementType == "SwitchPosition"
            assert discrete.description == f"{logical_node}.Pos"
            assert discrete.Terminal.sequenceNumber == 1


@pytest.fixture
def ieee13():
    logging.getLogger("cimgraph").setLevel(logging.ERROR)
    return FeederModel(
        container=cim.Feeder(mRID=IEEE13),
        connection=XMLFile(filename="tests/test_models/IEEE13.xml"),
        distributed=False,
    )


def test_ieee13_battery_state_of_charge(ieee13):
    builder = AnalogBuilder(ieee13, ieee13.container)
    state_of_charge = []
    for inverter in ieee13.graph[cim.PowerElectronicsConnection].values():
        _, analogs = builder.add_inverter_analogs(inverter)
        state_of_charge += [a for a in analogs if a.measurementType == "StateOfChargePct"]

    assert len(state_of_charge) == len(ieee13.graph[cim.BatteryUnit])
    for analog in state_of_charge:
        assert isinstance(analog.PowerSystemResource, cim.BatteryUnit)
        assert analog.Terminal is None
        assert analog.description == "DSTO.UseSocPct"


@pytest.fixture
def open_delta_bank(network, container):
    """open-wye open-delta bank: ABN primary, ABCN secondary, one TransformerPhaseEnd per conductor"""
    bv_builder = BaseVoltageBuilder(network, container)
    hv = bv_builder.create(mRID="bv_12_47kv", nominalVoltage=Qty(12.47, "kV"))
    lv = bv_builder.create(mRID="bv_240v", nominalVoltage=Qty(240, "V"))
    builder = TransformerBankBuilder(network, container)
    xfmr = builder.create(mRID="xf_ob1", name="ob1")
    builder.add_connectivity(xfmr)
    builder.add_power_transformer_end(
        xfmr, node="cn_pri", endNumber=1, phases="ABN", connectionKind="oY", BaseVoltage=hv.mRID
    )
    builder.add_power_transformer_end(
        xfmr, node="cn_sec", endNumber=2, phases="ABCN", connectionKind="oD", BaseVoltage=lv.mRID
    )
    for endNumber, sequenceNumber, phase in [
        (1, 1, "A"), (1, 2, "B"), (1, 3, "N"), (2, 4, "A"), (2, 5, "B"), (2, 6, "C"), (2, 7, "N"),
    ]:
        builder.add_transformer_phase_end(
            xfmr, endNumber=endNumber, sequenceNumber=sequenceNumber, phase=phase
        )
    return xfmr


def power_phases(analogs) -> list[tuple[int, str]]:
    return sorted(
        (analog.Terminal.sequenceNumber, analog.phases.value)
        for analog in analogs
        if analog.measurementType == "ApparentPower"
    )


def test_transformer_analogs_per_end_terminal(network, container, open_delta_bank):
    _, analogs = AnalogBuilder(network, container).add_transformer_analogs(open_delta_bank)

    assert power_phases(analogs) == [(1, "A"), (1, "B"), (2, "A"), (2, "B"), (2, "C")]
    assert len([a for a in analogs if a.measurementType == "PhaseToNeutralVoltage"]) == 5


def test_transformer_phases_from_phase_ends(network, container, open_delta_bank):
    """an imported model with TransformerPhaseEnds but no Terminal.phases"""
    for terminal in open_delta_bank.Terminals:
        terminal.phases = None

    _, analogs = AnalogBuilder(network, container).add_transformer_analogs(open_delta_bank)

    assert power_phases(analogs) == [(1, "A"), (1, "B"), (2, "A"), (2, "B"), (2, "C")]


def test_regulator_tap_position(network, container, base_voltage):
    """single-phase type A regulator on phase A, tap changer on end 2"""
    builder = VoltageRegulatorBuilder(network, container)
    regulator = builder.create(mRID="vr_reg1a", name="reg1a")
    builder.add_connectivity(regulator, construction="typeA")
    ends = {}
    for endNumber, node in {1: "cn_src", 2: "cn_load"}.items():
        _, _, ends[endNumber] = builder.add_auto_transformer_end(
            regulator, node=node, endNumber=endNumber, phase="AN", BaseVoltage=base_voltage.mRID
        )
    tap_builder = RatioTapChangerBuilder(network, container)
    tap_changer = tap_builder.create(mRID="vr_reg1a_tap", name="reg1a_tap")
    tap_builder.add_connectivity(tap_changer, TransformerEnd=ends[2].mRID)

    analog_builder = AnalogBuilder(network, container)
    _, [tap_position] = analog_builder.add_tap_changer_analogs(tap_changer)
    _, analogs = analog_builder.add_transformer_analogs(regulator)

    assert tap_position.measurementType == "TapPosition"
    assert tap_position.description == "ATCC.TapPos"
    assert tap_position.PowerSystemResource is tap_changer
    assert tap_position.Terminal is ends[2].Terminal
    assert tap_position.phases == cim.PhaseCode.A
    assert power_phases(analogs) == [(1, "A"), (2, "A")]
