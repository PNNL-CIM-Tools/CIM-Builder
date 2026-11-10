import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.line import (
    ConcentricNeutralCableInfoBuilder,
    OverheadWireInfoBuilder,
)


def test_overhead_wire_info(network, container):
    """IEEE 13 556,500 26/7 ACSR"""
    builder = OverheadWireInfoBuilder(network=network, container=container)
    wire = builder.create(mRID="wire_556500_26_7", name="556,500 26/7")
    builder.add_asset_info(
        wire,
        gmr=Qty(0.031, "ft"),
        radius=Qty(0.927 / 2, "in"),
        rAC50=Qty(0.1859, "ohm/mi"),
        ratedCurrent=Qty(730, "A"),
    )
    assert float(wire.gmr.to("ft")) == pytest.approx(0.031)
    assert float(wire.rAC50.to("ohm/mi")) == pytest.approx(0.1859)
    assert float(wire.ratedCurrent.to("A")) == 730


def test_concentric_neutral_cable_info(network, container):
    """IEEE 13 250 kcmil AA, 1/3 neutral"""
    builder = ConcentricNeutralCableInfoBuilder(network=network, container=container)
    cable = builder.create(mRID="cable_cn_250", name="cn_250")
    builder.add_asset_info(
        cable,
        gmr=Qty(0.0171, "ft"),
        radius=Qty(0.567 / 2, "in"),
        rAC25=Qty(0.41, "ohm/mi"),
        diameterOverJacket=Qty(1.29, "in"),
        neutralStrandCount=13,
        neutralStrandRadius=Qty(0.0641 / 2, "in"),
        neutralStrandGmr=Qty(0.00208, "ft"),
        neutralStrandRDC20=Qty(14.8722, "ohm/mi"),
    )
    assert cable.neutralStrandCount == 13
    assert float(cable.diameterOverJacket.to("in")) == pytest.approx(1.29)
    assert float(cable.neutralStrandRDC20.to("ohm/mi")) == pytest.approx(14.8722)
