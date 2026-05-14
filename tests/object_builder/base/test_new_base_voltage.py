"""Tests for cimbuilder.object_builder.base.new_base_voltage."""
from __future__ import annotations

from cimgraph.databases import XMLFile
from cimgraph.models import DistributedArea

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.base.new_base_voltage import new_base_voltage


def test_basic(tmp_path):
    cim = get_cim()
    sub = cim.Substation(name="s")
    sub.uuid(name="s")
    net = DistributedArea(
        connection=XMLFile(filename=str(tmp_path / "x.xml")),
        container=sub, distributed=False,
    )
    net.add_to_graph(sub)

    bv = new_base_voltage(net, 13.8)
    assert isinstance(bv, cim.BaseVoltage)
    assert bv.name == "BaseV_13.8kV"
    assert isinstance(bv.nominalVoltage, cim.Voltage)
    assert float(bv.nominalVoltage) == 13_800
    assert bv in net.graph.get(cim.BaseVoltage, {}).values()


def test_custom_name(tmp_path):
    cim = get_cim()
    sub = cim.Substation(name="s")
    sub.uuid(name="s")
    net = DistributedArea(
        connection=XMLFile(filename=str(tmp_path / "x.xml")),
        container=sub, distributed=False,
    )
    net.add_to_graph(sub)

    bv = new_base_voltage(net, 230, name="HV_230kV")
    assert bv.name == "HV_230kV"
    assert float(bv.nominalVoltage) == 230_000
