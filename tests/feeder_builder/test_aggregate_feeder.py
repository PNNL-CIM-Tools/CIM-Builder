"""new_aggregate_feeder below a single-bus substation, on a fresh cim18v17 FeederModel."""

import os

import pytest

os.environ.setdefault("CIMG_CIM_PROFILE", "cim18v17")
os.environ.setdefault("CIMG_USE_UNITS", "TRUE")
os.environ.setdefault("CIMG_SYSTEM_MVA_BASE", "100")

import cimprofiles.cim18.cim18v17 as cim
from cimgraph.models import FeederModel
from cimtables.units import Qty

from cimbuilder.feeder_builder.aggregate_feeder import new_aggregate_feeder
from cimbuilder.object_builder import BaseVoltageBuilder
from cimbuilder.substation_builder import SingleBusSubstationBuilder


@pytest.fixture
def network():
    region = cim.Feeder(mRID="transmission", name="transmission")
    net = FeederModel(container=region, connection=None)
    net.add_to_graph(region)
    BaseVoltageBuilder(network=net, container=region).create(
        mRID="bv_12_47kV", nominalVoltage=Qty(12.47, "kV")
    )
    builder = SingleBusSubstationBuilder(net, region)
    substation = builder.create(mRID="sub_1")
    _, voltage_level = builder.add_voltage_level(substation, mRID="vl_12", BaseVoltage="bv_12_47kV")
    builder.add_buses(voltage_level)
    builder.add_branch(voltage_level, number=1, node="sub_1_feeder_1")
    return net


@pytest.fixture
def aggregate(network):
    return new_aggregate_feeder(
        network,
        mRID="agg_1",
        name="agg1",
        NormalEnergizingSubstation="sub_1",
        node="sub_1_feeder_1",
        BaseVoltage="bv_12_47kV",
        load_p=Qty(5, "MW"),
        load_q=Qty(1, "MVAr"),
        btm_pv_p=Qty(800, "kW"),
        btm_wind_p=Qty(200, "kW"),
        ftm_pv_p=Qty(2, "MW"),
    )


def test_topology(network, aggregate):
    feeder, load, breaker = aggregate
    node1, node2 = (terminal.ConnectivityNode.mRID for terminal in sorted(
        breaker.Terminals, key=lambda terminal: terminal.sequenceNumber
    ))
    assert (node1, node2) == ("sub_1_feeder_1", "agg_1_node_1")
    assert feeder.NormalEnergizingSubstation.mRID == "sub_1"
    assert feeder.NormalHeadTerminal == [breaker.Terminals[1]]
    assert breaker.EquipmentContainer is feeder
    assert load.Terminals[0].ConnectivityNode.mRID == "agg_1_node_1"
    assert load.aggregate is True


def test_power_in_si_units(network, aggregate):
    _, load, _ = aggregate
    assert float(load.p.to("MW")) == pytest.approx(5)
    assert float(load.q.to("MVAr")) == pytest.approx(1)
    btm = network.find_by_mRID("agg_1_btm")
    ftm = network.find_by_mRID("agg_1_ftm")
    assert float(btm.p.to("kW")) == pytest.approx(1000)
    assert {type(unit).__name__ for unit in btm.PowerElectronicsUnit} == {
        "PhotoVoltaicUnit", "PowerElectronicsWindUnit"
    }
    assert [type(unit).__name__ for unit in ftm.PowerElectronicsUnit] == ["PhotoVoltaicUnit"]
    assert float(network.find_by_mRID("agg_1_ftm_pv").maxP.to("MW")) == pytest.approx(2)


def test_measurements(network, aggregate):
    _, load, breaker = aggregate
    analogs = {analog.name: analog for analog in network.graph[cim.Analog].values()}
    assert set(analogs) == {
        "NetLoad(MW)_agg1", "ExcessGeneration(MW)_agg1", "TotalGeneration(MW)_agg1",
        "GrossLoad(MW)_agg1", "BTMGeneration(MW)_agg1", "FTMGeneration(MW)_agg1",
    }
    for analog in analogs.values():
        assert analog.measurementType == "ThreePhaseActivePower"
        assert analog.description == "MMXU.TotW"
        assert analog.phases == cim.PhaseCode.ABC
    assert analogs["GrossLoad(MW)_agg1"].PowerSystemResource is load

    [position] = network.graph[cim.Discrete].values()
    assert position.measurementType == "SwitchPosition"
    assert position.description == "XCBR.Pos"
    assert position.PowerSystemResource is breaker
    assert position.Terminal is breaker.Terminals[1]
