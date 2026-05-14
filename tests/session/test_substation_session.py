"""Tests for session.SubstationSession."""
from __future__ import annotations

import pytest

from cimbuilder._profile import get_cim
from cimbuilder.session import SubstationSession


# ---------------------------------------------------------------------------
# Factory classmethods
# ---------------------------------------------------------------------------

def test_single_bus_factory(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    sess = SubstationSession.single_bus(conn, "Sub1", 115000)

    assert sess.topology == "single_bus"
    assert isinstance(sess.substation, cim.Substation)
    assert sess.substation.name == "Sub1"
    assert isinstance(sess.base_voltage, cim.BaseVoltage)
    assert "main_bus" in sess._buses


def test_double_bus_factory(tmp_xml):
    _, conn = tmp_xml
    sess = SubstationSession.double_bus_single_breaker(conn, "DBSub", 115000)
    assert sess.topology == "double_bus_single_breaker"
    assert "north_bus" in sess._buses
    assert "south_bus" in sess._buses


def test_main_and_transfer_factory(tmp_xml):
    _, conn = tmp_xml
    sess = SubstationSession.main_and_transfer(conn, "MTSub", 115000)
    assert sess.topology == "main_and_transfer"
    assert "main_bus" in sess._buses
    assert "transfer_bus" in sess._buses


def test_ring_bus_factory(tmp_xml):
    _, conn = tmp_xml
    sess = SubstationSession.ring_bus(conn, "RingSub", 115000, total_sections=6)
    assert sess.topology == "ring_bus"
    assert len(sess._buses["buses"]) == 6


def test_sectionalized_bus_factory(tmp_xml):
    _, conn = tmp_xml
    sess = SubstationSession.sectionalized_bus(conn, "SecSub", 115000, total_sections=3)
    assert sess.topology == "sectionalized_bus"
    assert len(sess._buses["buses"]) == 3


def test_breaker_and_half_factory(tmp_xml):
    _, conn = tmp_xml
    sess = SubstationSession.breaker_and_half(conn, "BahSub", 115000, total_bus_ties=2)
    assert sess.topology == "breaker_and_half"
    assert len(sess._buses["bus_tie_junctions"]) == 2


# ---------------------------------------------------------------------------
# add_feeder dispatch
# ---------------------------------------------------------------------------

def test_single_bus_add_feeder(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    sess = SubstationSession.single_bus(conn, "Sub1", 115000)
    feeder, feeder_net = minimal_feeder

    bay = sess.add_feeder(10, feeder_net, feeder)
    assert "breaker" in bay
    assert feeder.NormalEnergizingSubstation is sess.substation


def test_double_bus_add_feeder(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    sess = SubstationSession.double_bus_single_breaker(conn, "DBSub", 115000)
    feeder, feeder_net = minimal_feeder

    bay = sess.add_feeder(10, feeder_net, feeder)
    assert "breaker" in bay


def test_main_and_transfer_add_feeder(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    sess = SubstationSession.main_and_transfer(conn, "MTSub", 115000)
    feeder, feeder_net = minimal_feeder

    bay = sess.add_feeder(10, feeder_net, feeder)
    # Transfer disconnector should be normally open
    assert bay["disconnectors"][2].normalOpen is True


def test_ring_bus_add_feeder_requires_bus_number(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    sess = SubstationSession.ring_bus(conn, "RingSub", 115000)
    feeder, feeder_net = minimal_feeder

    with pytest.raises(ValueError, match="bus_number"):
        sess.add_feeder(10, feeder_net, feeder)


def test_ring_bus_add_feeder_with_bus_number(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    sess = SubstationSession.ring_bus(conn, "RingSub", 115000)
    feeder, feeder_net = minimal_feeder

    bay = sess.add_feeder(10, feeder_net, feeder, bus_number=2)
    assert "disconnector" in bay


def test_sectionalized_bus_add_feeder(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    sess = SubstationSession.sectionalized_bus(conn, "SecSub", 115000)
    feeder, feeder_net = minimal_feeder

    bay = sess.add_feeder(10, feeder_net, feeder, section_number=1)
    assert "breaker" in bay


def test_breaker_and_half_add_feeder(tmp_xml, minimal_feeder):
    _, conn = tmp_xml
    sess = SubstationSession.breaker_and_half(conn, "BahSub", 115000)
    feeder, feeder_net = minimal_feeder

    bay = sess.add_feeder(1, feeder_net, feeder, tie_number=0)
    assert "disconnector" in bay


# ---------------------------------------------------------------------------
# add_branch dispatch
# ---------------------------------------------------------------------------

def test_single_bus_add_branch(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    sess = SubstationSession.single_bus(conn, "Sub1", 115000)

    terminal = cim.Terminal(name="t1")
    terminal.uuid(name="t1")
    bay = sess.add_branch(20, terminal)
    assert terminal.ConnectivityNode is not None


def test_breaker_and_half_add_branch_requires_tie_number(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    sess = SubstationSession.breaker_and_half(conn, "BahSub", 115000)

    terminal = cim.Terminal(name="t1")
    terminal.uuid(name="t1")
    with pytest.raises(ValueError, match="tie_number"):
        sess.add_branch(1, terminal)


# ---------------------------------------------------------------------------
# add_linear_shunt_compensator
# ---------------------------------------------------------------------------

def test_add_shunt_creates_lsc(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    sess = SubstationSession.single_bus(conn, "Sub1", 115000)

    lsc = sess.add_linear_shunt_compensator(30, "Cap1", b_per_section=0.003)
    assert isinstance(lsc, cim.LinearShuntCompensator)
    assert lsc.name == "Cap1"


# ---------------------------------------------------------------------------
# NetworkSession integration
# ---------------------------------------------------------------------------

def test_network_session_multi_substation(tmp_path):
    from cimgraph.databases import XMLFile
    from cimbuilder.session import NetworkSession

    sess1 = SubstationSession.single_bus(
        XMLFile(filename=str(tmp_path / "sub1.xml")), "Sub1", 115000,
    )
    sess2 = SubstationSession.single_bus(
        XMLFile(filename=str(tmp_path / "sub2.xml")), "Sub2", 230000,
    )

    net = NetworkSession()
    net.add_substation(sess1)
    net.add_substation(sess2)

    assert len(net.substations) == 2
    assert net.get_substation("Sub1") is sess1
    assert net.get_substation("Sub2") is sess2
    assert net.get_substation("NonExistent") is None


# ---------------------------------------------------------------------------
# FeederSession
# ---------------------------------------------------------------------------

def test_feeder_session_new(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    from cimbuilder.session import FeederSession
    fs = FeederSession.new(conn, "Feeder1")
    assert fs.feeder.name == "Feeder1"
    assert isinstance(fs.feeder, cim.Feeder)


def test_feeder_session_add_load(tmp_xml):
    cim = get_cim()
    _, conn = tmp_xml
    from cimbuilder.session import FeederSession

    fs = FeederSession.new(conn, "Feeder1")

    node = cim.ConnectivityNode(name="load_bus")
    node.uuid(name="load_bus")
    node.ConnectivityNodeContainer = fs.feeder
    fs.network.add_to_graph(node)

    load = fs.add_energy_consumer("Load1", node, p_kW=500.0)
    assert isinstance(load, cim.EnergyConsumer)


def test_20_line_multi_substation_workflow(tmp_path):
    """A notebook-style multi-substation build using only sessions."""
    cim = get_cim()
    from cimgraph.databases import XMLFile
    from cimbuilder.session import SubstationSession, FeederSession, NetworkSession

    # Build two substations
    sub1 = SubstationSession.single_bus(
        XMLFile(filename=str(tmp_path / "sub1.xml")), "Transmission_115kV", 115000,
    )
    sub2 = SubstationSession.double_bus_single_breaker(
        XMLFile(filename=str(tmp_path / "sub2.xml")), "Distribution_12kV", 12470,
    )

    # Build a feeder with an explicit sourcebus so get_source_bus() can find it
    fs = FeederSession.new(XMLFile(filename=str(tmp_path / "f1.xml")), "Feeder_A")
    sourcebus = cim.ConnectivityNode(name="sourcebus")
    sourcebus.uuid(name="sourcebus")
    sourcebus.ConnectivityNodeContainer = fs.feeder
    fs.network.add_to_graph(sourcebus)
    es = cim.EnergySource(name="src")
    es.EquipmentContainer = fs.feeder
    t = cim.Terminal(name="src_t1", sequenceNumber=1)
    t.ConnectivityNode = sourcebus
    t.ConductingEquipment = es
    es.Terminals.append(t)
    fs.network.add_to_graph(es)
    fs.network.add_to_graph(t)

    # Connect feeder to sub1; sub2 gets it next (NormalEnergizingSubstation is overwritten)
    sub1.add_feeder(10, fs.network, fs.feeder)
    sub2.add_feeder(20, fs.network, fs.feeder)

    # Collect into a network
    network = NetworkSession()
    network.add_substation(sub1)
    network.add_substation(sub2)

    assert len(network.substations) == 2
    assert fs.feeder.NormalEnergizingSubstation in (sub1.substation, sub2.substation)
