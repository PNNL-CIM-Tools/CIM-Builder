"""Tests for topology_builder.main_and_transfer."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.topology_builder.main_and_transfer import (
    new_main_and_transfer_substation,
    add_feeder_to_main_and_transfer,
    add_branch_to_main_and_transfer,
)


def test_creation_returns_correct_keys(tmp_xml):
    _, conn = tmp_xml
    result = new_main_and_transfer_substation(conn, "MTSub", 115000)
    assert set(result) == {"network", "substation", "main_bus", "transfer_bus", "base_voltage"}


def test_both_buses_in_graph(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_main_and_transfer_substation(conn, "MTSub", 115000)
    net = result["network"]
    nodes = list(net.graph.get(cim.ConnectivityNode, {}).values())
    assert result["main_bus"] in nodes
    assert result["transfer_bus"] in nodes


def test_bus_tie_breaker_created(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_main_and_transfer_substation(conn, "MTSub", 115000)
    net = result["network"]
    net.get_all_edges(cim.Breaker)
    assert cim.Breaker in net.graph


def test_add_feeder_transfer_disconnector_normally_open(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_main_and_transfer_substation(conn, "MTSub", 115000)
    feeder, feeder_net = minimal_feeder

    bay = add_feeder_to_main_and_transfer(
        result["network"], result["substation"],
        result["main_bus"], result["transfer_bus"],
        result["base_voltage"], 10, feeder_net, feeder,
    )
    ag3 = bay["disconnectors"][2]
    assert ag3.normalOpen is True
    assert ag3.open is True


def test_add_feeder_three_disconnectors(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_main_and_transfer_substation(conn, "MTSub2", 115000)
    feeder, feeder_net = minimal_feeder

    bay = add_feeder_to_main_and_transfer(
        result["network"], result["substation"],
        result["main_bus"], result["transfer_bus"],
        result["base_voltage"], 10, feeder_net, feeder,
    )
    assert len(bay["disconnectors"]) == 3
    assert len(bay["junctions"]) == 2


def test_add_feeder_links_to_substation(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_main_and_transfer_substation(conn, "MTSub3", 115000)
    feeder, feeder_net = minimal_feeder

    add_feeder_to_main_and_transfer(
        result["network"], result["substation"],
        result["main_bus"], result["transfer_bus"],
        result["base_voltage"], 10, feeder_net, feeder,
    )
    assert feeder.NormalEnergizingSubstation is result["substation"]


def test_add_branch_wires_terminal(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_main_and_transfer_substation(conn, "MTSub", 115000)

    terminal = cim.Terminal(name="branch_t1")
    terminal.uuid(name="branch_t1")

    bay = add_branch_to_main_and_transfer(
        result["network"], result["substation"],
        result["main_bus"], result["transfer_bus"],
        result["base_voltage"], 20, terminal,
    )
    assert terminal.ConnectivityNode is bay["junctions"][2]
    assert len(bay["disconnectors"]) == 3
