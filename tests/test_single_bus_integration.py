"""Integration tests for single-bus substation using the functional topology API."""
from __future__ import annotations

import pytest

from cimbuilder._profile import get_cim
from cimbuilder.topology_builder.single_bus import (
    new_single_bus_substation,
    add_feeder_to_single_bus,
    add_branch_to_single_bus,
)


def test_creation_structure(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "test_single_bus_sub", 115000)

    assert "network" in result
    assert "substation" in result
    assert "main_bus" in result
    assert "base_voltage" in result

    assert result["substation"].name == "test_single_bus_sub"
    assert isinstance(result["substation"], cim.Substation)
    assert result["main_bus"].name == "test_single_bus_sub_main_bus"
    assert isinstance(result["main_bus"], cim.ConnectivityNode)
    assert result["main_bus"].ConnectivityNodeContainer is result["substation"]
    assert isinstance(result["base_voltage"], cim.BaseVoltage)

    net = result["network"]
    net.get_all_edges(cim.BusbarSection)
    assert cim.BusbarSection in net.graph
    assert len(net.graph[cim.BusbarSection]) > 0


def test_add_feeder_topology(tmp_xml, minimal_feeder):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "test_sub_with_feeder", 115000)
    feeder, feeder_network = minimal_feeder

    bay = add_feeder_to_single_bus(
        result["network"], result["substation"], result["main_bus"],
        result["base_voltage"], 10, feeder_network, feeder,
    )

    assert "breaker" in bay
    assert "disconnectors" in bay
    assert "junctions" in bay

    assert isinstance(bay["breaker"], cim.Breaker)
    assert bay["breaker"].BaseVoltage is result["base_voltage"]
    assert len(bay["disconnectors"]) == 2
    assert all(isinstance(d, cim.Disconnector) for d in bay["disconnectors"])
    assert len(bay["junctions"]) == 2

    assert feeder.NormalEnergizingSubstation is result["substation"]
    assert feeder in result["substation"].NormalEnergizedFeeder


def test_multiple_feeders(tmp_xml, minimal_feeder, tmp_path):
    cim = get_cim()
    from cimgraph.databases import XMLFile
    from cimgraph.models import FeederModel

    _, conn = tmp_xml
    result = new_single_bus_substation(conn, "test_multi_feeder_sub", 115000)

    feeder1, feeder_net1 = minimal_feeder

    feeder2 = cim.Feeder(mRID="TEST-FEEDER-002")
    feeder2.name = "feeder2"
    path2 = tmp_path / "feeder2.xml"
    feeder_net2 = FeederModel(connection=XMLFile(filename=str(path2)),
                              container=feeder2, distributed=False)
    src2 = cim.ConnectivityNode(name="sourcebus")
    src2.ConnectivityNodeContainer = feeder2
    feeder_net2.add_to_graph(src2)
    es2 = cim.EnergySource(name="source2")
    es2.EquipmentContainer = feeder2
    t2 = cim.Terminal(name="source2_t1", sequenceNumber=1)
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

    assert len(result["substation"].NormalEnergizedFeeder) >= 2
    assert feeder1 in result["substation"].NormalEnergizedFeeder
    assert feeder2 in result["substation"].NormalEnergizedFeeder
    assert bay1["breaker"].name != bay2["breaker"].name


@pytest.mark.xfail(
    reason="cim-graph write_xml missing namespace for cimhub_2026 draft URI (cim-graph bug)",
    strict=False,
)
def test_export_to_xml(tmp_xml, minimal_feeder):
    path, conn = tmp_xml
    result = new_single_bus_substation(conn, "test_export_sub", 115000)
    feeder, feeder_network = minimal_feeder

    add_feeder_to_single_bus(
        result["network"], result["substation"], result["main_bus"],
        result["base_voltage"], 10, feeder_network, feeder,
    )

    result["network"].upload()

    assert path.exists()
    assert path.stat().st_size > 0
    content = path.read_text()
    assert "test_export_sub" in content
    assert "Substation" in content


def test_two_substations_are_independent(tmp_path):
    from cimgraph.databases import XMLFile
    conn1 = XMLFile(filename=str(tmp_path / "sub1.xml"))
    conn2 = XMLFile(filename=str(tmp_path / "sub2.xml"))

    result1 = new_single_bus_substation(conn1, "sub1", 115000)
    result2 = new_single_bus_substation(conn2, "sub2", 230000)

    assert result1["substation"] is not result2["substation"]
    assert result1["substation"].name == "sub1"
    assert result2["substation"].name == "sub2"
    assert result1["main_bus"] is not result2["main_bus"]
    assert result1["network"] is not result2["network"]
