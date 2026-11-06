import pytest
import cimprofiles.cim18.cim18v17 as cim
from cimtables.units import Qty

from cimbuilder.object_builder.transformer import PowerTransformerBuilder


def test_power_transformer_add_connectivity(network, container):
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    builder.add_connectivity(xfmr)
    assert xfmr.EquipmentContainer is container


def test_power_transformer_add_power_transformer_end_broken_without_endNumber_set_first(
    network, container, base_voltage
):
    """add_power_transformer_end creates `xfmr_end = cn.PowerTransformerEnd(...)`
    and immediately calls connectivity.add_connectivity(equipment=xfmr_end, ...)
    - but connectivity.add_connectivity's own contract (cimtables/connectivity.py)
    requires a TransformerEnd's PowerTransformer FK and endNumber to already
    be set before that call. This method only calls
    graph_write.set_attr(xfmr_end, CN, "endNumber", endNumber) AFTER
    add_connectivity, and never sets xfmr_end.PowerTransformer at all - so
    this raises for every call, independent of connectionKind or any other
    argument. (connectionKind also isn't wrapped in cn.WindingConnection(...)
    the way by_template.py's add_phase_end wraps `phase` - a second,
    unreachable bug behind this one.)"""
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    builder.add_connectivity(xfmr)

    with pytest.raises(ValueError, match="PowerTransformer"):
        builder.add_power_transformer_end(
            xfmr, node="bus1", endNumber=1, BaseVoltage=base_voltage.mRID
        )


def test_power_transformer_add_electrical(network, container):
    """add_electrical operates directly on an already-built
    PowerTransformerEnd - exercised here via a manually constructed end,
    since add_power_transformer_end (the method meant to build one) is
    itself broken (see the test above)."""
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr_end = cim.PowerTransformerEnd(mRID="xfmr1_end1", endNumber=1)
    network.add_to_graph(xfmr_end)

    builder.add_electrical(
        xfmr_end, r=Qty(1, "ohm"), x=Qty(5, "ohm"), ratedS=Qty(1, "MVA"), ratedU=Qty(12.47, "kV")
    )
    assert float(xfmr_end.r.to("ohm")) == 1


def test_power_transformer_add_mesh_impedance(network, container):
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    end1 = cim.PowerTransformerEnd(mRID="end1", endNumber=1)
    end2 = cim.PowerTransformerEnd(mRID="end2", endNumber=2)
    network.add_to_graph(end1)
    network.add_to_graph(end2)

    xfmr, mesh = builder.add_mesh_impedance(
        xfmr, FromTransformerEnd="end1", ToTransformerEnd="end2", r=Qty(1, "ohm"), x=Qty(5, "ohm")
    )
    assert float(mesh.r.to("ohm")) == 1


def test_power_transformer_add_short_circuit_wrong_profile_part_module(network, container):
    """add_short_circuit calls graph_write.set_attr(xfmr_end, EL_BAL, "r0",
    r0) (and x0/b0/g0) - EL_BAL (electrical_balanced).PowerTransformerEnd
    has no r0/x0/b0/g0 fields at all (only the positive-sequence r/x/b/g,
    already written by add_electrical). Those zero-sequence fields exist
    on SC (short_circuit).PowerTransformerEnd instead - this is the wrong
    profile-part module for every call, unconditionally."""
    builder = PowerTransformerBuilder(network=network, container=container)
    xfmr_end = cim.PowerTransformerEnd(mRID="xfmr1_end1", endNumber=1)
    network.add_to_graph(xfmr_end)

    with pytest.raises(ValueError, match="r0"):
        builder.add_short_circuit(xfmr_end, r0=Qty(1, "ohm"), x0=Qty(5, "ohm"))
