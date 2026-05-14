"""Tests for cimbuilder.object_builder.line.new_ac_line_segment."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.line.new_ac_line_segment import new_ac_line_segment
from cimbuilder.object_builder.line.new_per_length_sequence_impedance import (
    new_per_length_sequence_impedance,
)


def test_basic_with_total_impedance(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    line = new_ac_line_segment(
        net, sub, "L1",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        length_km=1.0,
        r_ohm=0.1, x_ohm=0.4,
    )
    assert isinstance(line, cim.ACLineSegment)
    assert line.name == "L1"
    assert isinstance(line.length, cim.Length)
    assert float(line.length) == 1000.0  # km → m
    assert isinstance(line.r, cim.Resistance)
    assert float(line.r) == 0.1
    assert isinstance(line.x, cim.Reactance)
    assert float(line.x) == 0.4
    assert len(line.Terminals) == 2


def test_per_length_impedance_reference(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    z = new_per_length_sequence_impedance(net, "Z1", r_ohm_per_km=0.1, x_ohm_per_km=0.4)
    line = new_ac_line_segment(
        net, sub, "L2",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        length_km=2.5,
        per_length_impedance=z,
    )
    assert line.PerLengthImpedance is z


def test_underground_flag(simple_substation_network, connectivity_nodes):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    line = new_ac_line_segment(
        net, sub, "L3",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        length_km=0.5, is_underground=True,
    )
    assert line.isUnderground is True


def test_template_accepted_no_op(simple_substation_network, connectivity_nodes):
    """``template`` is accepted in the signature but is a no-op until Phase 6."""
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    fake_template = cim.OverheadWireInfo(name="ACSR-Turkey")
    line = new_ac_line_segment(
        net, sub, "L4",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        length_km=1.0, template=fake_template,
    )
    assert line.r is None
    assert line.x is None


def test_added_to_graph(simple_substation_network, connectivity_nodes):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    line = new_ac_line_segment(
        net, sub, "L5",
        node1=connectivity_nodes["node1"],
        node2=connectivity_nodes["node2"],
        length_km=1.0, r_ohm=0.1, x_ohm=0.4,
    )
    assert line in net.graph.get(cim.ACLineSegment, {}).values()
