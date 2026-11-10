import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.shunt import LinearShuntCompensatorBuilder


def test_add_connectivity_compensatorType_wrapped_in_enum(network, container, base_voltage):
    builder = LinearShuntCompensatorBuilder(network=network, container=container)
    shunt = builder.create(mRID="cap1")

    builder.add_connectivity(
        shunt, node="bus1", compensatorType="capacitor", BaseVoltage=base_voltage.mRID
    )

    assert shunt.compensatorType == network.cim.CompensatorKind("capacitor")


def test_add_electrical_with_explicit_bPerSection(network, container):
    builder = LinearShuntCompensatorBuilder(network=network, container=container)
    shunt = builder.create(mRID="cap1")

    builder.add_electrical(shunt, nomU=Qty(12.47, "kV"), bPerSection=Qty(1e-4, "S"))
    assert float(shunt.bPerSection.to("S")) == pytest.approx(1e-4)


def test_add_electrical_computes_bPerSection_from_nomQ(network, container):
    builder = LinearShuntCompensatorBuilder(network=network, container=container)
    shunt = builder.create(mRID="cap1")

    builder.add_electrical(
        shunt, nomU=Qty(12.47, "kV"), nomQ=Qty(300, "kVAr"), maximumSections=3
    )
    assert shunt.bPerSection is not None


def test_add_electrical_raises_without_nomQ_or_bPerSection(network, container):
    builder = LinearShuntCompensatorBuilder(network=network, container=container)
    shunt = builder.create(mRID="cap1")

    with pytest.raises(ValueError, match="bPerSection"):
        builder.add_electrical(shunt, nomU=Qty(12.47, "kV"))


def test_add_short_circuit(network, container):
    builder = LinearShuntCompensatorBuilder(network=network, container=container)
    shunt = builder.create(mRID="cap1")

    builder.add_short_circuit(shunt, b0PerSection=Qty(1e-5, "S"), g0PerSection=Qty(1e-6, "S"))
    assert float(shunt.b0PerSection.to("S")) == pytest.approx(1e-5)


def test_add_ssh(network, container):
    builder = LinearShuntCompensatorBuilder(network=network, container=container)
    shunt = builder.create(mRID="cap1")

    builder.add_ssh(shunt, sections=3, inService=True)
    assert shunt.sections == 3
    assert shunt.inService is True


def test_capacitor_voltage_control(network, container, base_voltage):
    """B10: a voltage-controlled capacitor watching its own terminal"""
    from cimbuilder.object_builder.control import RegulatingControlBuilder

    builder = LinearShuntCompensatorBuilder(network=network, container=container)
    shunt = builder.create(mRID="cap_675")
    _, terminal, _ = builder.add_connectivity(
        shunt, node="675", compensatorType="capacitor", phases="ABC", BaseVoltage=base_voltage.mRID
    )
    control_builder = RegulatingControlBuilder(network=network, container=container)
    control = control_builder.create(mRID="cap_675_ctrl")
    control_builder.add_regulating_control(
        control,
        Terminal=terminal.mRID,
        mode="voltage",
        targetValue=120.5 * 60,
        targetDeadband=3 * 60,
        ptRatio=60,
        discrete=True,
        enabled=True,
    )
    builder.add_regulating_control(
        shunt, RegulatingControl=control.mRID, controlEnabled=True, aVRDelay=Qty(30, "s")
    )

    assert shunt.RegulatingControl is control
    assert shunt in control.RegulatingCondEq
    assert control.Terminal is terminal
    assert control.mode == network.cim.RegulatingControlModeKind("voltage")
    assert control.monitoredPhase is None
    assert float(shunt.aVRDelay.to("s")) == 30


def test_add_electrical_integer_sections(network, container):
    """C3: section counts are int in cim18v17"""
    builder = LinearShuntCompensatorBuilder(network=network, container=container)
    shunt = builder.create(mRID="cap1")
    builder.add_electrical(
        shunt, nomU=Qty(4.16, "kV"), nomQ=Qty(600, "kVAr"), normalSections=2, maximumSections=4
    )
    assert shunt.maximumSections == 4
