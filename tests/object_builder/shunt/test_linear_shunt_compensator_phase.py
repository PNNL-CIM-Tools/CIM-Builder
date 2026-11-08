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


def test_add_electrical_derives_bPerSection_from_parent_nomU(network, container):
    cap_builder = LinearShuntCompensatorBuilder(network=network, container=container)
    shunt = cap_builder.create(mRID="cap_675")
    cap_builder.add_electrical(shunt, nomU=Qty(4.16, "kV"), nomQ=Qty(600, "kVAr"))

    builder = LinearShuntCompensatorPhaseBuilder(network=network, container=container)
    phs = builder.create(mRID="cap_675_A")
    builder.add_connectivity(phs, phase="A", ShuntCompensator=shunt.mRID)
    builder.add_electrical(phs, nomQ=Qty(200, "kVAr"), normalSections=1, maximumSections=1)

    assert phs.maximumSections == 1
    assert float(phs.bPerSection.to("S")) == pytest.approx(200e3 / 4160**2)


def test_add_ssh(network, container):
    builder = LinearShuntCompensatorPhaseBuilder(network=network, container=container)
    phs = builder.create(mRID="cap_675_A")

    builder.add_ssh(phs, sections=1)
    assert phs.sections == 1
