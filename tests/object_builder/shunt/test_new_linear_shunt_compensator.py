"""Tests for cimbuilder.object_builder.shunt.new_linear_shunt_compensator."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.shunt.new_linear_shunt_compensator import (
    new_linear_shunt_compensator,
)


def test_basic(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    n1 = connectivity_nodes["node1"]

    cap = new_linear_shunt_compensator(
        net, sub, "CAP1", node=n1,
        b_per_section=1.5e-3,
        nominal_voltage_kV=12.47,
    )

    assert isinstance(cap, cim.LinearShuntCompensator)
    assert cap.name == "CAP1"
    assert cap.EquipmentContainer is sub
    assert isinstance(cap.bPerSection, cim.Susceptance)
    assert float(cap.bPerSection) == 1.5e-3
    assert isinstance(cap.nomU, cim.Voltage)
    assert float(cap.nomU) == 12470.0  # kV → V
    assert cap.sections == 1.0
    assert cap.maximumSections == 1
    assert cap.normalSections == 1
    assert cap.grounded is False

    assert len(cap.Terminals) == 1
    assert cap.Terminals[0].sequenceNumber == 1
    assert cap.Terminals[0].ConnectivityNode is n1


def test_node_by_name(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    cap = new_linear_shunt_compensator(net, sub, "CAP2", node="node1", b_per_section=2e-3)
    assert cap.Terminals[0].ConnectivityNode is connectivity_nodes["node1"]


def test_with_base_voltage(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]
    bv = simple_substation_network["base_voltage"]

    cap = new_linear_shunt_compensator(
        net, sub, "CAP3", node=connectivity_nodes["node1"],
        base_voltage=bv, b_per_section=1e-3,
    )
    assert cap.BaseVoltage is bv


def test_zero_sequence_admittance(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    cap = new_linear_shunt_compensator(
        net, sub, "CAP4", node=connectivity_nodes["node1"],
        b_per_section=1e-3, b0_per_section=2e-4,
        g_per_section=1e-5, g0_per_section=2e-6,
    )
    assert isinstance(cap.b0PerSection, cim.Susceptance)
    assert float(cap.b0PerSection) == 2e-4
    assert isinstance(cap.gPerSection, cim.Conductance)
    assert float(cap.gPerSection) == 1e-5
    assert isinstance(cap.g0PerSection, cim.Conductance)
    assert float(cap.g0PerSection) == 2e-6


def test_sections(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    cap = new_linear_shunt_compensator(
        net, sub, "CAP5", node=connectivity_nodes["node1"],
        b_per_section=1e-3, sections=2, maximum_sections=4, normal_sections=3,
    )
    assert cap.sections == 2.0
    assert cap.maximumSections == 4
    assert cap.normalSections == 3


def test_added_to_graph(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    cap = new_linear_shunt_compensator(
        net, sub, "CAP6", node=connectivity_nodes["node1"], b_per_section=1e-3,
    )
    assert cap in net.graph.get(cim.LinearShuntCompensator, {}).values()
    assert cap.Terminals[0] in net.graph.get(cim.Terminal, {}).values()
