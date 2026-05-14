"""Tests for topology_builder.sectionalized_bus."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.topology_builder.sectionalized_bus import (
    new_sectionalized_bus_substation,
    add_feeder_to_sectionalized_bus,
    add_branch_to_sectionalized_bus,
)


def test_creation_returns_correct_keys(tmp_xml):
    _, conn = tmp_xml
    result = new_sectionalized_bus_substation(conn, "SecSub", 115000)
    assert set(result) == {"network", "substation", "buses", "base_voltage"}


def test_default_two_sections(tmp_xml):
    _, conn = tmp_xml
    result = new_sectionalized_bus_substation(conn, "SecSub", 115000)
    assert len(result["buses"]) == 2


def test_custom_section_count(tmp_xml):
    _, conn = tmp_xml
    result = new_sectionalized_bus_substation(conn, "SecSub3", 115000, total_sections=3)
    assert len(result["buses"]) == 3


def test_n_minus_one_bus_ties(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_sectionalized_bus_substation(conn, "SecSub3", 115000, total_sections=3)
    net = result["network"]
    net.get_all_edges(cim.Breaker)
    # 2 bus-tie breakers for 3 sections
    assert len(net.graph.get(cim.Breaker, {})) >= 2


def test_add_feeder_to_section1(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_sectionalized_bus_substation(conn, "SecSub", 115000)
    feeder, feeder_net = minimal_feeder

    bay = add_feeder_to_sectionalized_bus(
        result["network"], result["substation"], result["buses"],
        result["base_voltage"], 1, 10, feeder_net, feeder,
    )
    assert set(bay) == {"breaker", "disconnectors", "junctions"}
    assert feeder.NormalEnergizingSubstation is result["substation"]


def test_add_feeder_two_disconnectors(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_sectionalized_bus_substation(conn, "SecSub", 115000)
    feeder, feeder_net = minimal_feeder

    bay = add_feeder_to_sectionalized_bus(
        result["network"], result["substation"], result["buses"],
        result["base_voltage"], 2, 20, feeder_net, feeder,
    )
    assert len(bay["disconnectors"]) == 2
    assert len(bay["junctions"]) == 2


def test_add_branch_wires_terminal(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_sectionalized_bus_substation(conn, "SecSub", 115000)

    terminal = cim.Terminal(name="branch_t1")
    terminal.uuid(name="branch_t1")

    bay = add_branch_to_sectionalized_bus(
        result["network"], result["substation"], result["buses"],
        result["base_voltage"], 1, 30, terminal,
    )
    assert terminal.ConnectivityNode is bay["junctions"][1]
