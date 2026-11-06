import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.transformer import TransformerTankConfigurationBuilder


def test_add_nameplate(network, container):
    builder = TransformerTankConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="config1")

    builder.add_nameplate(
        config,
        percentImpedance=Qty(2.5, "percent"),
        percentMagnetizingCurrent=Qty(0.5, "percent"),
        noLoadLoss=Qty(500, "W"),
        loadLoss=Qty(2, "kW"),
    )
    assert float(config.loadLoss.to("kW")) == 2


def test_add_phase_end(network, container):
    builder = TransformerTankConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="config1")

    end = builder.add_phase_end(
        config, mRID="config1_end1_A", endNumber=1, sequenceNumber=1, phase="A"
    )
    assert end.TankConfiguration is config


def test_add_winding_with_absolute_r(network, container):
    builder = TransformerTankConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="config1")

    winding = builder.add_winding(
        config,
        mRID="winding1",
        ratedS=Qty(100, "kVA"),
        ratedU=Qty(12.47, "kV"),
        baseS=Qty(100, "kVA"),
        baseU=Qty(12.47, "kV"),
        r=Qty(1, "ohm"),
    )
    assert float(winding.r.to("ohm")) == 1


def test_add_winding_with_relative_r_calls_z_base_with_wrong_arity(network, container):
    """When r is a relative Qty (pu/percent), add_winding calls
    graph_write.set_attr(winding, EL_BAL, 'r', r,
    z_base=impedance.z_base(winding, [], self.network.base_power)) - two
    bugs stacked: impedance.z_base's real signature is
    z_base(obj, system_base, *, on_system_base=False), taking exactly 2
    positional args, but this call passes 3 (winding, [], base_power) -
    raises TypeError before set_attr is ever reached, so its own
    separate z_base= (vs. the real system_base=) kwarg bug on set_attr is
    unreachable. Absolute r values skip this branch entirely (see the
    test above)."""
    builder = TransformerTankConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="config1")

    with pytest.raises(TypeError, match="z_base"):
        builder.add_winding(
            config,
            mRID="winding1",
            baseS=Qty(100, "kVA"),
            baseU=Qty(12.47, "kV"),
            r=Qty(2, "percent"),
        )


def test_add_mesh_impedance_with_absolute_x(network, container):
    builder = TransformerTankConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="config1")
    w1 = builder.add_winding(
        config, mRID="w1", baseS=Qty(100, "kVA"), baseU=Qty(12.47, "kV"), r=Qty(1, "ohm")
    )
    w2 = builder.add_winding(
        config, mRID="w2", baseS=Qty(100, "kVA"), baseU=Qty(12.47, "kV"), r=Qty(1, "ohm")
    )

    mesh = builder.add_mesh_impedance(FromWinding="w1", ToWinding="w2", x=Qty(5, "ohm"))
    assert float(mesh.x.to("ohm")) == 5


def test_add_mesh_impedance_with_relative_x_calls_z_base_with_wrong_arity(network, container):
    """Same bug as test_add_winding_with_relative_r_calls_z_base_with_wrong_arity:
    impedance.z_base(mesh, [from_winding], self.network.base_power) passes
    3 positional args to a 2-positional-arg function."""
    builder = TransformerTankConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="config1")
    w1 = builder.add_winding(
        config, mRID="w1", baseS=Qty(100, "kVA"), baseU=Qty(12.47, "kV"), r=Qty(1, "ohm")
    )
    w2 = builder.add_winding(
        config, mRID="w2", baseS=Qty(100, "kVA"), baseU=Qty(12.47, "kV"), r=Qty(1, "ohm")
    )

    with pytest.raises(TypeError, match="z_base"):
        builder.add_mesh_impedance(FromWinding="w1", ToWinding="w2", x=Qty(2, "percent"))


def test_add_mesh_impedance_requires_existing_windings(network, container):
    builder = TransformerTankConfigurationBuilder(network=network, container=container)
    builder.create(mRID="config1")

    with pytest.raises(ValueError, match="not both found"):
        builder.add_mesh_impedance(FromWinding="missing1", ToWinding="missing2", x=Qty(5, "ohm"))
