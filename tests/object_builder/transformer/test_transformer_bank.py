import pytest
import cimprofiles.cim18.cim18v17 as cim
from cimtables.units import Qty

from cimbuilder.object_builder.transformer import TransformerBankBuilder


def test_add_connectivity(network, container):
    builder = TransformerBankBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    builder.add_connectivity(xfmr)
    assert xfmr.EquipmentContainer is container


def test_add_power_transformer_end_inherits_broken_super_call(network, container, base_voltage):
    """TransformerBankBuilder.add_power_transformer_end calls
    super().add_power_transformer_end(...) first - PowerTransformerBuilder's
    version is unconditionally broken (see
    test_power_transformer.py::test_power_transformer_add_power_transformer_end_broken_without_endNumber_set_first),
    so this raises before TransformerBankBuilder's own phases/
    TankConfiguration handling is ever reached."""
    builder = TransformerBankBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    builder.add_connectivity(xfmr)

    with pytest.raises(ValueError, match="PowerTransformer"):
        builder.add_power_transformer_end(
            xfmr,
            node="bus1",
            endNumber=1,
            BaseVoltage=base_voltage.mRID,
            phases=None,
            TankConfiguration=None,
        )


def test_add_transformer_tank_wrong_profile_part_module(network, container):
    """add_transformer_tank calls
    graph_write.set_attr(tank, CONSTR, "loadLoss", loadLoss) (and
    noLoadLoss/percentImpedance/percentMagnetizingCurrent) - none of these
    four fields exist on CONSTR.TransformerTank at all; they exist on
    CONSTR.TransformerTankConfiguration instead. Unconditional whenever
    any of these kwargs is passed a non-None value."""
    builder = TransformerBankBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")

    with pytest.raises(ValueError, match="loadLoss"):
        builder.add_transformer_tank(xfmr, TransformerTank="tank1", loadLoss=Qty(1, "kW"))


def test_add_transformer_phase_end_wrong_profile_part_module(network, container):
    """add_transformer_phase_end calls
    graph_write.set_attr(phase_end, CONSTR, "phase", phase) -
    CONSTR.TransformerPhaseEnd has no `phase` field (it lives on
    CN.TransformerPhaseEnd instead); `phase` isn't optional, so this
    raises for every call. This also means add_power_transformer_end's
    own internal per-phase loop (when `phases` is given) would hit this
    too, if it ever got that far."""
    builder = TransformerBankBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")

    with pytest.raises(ValueError, match="phase"):
        builder.add_transformer_phase_end(
            xfmr,
            endNumber=1,
            sequenceNumber=1,
            phase="A",
            phaseNeutralU=None,
            TankConfiguration=None,
            TransformerPhaseEnd=None,
        )


def test_add_transformer_lug(network, container):
    builder = TransformerBankBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    tank = cim.TransformerTank(mRID="tank1")
    network.add_to_graph(tank)
    end = cim.TransformerPhaseEnd(mRID="end1")
    network.add_to_graph(end)

    xfmr, lug = builder.add_transformer_lug(
        xfmr, designation="H1", TransformerTank="tank1", TransformerEnd="end1"
    )
    assert lug.TransformerTank is tank
    assert lug.TransformerEnd is end


def test_add_transformer_core_form_not_wrapped_in_enum(network, container):
    """add_transformer_core calls
    graph_write.set_attr(core, EL_UNBAL, "form", form) with the raw
    string, instead of wrapping it as
    el_unbal.CoreConstructionKind(form). form is a required (non-optional)
    CoreConstructionKind-typed parameter, so this raises for every call."""
    builder = TransformerBankBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")

    with pytest.raises(TypeError, match="CoreConstructionKind"):
        builder.add_transformer_core(xfmr, TransformerTank="tank1", form="coreForm")


def test_add_transformer_winding_connection_not_wrapped_in_enum(network, container):
    """add_transformer_winding calls
    graph_write.set_attr(winding, CONSTR, "connection", connection) with
    the raw string, instead of wrapping it as
    constr.PhaseShuntConnectionKind(connection). connection is a required
    (non-optional) PhaseShuntConnectionKind-typed parameter, so this
    raises for every call - before the deeper, separately-broken
    baseS/baseU/ratedS/ratedU/r/rDC writes (which use CONSTR instead of
    EL_BAL, the profile part that actually has those fields) are ever
    reached."""
    builder = TransformerBankBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    tank = cim.TransformerTank(mRID="tank1")
    network.add_to_graph(tank)
    end = cim.TransformerPhaseEnd(mRID="end1")
    network.add_to_graph(end)
    xfmr, lug1 = builder.add_transformer_lug(
        xfmr, designation="H1", TransformerTank="tank1", TransformerEnd="end1"
    )
    xfmr, lug2 = builder.add_transformer_lug(
        xfmr, designation="X1", TransformerTank="tank1", TransformerEnd="end1"
    )

    with pytest.raises(TypeError, match="PhaseShuntConnectionKind"):
        builder.add_transformer_winding(
            xfmr,
            TransformerTank="tank1",
            FromTransformerLug="tank1_lug_H1",
            ToTransformerLug="tank1_lug_X1",
            connection="Y",
            baseS=Qty(100, "kVA"),
            baseU=Qty(12.47, "kV"),
            ratedS=Qty(100, "kVA"),
            ratedU=Qty(12.47, "kV"),
            r=Qty(1, "ohm"),
        )


def test_add_mesh_impedance_construction_module_has_no_mesh_class(network, container):
    """TransformerBankBuilder.add_mesh_impedance calls
    super().add_mesh_impedance(...) first (which succeeds, same as
    PowerTransformerBuilder's standalone test), then calls
    graph_write.set_assc_from_mrid(..., profile_part=CONSTR,
    association_name="FromWinding", target_class=constr.TransformerWinding, ...)
    - but CONSTR (construction) has no TransformerMeshImpedance class at
    all, so _part_field's getattr(part, cls_name, None) returns None and
    raises ValueError naming the wrong module, for every call. Should be
    EL_BAL (electrical_balanced), which does have TransformerMeshImpedance
    with FromWinding/ToWinding fields."""
    builder = TransformerBankBuilder(network=network, container=container)
    xfmr = builder.create(mRID="xfmr1")
    end1 = cim.PowerTransformerEnd(mRID="end1", endNumber=1)
    end2 = cim.PowerTransformerEnd(mRID="end2", endNumber=2)
    network.add_to_graph(end1)
    network.add_to_graph(end2)
    w1 = cim.TransformerWinding(mRID="w1")
    w2 = cim.TransformerWinding(mRID="w2")
    network.add_to_graph(w1)
    network.add_to_graph(w2)

    with pytest.raises(ValueError, match="TransformerMeshImpedance"):
        builder.add_mesh_impedance(
            xfmr,
            FromTransformerEnd="end1",
            ToTransformerEnd="end2",
            FromWinding="w1",
            ToWinding="w2",
            r=Qty(1, "ohm"),
            x=Qty(5, "ohm"),
        )
