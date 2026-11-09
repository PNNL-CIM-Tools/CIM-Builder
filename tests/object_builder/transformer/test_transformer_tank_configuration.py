import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.transformer import TransformerTankConfigurationBuilder


@pytest.fixture
def builder(network, container):
    return TransformerTankConfigurationBuilder(network=network, container=container)


@pytest.fixture
def config(builder):
    return builder.create(mRID="ct_25kVA")


def test_add_electrical(builder, config):
    builder.add_electrical(
        config,
        loadLoss=Qty(0.3, "kW"),
        noLoadLoss=Qty(0.1, "kW"),
        percentImpedance=1.8,
        percentMagnetizingCurrent=0.5,
    )
    assert float(config.loadLoss.to("W")) == pytest.approx(300)
    assert float(config.noLoadLoss.to("W")) == pytest.approx(100)
    assert float(config.percentImpedance) == pytest.approx(1.8)
    assert float(config.percentMagnetizingCurrent) == pytest.approx(0.5)


def test_add_transformer_phase_end(network, builder, config):
    _, phase_end = builder.add_transformer_phase_end(
        config, endNumber=2, sequenceNumber=1, phase="s1", phaseNeutralU=Qty(120, "V")
    )
    assert phase_end.mRID == "ct_25kVA_end_2_seq_1"
    assert phase_end.endNumber == 2
    assert phase_end.sequenceNumber == 1
    assert phase_end.phase == network.cim.SinglePhaseKind("s1")
    assert float(phase_end.phaseNeutralU.to("V")) == pytest.approx(120)
    assert phase_end.TankConfiguration is config
    assert phase_end in config.TransformerPhaseEnd
    assert network.find_by_mRID("ct_25kVA_end_2_seq_1") is phase_end


def test_add_transformer_lug(builder, config):
    _, phase_end = builder.add_transformer_phase_end(
        config, endNumber=1, sequenceNumber=1, phase="A"
    )
    _, lug = builder.add_transformer_lug(
        config, designation="H1", sequenceNumber=1, TransformerEnd=phase_end.mRID
    )
    assert lug.designation == "H1"
    assert lug.TankConfiguration is config
    assert lug.TransformerEnd is phase_end


def test_add_transformer_lug_floating(builder, config):
    _, lug = builder.add_transformer_lug(config, designation="H2", sequenceNumber=2)
    assert lug.TransformerEnd is None
    assert lug.TankConfiguration is config


def test_add_transformer_core(network, builder, config):
    _, core = builder.add_transformer_core(
        config, form="shellForm", b=Qty(1e-6, "S"), g=Qty(2e-6, "S")
    )
    assert core.form == network.cim.CoreConstructionKind("shellForm")
    assert float(core.b.to("S")) == pytest.approx(1e-6)
    assert config.TransformerCore is core


def test_add_transformer_winding(network, builder, config):
    builder.add_transformer_lug(config, designation="H1", sequenceNumber=1)
    builder.add_transformer_lug(config, designation="H2", sequenceNumber=2)
    _, core = builder.add_transformer_core(config, form="coreForm")

    _, winding = builder.add_transformer_winding(
        config,
        FromTransformerLug="ct_25kVA_lug_h1",
        ToTransformerLug="ct_25kVA_lug_h2",
        TransformerCore=core.mRID,
        connection="I",
        baseS=Qty(25, "kVA"),
        baseU=Qty(7.2, "kV"),
        r=Qty(1, "percent"),
    )
    assert winding.mRID == "ct_25kVA_wdg_h1h2"
    assert winding.connection == network.cim.PhaseShuntConnectionKind("I")
    assert winding.FromTransformerLug.designation == "H1"
    assert winding.ToTransformerLug.designation == "H2"
    assert winding.TransformerCore is core
    assert winding.TankConfiguration is config
    # 1% of (7200 V)^2 / 25 kVA
    assert float(winding.r.to("ohm")) == pytest.approx(0.01 * 7200**2 / 25e3)


def test_add_transformer_winding_missing_lug(builder, config):
    builder.add_transformer_lug(config, designation="H1", sequenceNumber=1)
    with pytest.raises(ValueError, match="not both found"):
        builder.add_transformer_winding(
            config,
            FromTransformerLug="ct_25kVA_lug_h1",
            ToTransformerLug="no_such_lug",
            connection="I",
        )


def test_split_phase_mesh_impedance(builder, config):
    """Center-tapped 7.2kV / 120-240V tank: one primary coil and two
    secondary half-coils, mesh impedance from primary to each half."""
    _, h_end = builder.add_transformer_phase_end(config, endNumber=1, sequenceNumber=1, phase="A")
    _, x_end = builder.add_transformer_phase_end(config, endNumber=2, sequenceNumber=1, phase="s1")
    for seq, designation in enumerate(["H1", "H2"], start=1):
        builder.add_transformer_lug(
            config, designation=designation, sequenceNumber=seq, TransformerEnd=h_end.mRID
        )
    for seq, designation in enumerate(["X1", "X2", "X3"], start=1):
        builder.add_transformer_lug(
            config, designation=designation, sequenceNumber=seq, TransformerEnd=x_end.mRID
        )
    _, primary = builder.add_transformer_winding(
        config,
        FromTransformerLug="ct_25kVA_lug_h1",
        ToTransformerLug="ct_25kVA_lug_h2",
        connection="I",
        baseS=Qty(25, "kVA"),
        baseU=Qty(7.2, "kV"),
    )
    _, half1 = builder.add_transformer_winding(
        config,
        FromTransformerLug="ct_25kVA_lug_x1",
        ToTransformerLug="ct_25kVA_lug_x2",
        connection="I",
    )
    _, mesh = builder.add_mesh_impedance(
        config,
        FromTransformerEnd=h_end.mRID,
        ToTransformerEnd=x_end.mRID,
        FromWinding=primary.mRID,
        ToWinding=half1.mRID,
        r=Qty(1, "percent"),
        x=Qty(2, "percent"),
    )
    assert len(config.TransformerWinding) == 2
    assert len(config.TransformerLugs) == 5
    assert mesh.FromWinding is primary
    assert mesh.ToWinding is half1
    assert mesh.FromTransformerEnd is h_end
    assert mesh in primary.FromMeshImpedance
    assert mesh.mRID == f"{config.mRID}_mesh_h1h2x1x2"
    # pu base comes from the From winding
    z_base = 7200**2 / 25e3
    assert float(mesh.r.to("ohm")) == pytest.approx(0.01 * z_base)
    assert float(mesh.x.to("ohm")) == pytest.approx(0.02 * z_base)
