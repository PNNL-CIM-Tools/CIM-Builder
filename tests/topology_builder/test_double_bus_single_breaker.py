"""Tests for topology_builder.double_bus_single_breaker."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.topology_builder.double_bus_single_breaker import (
    new_double_bus_single_breaker_substation,
    add_feeder_to_double_bus_single_breaker,
    add_branch_to_double_bus_single_breaker,
)


def test_creation_returns_correct_keys(tmp_xml):
    _, conn = tmp_xml
    result = new_double_bus_single_breaker_substation(conn, "DBSub", 115000)
    assert set(result) == {"network", "substation", "north_bus", "south_bus", "base_voltage"}


def test_both_buses_in_graph(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_double_bus_single_breaker_substation(conn, "DBSub", 115000)
    net = result["network"]
    nodes = list(net.graph.get(cim.ConnectivityNode, {}).values())
    assert result["north_bus"] in nodes
    assert result["south_bus"] in nodes


def test_bus_tie_breaker_created(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_double_bus_single_breaker_substation(conn, "DBSub", 115000)
    net = result["network"]
    net.get_all_edges(cim.Breaker)
    assert cim.Breaker in net.graph
    assert len(net.graph[cim.Breaker]) >= 1


def test_add_feeder_even_breaker_north_normally_open(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_double_bus_single_breaker_substation(conn, "DBSub", 115000)
    feeder, feeder_net = minimal_feeder

    bay = add_feeder_to_double_bus_single_breaker(
        result["network"], result["substation"],
        result["north_bus"], result["south_bus"],
        result["base_voltage"], 10, feeder_net, feeder,
    )
    ag1, ag2 = bay["disconnectors"]
    assert ag1.normalOpen is True   # even breaker_number → north normally open
    assert not getattr(ag2, "normalOpen", False)


def test_add_feeder_odd_breaker_south_normally_open(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_double_bus_single_breaker_substation(conn, "DBSub2", 115000)
    feeder, feeder_net = minimal_feeder

    bay = add_feeder_to_double_bus_single_breaker(
        result["network"], result["substation"],
        result["north_bus"], result["south_bus"],
        result["base_voltage"], 11, feeder_net, feeder,
    )
    ag1, ag2 = bay["disconnectors"]
    assert ag2.normalOpen is True   # odd breaker_number → south normally open
    assert not getattr(ag1, "normalOpen", False)


def test_add_branch_returns_correct_keys(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_double_bus_single_breaker_substation(conn, "DBSub", 115000)

    terminal = cim.Terminal(name="branch_t1")
    terminal.uuid(name="branch_t1")

    bay = add_branch_to_double_bus_single_breaker(
        result["network"], result["substation"],
        result["north_bus"], result["south_bus"],
        result["base_voltage"], 20, terminal,
    )
    assert "breaker" in bay
    assert len(bay["disconnectors"]) == 3
    assert len(bay["junctions"]) == 3
    assert terminal.ConnectivityNode is bay["junctions"][2]
