from cimtables.units import Qty

from cimbuilder.object_builder.line import SeriesCompensatorBuilder


def test_series_compensator_add_connectivity(network, container, base_voltage):
    builder = SeriesCompensatorBuilder(network=network, container=container)
    compensator = builder.create(mRID="rx_r1")

    compensator, terminals = builder.add_connectivity(
        compensator, node1="bus1", node2="bus2", phases="B", BaseVoltage=base_voltage.mRID
    )
    assert [t.mRID for t in terminals] == ["rx_r1_T1", "rx_r1_T2"]
    assert all(t.phases.value == "B" for t in terminals)
    assert compensator.BaseVoltage is base_voltage
    assert compensator.EquipmentContainer is container


def test_series_compensator_balanced_has_no_terminal_phases(network, container, base_voltage):
    builder = SeriesCompensatorBuilder(network=network, container=container)
    compensator = builder.create(mRID="rx_r1")

    _, terminals = builder.add_connectivity(compensator, node1="bus1", node2="bus2", BaseVoltage=base_voltage.mRID)
    assert all(t.phases is None for t in terminals)


def test_series_compensator_impedances(network, container):
    builder = SeriesCompensatorBuilder(network=network, container=container)
    compensator = builder.create(mRID="rx_r1")

    builder.add_electrical(compensator, r=Qty(0.5, "ohm"), x=Qty(2.0, "ohm"))
    builder.add_short_circuit(compensator, r0=Qty(0.5, "ohm"), x0=Qty(2.0, "ohm"))
    assert float(compensator.x.to("ohm")) == 2.0
    assert float(compensator.r0.to("ohm")) == 0.5
