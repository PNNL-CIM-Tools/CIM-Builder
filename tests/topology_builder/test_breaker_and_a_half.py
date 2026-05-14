"""Tests for topology_builder.breaker_and_a_half."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.topology_builder.breaker_and_a_half import (
    new_breaker_and_half_substation,
    add_feeder_to_breaker_and_half,
    add_branch_to_breaker_and_half,
)


def test_creation_returns_correct_keys(tmp_xml):
    _, conn = tmp_xml
    result = new_breaker_and_half_substation(conn, "BahSub", 115000)
    assert set(result) == {"network", "substation", "main_bus_1", "main_bus_2",
                           "bus_tie_junctions", "base_voltage"}


def test_two_main_buses(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_breaker_and_half_substation(conn, "BahSub", 115000)
    net = result["network"]
    nodes = list(net.graph.get(cim.ConnectivityNode, {}).values())
    assert result["main_bus_1"] in nodes
    assert result["main_bus_2"] in nodes


def test_default_two_bus_ties(tmp_xml):
    _, conn = tmp_xml
    result = new_breaker_and_half_substation(conn, "BahSub", 115000)
    assert len(result["bus_tie_junctions"]) == 2


def test_each_tie_has_eight_junctions(tmp_xml):
    _, conn = tmp_xml
    result = new_breaker_and_half_substation(conn, "BahSub", 115000)
    for junctions in result["bus_tie_junctions"]:
        assert len(junctions) == 8


def test_bus_tie_breakers_created(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_breaker_and_half_substation(conn, "BahSub", 115000, total_bus_ties=2)
    net = result["network"]
    net.get_all_edges(cim.Breaker)
    # 3 breakers per tie × 2 ties = 6 bus-tie breakers
    assert len(net.graph.get(cim.Breaker, {})) >= 6


def test_add_feeder_links_substation(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_breaker_and_half_substation(conn, "BahSub", 115000)
    feeder, feeder_net = minimal_feeder

    add_feeder_to_breaker_and_half(
        result["network"], result["substation"],
        result["bus_tie_junctions"], result["base_voltage"],
        1, 0, feeder_net, feeder,
    )
    assert feeder.NormalEnergizingSubstation is result["substation"]
    assert feeder in result["substation"].NormalEnergizedFeeder


def test_add_feeder_returns_disconnector(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_breaker_and_half_substation(conn, "BahSub", 115000)
    feeder, feeder_net = minimal_feeder

    bay = add_feeder_to_breaker_and_half(
        result["network"], result["substation"],
        result["bus_tie_junctions"], result["base_voltage"],
        2, 0, feeder_net, feeder,
    )
    assert "disconnector" in bay


def test_add_branch_wires_terminal(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_breaker_and_half_substation(conn, "BahSub", 115000)

    terminal = cim.Terminal(name="branch_t1")
    terminal.uuid(name="branch_t1")

    bay = add_branch_to_breaker_and_half(
        result["network"], result["substation"],
        result["bus_tie_junctions"], result["base_voltage"],
        1, 0, terminal,
    )
    assert "junction" in bay
    assert terminal.ConnectivityNode is bay["junction"]
