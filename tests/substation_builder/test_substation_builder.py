"""Builds each node-breaker substation layout on a fresh cim18v17 FeederModel and checks the
switch wiring through the Terminals each switch was given."""

import os

import pytest

os.environ.setdefault("CIMG_CIM_PROFILE", "cim18v17")
os.environ.setdefault("CIMG_USE_UNITS", "TRUE")
os.environ.setdefault("CIMG_SYSTEM_MVA_BASE", "100")

import cimprofiles.cim18.cim18v17 as cim
from cimgraph.models import FeederModel
from cimtables.units import Qty

from cimbuilder.object_builder import (
    BaseVoltageBuilder,
    ConnectivityNodeBuilder,
    FeederBuilder,
)
from cimbuilder.substation_builder import (
    BreakerAndHalfSubstationBuilder,
    DoubleBusSingleBreakerSubstationBuilder,
    MainAndTransferSubstationBuilder,
    RingBusSubstationBuilder,
    SectionalizedBusSubstationBuilder,
    SingleBusSubstationBuilder,
    SubstationBuilder,
)


@pytest.fixture
def network():
    feeder = cim.Feeder(mRID="fdr_1", name="fdr_1")
    net = FeederModel(container=feeder, connection=None)
    net.add_to_graph(feeder)
    BaseVoltageBuilder(network=net, container=feeder).create(
        mRID="bv_115kV", nominalVoltage=Qty(115, "kV")
    )
    return net


def new_voltage_level(builder: SubstationBuilder):
    substation = builder.create(mRID="sub_1")
    substation, voltage_level = builder.add_voltage_level(
        substation, mRID="vl_115", BaseVoltage="bv_115kV"
    )
    return substation, voltage_level


def nodes_of(switch) -> set[str]:
    return {terminal.ConnectivityNode.mRID for terminal in switch.Terminals}


def test_add_voltage_level_and_bay(network):
    builder = SubstationBuilder(network, network.container)
    substation, voltage_level = new_voltage_level(builder)

    voltage_level, bay = builder.add_bay(
        voltage_level, mRID="bay_1", breakerConfiguration="singleBreaker"
    )

    assert voltage_level in substation.VoltageLevels
    assert voltage_level.BaseVoltage.mRID == "bv_115kV"
    assert bay in voltage_level.Bays


def test_single_bus(network):
    builder = SingleBusSubstationBuilder(network, network.container)
    _, voltage_level = new_voltage_level(builder)

    voltage_level, busbars, ties = builder.add_buses(voltage_level)
    voltage_level, switches = builder.add_branch(voltage_level, number=1, node="line_1")

    assert [busbar.mRID for busbar in busbars] == ["vl_115_bus_1_bbs"]
    assert ties == []
    disconnector1, breaker, disconnector2 = switches
    assert isinstance(breaker, cim.Breaker)
    assert nodes_of(disconnector1) == {"vl_115_bus_1", "vl_115_1_j1"}
    assert nodes_of(breaker) == {"vl_115_1_j1", "vl_115_1_j2"}
    assert nodes_of(disconnector2) == {"vl_115_1_j2", "line_1"}
    for switch in switches:
        assert switch.EquipmentContainer is voltage_level
        assert switch.BaseVoltage.mRID == "bv_115kV"
        assert switch.normalOpen is False


def test_branch_node_created_in_voltage_level(network):
    builder = SingleBusSubstationBuilder(network, network.container)
    _, voltage_level = new_voltage_level(builder)
    builder.add_buses(voltage_level)

    builder.add_branch(voltage_level, number=1, node="line_1")

    node = network.find_by_mRID("line_1")
    assert node.ConnectivityNodeContainer is voltage_level
    assert node.BaseVoltage.mRID == "bv_115kV"


def test_feeder_head_node_keeps_feeder_container(network):
    feeder = network.container
    node_builder = ConnectivityNodeBuilder(network, feeder)
    sourcebus = node_builder.create(mRID="sourcebus")
    node_builder.add_connectivity(sourcebus, BaseVoltage="bv_115kV")

    builder = SingleBusSubstationBuilder(network, feeder)
    substation, voltage_level = new_voltage_level(builder)
    builder.add_buses(voltage_level)
    _, switches = builder.add_branch(voltage_level, number=1, node="sourcebus")
    FeederBuilder(network, feeder).add_connectivity(
        feeder, NormalEnergizingSubstation=substation.mRID
    )

    assert sourcebus.ConnectivityNodeContainer is feeder
    assert "sourcebus" in nodes_of(switches[-1])
    assert feeder in substation.NormalEnergizedFeeder


