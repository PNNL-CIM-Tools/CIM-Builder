"""Tests for topology_builder.ring_bus."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.topology_builder.ring_bus import (
    new_ring_bus_substation,
    add_feeder_to_ring_bus,
    add_branch_to_ring_bus,
)


def test_creation_returns_correct_keys(tmp_xml):
    _, conn = tmp_xml
    result = new_ring_bus_substation(conn, "RingSub", 115000)
    assert set(result) == {"network", "substation", "buses", "base_voltage"}


def test_default_four_sections(tmp_xml):
    _, conn = tmp_xml
    result = new_ring_bus_substation(conn, "RingSub", 115000)
    assert len(result["buses"]) == 4


def test_custom_section_count(tmp_xml):
    _, conn = tmp_xml
    result = new_ring_bus_substation(conn, "RingSub6", 115000, total_sections=6)
    assert len(result["buses"]) == 6


def test_ring_breakers_created(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_ring_bus_substation(conn, "RingSub", 115000, total_sections=4)
    net = result["network"]
    net.get_all_edges(cim.Breaker)
    # 4 ring-section breakers
    assert len(net.graph.get(cim.Breaker, {})) >= 4


def test_add_feeder_links_substation(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_ring_bus_substation(conn, "RingSub", 115000)
    feeder, feeder_net = minimal_feeder

    add_feeder_to_ring_bus(
        result["network"], result["substation"], result["buses"],
        result["base_voltage"], 1, feeder_net, feeder,
    )
    assert feeder.NormalEnergizingSubstation is result["substation"]
    assert feeder in result["substation"].NormalEnergizedFeeder


def test_add_feeder_returns_disconnector(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    result = new_ring_bus_substation(conn, "RingSub", 115000)
    feeder, feeder_net = minimal_feeder

    bay = add_feeder_to_ring_bus(
        result["network"], result["substation"], result["buses"],
        result["base_voltage"], 2, feeder_net, feeder,
    )
    assert "disconnector" in bay


def test_add_branch_wires_terminal(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    result = new_ring_bus_substation(conn, "RingSub", 115000)

    terminal = cim.Terminal(name="branch_t1")
    terminal.uuid(name="branch_t1")

    bay = add_branch_to_ring_bus(
        result["network"], result["substation"], result["buses"],
        result["base_voltage"], 3, terminal,
    )
    assert "junction" in bay
    assert terminal.ConnectivityNode is bay["junction"]
