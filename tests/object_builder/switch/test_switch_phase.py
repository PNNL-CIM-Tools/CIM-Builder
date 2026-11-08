from cimtables.units import Qty

from cimbuilder.object_builder.switch import SwitchBuilder, SwitchPhaseBuilder


def test_switch_phase_add_connectivity(network, container, base_voltage):
    switch_builder = SwitchBuilder(network=network, container=container)
    switch = switch_builder.create(mRID="sw1")
    switch_builder.add_connectivity(
        switch, node1="bus1", node2="bus2", BaseVoltage=base_voltage.mRID
    )

    builder = SwitchPhaseBuilder(network=network, container=container)
    phs = builder.create(mRID="sw1_A")
    phs = builder.add_connectivity(
        phs, Switch=switch.mRID, phaseSide1="A", phaseSide2="A", normalOpen=False
    )
    assert phs.Switch is switch


def test_switch_phase_add_electrical(network, container):
    builder = SwitchPhaseBuilder(network=network, container=container)
    phs = builder.create(mRID="sw1_A")

    builder.add_electrical(phs, ratedCurrent=Qty(100, "A"))
    assert float(phs.ratedCurrent.to("A")) == 100


def test_switch_phase_add_ssh(network, container):
    builder = SwitchPhaseBuilder(network=network, container=container)
    phs = builder.create(mRID="sw1_A")

    builder.add_ssh(phs, open=True)
    assert phs.open is True
