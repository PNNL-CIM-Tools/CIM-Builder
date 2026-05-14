"""Tests for topology_builder.single_bus."""
from __future__ import annotations

import pytest

from cimbuilder._profile import get_cim
from cimbuilder.topology_builder.single_bus import (
    new_single_bus_substation,
    add_feeder_to_single_bus,
    add_branch_to_single_bus,
)


def test_creation_returns_correct_keys(tmp_xml):
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "TestSub", 115000)
    assert set(result) == {"network", "substation", "main_bus", "base_voltage"}


def test_substation_in_graph(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "TestSub", 115000)
    net = result["network"]
    assert cim.Substation in net.graph
    assert result["substation"] in net.graph[cim.Substation].values()


def test_main_bus_in_graph(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "TestSub", 115000)
    net = result["network"]
    assert cim.ConnectivityNode in net.graph
    assert result["main_bus"] in net.graph[cim.ConnectivityNode].values()


def test_bus_bar_section_created(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "TestSub", 115000)
    net = result["network"]
    net.get_all_edges(cim.BusbarSection)
    assert cim.BusbarSection in net.graph
    assert len(net.graph[cim.BusbarSection]) >= 1


def test_main_bus_name(tmp_xml):
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "MySub", 115000)
    assert result["main_bus"].name == "MySub_main_bus"


def test_base_voltage_created(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "TestSub", 115000)
    assert isinstance(result["base_voltage"], cim.BaseVoltage)


def test_add_feeder_returns_correct_keys(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "Sub1", 115000)
    feeder, feeder_net = minimal_feeder

    bay = add_feeder_to_single_bus(
        result["network"], result["substation"], result["main_bus"],
        result["base_voltage"], 10, feeder_net, feeder,
    )
    assert set(bay) == {"breaker", "disconnectors", "junctions"}
    assert len(bay["disconnectors"]) == 2
    assert len(bay["junctions"]) == 2


def test_add_feeder_links_to_substation(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "Sub1", 115000)
    feeder, feeder_net = minimal_feeder

    add_feeder_to_single_bus(
        result["network"], result["substation"], result["main_bus"],
        result["base_voltage"], 10, feeder_net, feeder,
    )
    assert feeder.NormalEnergizingSubstation is result["substation"]
    assert feeder in result["substation"].NormalEnergizedFeeder


def test_add_feeder_breaker_has_base_voltage(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "Sub1", 115000)
    feeder, feeder_net = minimal_feeder

    bay = add_feeder_to_single_bus(
        result["network"], result["substation"], result["main_bus"],
        result["base_voltage"], 10, feeder_net, feeder,
    )
    assert bay["breaker"].BaseVoltage is result["base_voltage"]


def test_add_branch_wires_terminal(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "Sub1", 115000)

    terminal = cim.Terminal(name="branch_t1")
    terminal.uuid(name="branch_t1")

    bay = add_branch_to_single_bus(
        result["network"], result["substation"], result["main_bus"],
        result["base_voltage"], 20, terminal,
    )
    assert set(bay) == {"breaker", "disconnector", "junctions"}
    assert terminal.ConnectivityNode is bay["junctions"][1]


def test_two_feeders_independent(tmp_xml, minimal_feeder, tmp_path):
    cim = get_cim()
    from cimgraph.databases import XMLFile
    from cimgraph.models import FeederModel

    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "Sub1", 115000)

    feeder1, feeder_net1 = minimal_feeder

    feeder2 = cim.Feeder(mRID="FEEDER-002")
    feeder2.name = "feeder2"
    path2 = tmp_path / "feeder2.xml"
    feeder_net2 = FeederModel(connection=XMLFile(filename=str(path2)),
                              container=feeder2, distributed=False)
    src2 = cim.ConnectivityNode(name="sourcebus")
    src2.ConnectivityNodeContainer = feeder2
    feeder_net2.add_to_graph(src2)
    es2 = cim.EnergySource(name="src2")
    es2.EquipmentContainer = feeder2
    t2 = cim.Terminal(name="src2_t1", sequenceNumber=1)
    t2.ConnectivityNode = src2
    t2.ConductingEquipment = es2
    es2.Terminals.append(t2)
    feeder_net2.add_to_graph(es2)
    feeder_net2.add_to_graph(t2)
    feeder2.NormalHeadTerminal = t2
    feeder_net2.add_to_graph(feeder2)

    bay1 = add_feeder_to_single_bus(
        result["network"], result["substation"], result["main_bus"],
        result["base_voltage"], 10, feeder_net1, feeder1,
    )
    bay2 = add_feeder_to_single_bus(
        result["network"], result["substation"], result["main_bus"],
        result["base_voltage"], 20, feeder_net2, feeder2,
    )

    assert bay1["breaker"].name != bay2["breaker"].name
    assert len(result["substation"].NormalEnergizedFeeder) == 2
