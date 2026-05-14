"""Tests for cimbuilder.object_builder.transformer.new_power_transformer."""
from __future__ import annotations

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.transformer.new_power_transformer import new_power_transformer


def test_basic(simple_substation_network):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    xfmr = new_power_transformer(net, sub, "T1")
    assert isinstance(xfmr, cim.PowerTransformer)
    assert xfmr.name == "T1"
    assert xfmr.EquipmentContainer is sub


def test_optional_fields(simple_substation_network):
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    xfmr = new_power_transformer(
        net, sub, "T2",
        vector_group="Dyn11",
        is_part_of_generator_unit=False,
    )
    assert xfmr.vectorGroup == "Dyn11"
    assert xfmr.isPartOfGeneratorUnit is False


def test_added_to_graph(simple_substation_network):
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    xfmr = new_power_transformer(net, sub, "T3")
    assert xfmr in net.graph.get(cim.PowerTransformer, {}).values()


def test_template_no_op(simple_substation_network):
    """template= is accepted but not yet consumed (Phase 6 stub)."""
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    fake = cim.PowerTransformerInfo(name="HVMV_69_12")
    xfmr = new_power_transformer(net, sub, "T4", template=fake)
    assert isinstance(xfmr, cim.PowerTransformer)
