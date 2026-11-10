import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.source import EnergySourceBuilder


def test_energy_source(network, container, base_voltage):
    builder = EnergySourceBuilder(network=network, container=container)
    source = builder.create(mRID="src_source", name="source")
    _, terminal, source_phases = builder.add_connectivity(
        source,
        node="sourcebus",
        nominalVoltage=Qty(12.47, "kV"),
        phases="ABC",
        BaseVoltage=base_voltage.mRID,
    )
    builder.add_electrical(source, r=Qty(0.1, "ohm"), x=Qty(1.0, "ohm"))
    builder.add_short_circuit(source, r0=Qty(0.2, "ohm"), x0=Qty(3.0, "ohm"))
    builder.add_ssh(source, voltageMagnitude=Qty(12.8, "kV"), voltageAngle=Qty(30, "deg"))

    assert terminal.mRID == "src_source_T1"
    assert terminal.phases == network.cim.PhaseCode("ABC")
    assert [phase.mRID for phase in source_phases] == ["src_source_A", "src_source_B", "src_source_C"]
    assert source.EquipmentContainer is container
    assert source.BaseVoltage is base_voltage
    assert float(source.nominalVoltage.to("kV")) == pytest.approx(12.47)
    assert float(source.x0.to("ohm")) == 3.0
    assert float(source.voltageAngle.to("deg")) == pytest.approx(30)
