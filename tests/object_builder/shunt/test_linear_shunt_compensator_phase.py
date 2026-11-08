import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.shunt import (
    LinearShuntCompensatorBuilder,
    LinearShuntCompensatorPhaseBuilder,
)


def test_add_connectivity_phase_wrapped_in_enum(network, container):
    cap_builder = LinearShuntCompensatorBuilder(network=network, container=container)
    shunt = cap_builder.create(mRID="cap1")

    builder = LinearShuntCompensatorPhaseBuilder(network=network, container=container)
    phs = builder.create(mRID="cap1_A")

    builder.add_connectivity(phs, phase="A", ShuntCompensator=shunt.mRID)

    assert phs.phase == network.cim.SinglePhaseKind("A")


def test_add_electrical_wrong_profile_part_module(network, container):
    """add_electrical's type hint says
    `shunt_phase: EL_BAL.LinearShuntCompensator` (electrical_balanced),
    but the real runtime object is a LinearShuntCompensatorPhase, and
    EL_BAL (electrical_balanced) has no LinearShuntCompensatorPhase class
    at all - only EL_UNBAL (electrical_unbalanced) does, with exactly the
    fields this method tries to write (nomQ, normalSections,
    maximumSections, bPerSection, gPerSection). Every set_attr call in
    this method uses the wrong profile-part module and raises."""
    builder = LinearShuntCompensatorPhaseBuilder(network=network, container=container)
    phs = builder.create(mRID="cap1_A")

    with pytest.raises(ValueError, match="LinearShuntCompensatorPhase"):
        builder.add_electrical(phs, nomQ=Qty(100, "kVAr"), maximumSections=3)


def test_add_ssh_inService_field_does_not_exist_on_phase_class(network, container):
    """add_ssh calls graph_write.set_attr(shunt_phase, SSH, "inService",
    inService) unconditionally (no `if inService is not None` guard) -
    SSH.LinearShuntCompensatorPhase has only `sections`, no `inService`
    field (unlike the parent LinearShuntCompensator class, which does have
    one - this looks copy-pasted from LinearShuntCompensatorBuilder.add_ssh
    without checking the Phase class's real fields). Raises for every
    call regardless of what inService is set to, even its None default."""
    builder = LinearShuntCompensatorPhaseBuilder(network=network, container=container)
    phs = builder.create(mRID="cap1_A")

    with pytest.raises(ValueError, match="inService"):
        builder.add_ssh(phs, sections=3)