def test_add_branch_before_add_buses(network):
    builder = SingleBusSubstationBuilder(network, network.container)
    _, voltage_level = new_voltage_level(builder)

    with pytest.raises(ValueError, match="add_buses"):
        builder.add_branch(voltage_level, number=1, node="line_1")


def test_sectionalized_bus(network):
    builder = SectionalizedBusSubstationBuilder(network, network.container)
    _, voltage_level = new_voltage_level(builder)

    voltage_level, busbars, ties = builder.add_buses(voltage_level, sections=3)
    voltage_level, switches = builder.add_branch(
        voltage_level, section=3, number=1, node="line_1"
    )

    assert len(busbars) == 3
    assert len(ties) == 6  # two tie bays, disconnector - breaker - disconnector each
    assert "vl_115_bus_1" in nodes_of(ties[0])
    assert "vl_115_bus_3" in nodes_of(ties[-1])
    assert "vl_115_bus_3" in nodes_of(switches[0])

    with pytest.raises(ValueError, match="vl_115_bus_4"):
        builder.add_branch(voltage_level, section=4, number=2, node="line_2")


def test_ring_bus(network):
    builder = RingBusSubstationBuilder(network, network.container)
    _, voltage_level = new_voltage_level(builder)

    voltage_level, busbars, ring = builder.add_buses(voltage_level, sections=4)
    voltage_level, switches = builder.add_branch(voltage_level, section=2, node="line_1")

    assert len(busbars) == 4
    assert len(ring) == 12
    # the last ring bay closes the ring back onto bus 1
    assert nodes_of(ring[-1]) == {"vl_115_ring_4_j2", "vl_115_bus_1"}
    [disconnector] = switches
    assert nodes_of(disconnector) == {"vl_115_bus_2", "line_1"}


def test_ring_bus_needs_three_sections(network):
    builder = RingBusSubstationBuilder(network, network.container)
    _, voltage_level = new_voltage_level(builder)

    with pytest.raises(ValueError, match="at least 3"):
        builder.add_buses(voltage_level, sections=2)


def test_main_and_transfer(network):
    builder = MainAndTransferSubstationBuilder(network, network.container)
    _, voltage_level = new_voltage_level(builder)

    voltage_level, busbars, tie = builder.add_buses(voltage_level)
    voltage_level, switches = builder.add_branch(voltage_level, number=1, node="line_1")

    assert [busbar.mRID for busbar in busbars] == [
        "vl_115_bus_main_bbs",
        "vl_115_bus_transfer_bbs",
    ]
    assert len(tie) == 3
    *bay, bypass = switches
    assert "vl_115_bus_main" in nodes_of(bay[0])
    assert nodes_of(bypass) == {"line_1", "vl_115_bus_transfer"}
    assert bypass.normalOpen is True
    assert bypass.open is True


def test_double_bus_single_breaker(network):
    builder = DoubleBusSingleBreakerSubstationBuilder(network, network.container)
    _, voltage_level = new_voltage_level(builder)

    voltage_level, busbars, tie = builder.add_buses(voltage_level)
    voltage_level, switches = builder.add_branch(
        voltage_level, number=1, node="line_1", bus=2
    )

    assert len(busbars) == 2
    assert len(tie) == 3
    selector1, selector2, breaker, disconnector = switches
    assert nodes_of(selector1) == {"vl_115_bus_1", "vl_115_1_j1"}
    assert nodes_of(selector2) == {"vl_115_bus_2", "vl_115_1_j1"}
    assert selector1.normalOpen is True
    assert selector2.normalOpen is False
    assert isinstance(breaker, cim.Breaker)
    assert nodes_of(disconnector) == {"vl_115_1_j2", "line_1"}

    with pytest.raises(ValueError, match="bus must be 1 or 2"):
        builder.add_branch(voltage_level, number=2, node="line_2", bus=3)


def test_breaker_and_half(network):
    builder = BreakerAndHalfSubstationBuilder(network, network.container)
    _, voltage_level = new_voltage_level(builder)

    voltage_level, busbars, diameters = builder.add_buses(voltage_level, diameters=2)
    voltage_level, switches = builder.add_branch(
        voltage_level, diameter=2, side=2, node="line_1"
    )

    assert len(busbars) == 2
    assert len(diameters) == 18  # three breaker bays per diameter
    breakers = [switch for switch in diameters if isinstance(switch, cim.Breaker)]
    assert len(breakers) == 6
    assert "vl_115_bus_1" in nodes_of(diameters[0])
    assert "vl_115_bus_2" in nodes_of(diameters[-1])
    [disconnector] = switches
    assert nodes_of(disconnector) == {"vl_115_dia_2_side_2", "line_1"}

    with pytest.raises(ValueError, match="side must be 1 or 2"):
        builder.add_branch(voltage_level, diameter=1, side=3, node="line_2")
