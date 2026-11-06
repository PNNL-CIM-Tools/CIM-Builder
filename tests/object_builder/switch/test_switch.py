from cimtables.units import Qty

from cimbuilder.object_builder.switch import (
    AirBreakSwitchBuilder,
    DisconnectorBuilder,
    ElbowBuilder,
    FuseBuilder,
    HookstickSwitchBuilder,
    SectionaliserBuilder,
    ServiceDisconnectBuilder,
    SwitchBuilder,
)


def test_switch_add_connectivity(network, container, base_voltage):
    builder = SwitchBuilder(network=network, container=container)
    switch = builder.create(mRID="sw1")

    switch, terminals, phases = builder.add_connectivity(
        switch,
        node1="bus1",
        node2="bus2",
        phases="ABC",
        normalOpen=False,
        retained=True,
        areaBoundary=False,
        topologicalUsage="busTie",
        BaseVoltage=base_voltage.mRID,
    )
    assert len(terminals) == 2
    assert switch.topologicalUsage is not None


def test_switch_add_electrical(network, container):
    builder = SwitchBuilder(network=network, container=container)
    switch = builder.create(mRID="sw1")

    builder.add_electrical(switch, ratedCurrent=Qty(200, "A"), gangOperated=True)
    assert float(switch.ratedCurrent.to("A")) == 200


def test_switch_add_ssh(network, container):
    builder = SwitchBuilder(network=network, container=container)
    switch = builder.create(mRID="sw1")

    builder.add_ssh(switch, inService=True, open=False)
    assert switch.open is False


def test_fuse_builder_create(network, container):
    builder = FuseBuilder(network=network, container=container)
    fuse = builder.create(mRID="fuse1")
    assert fuse.mRID == "fuse1"


def test_sectionaliser_builder_create(network, container):
    builder = SectionaliserBuilder(network=network, container=container)
    sw = builder.create(mRID="sect1")
    assert sw.mRID == "sect1"


def test_disconnector_builder_create(network, container):
    builder = DisconnectorBuilder(network=network, container=container)
    sw = builder.create(mRID="disc1")
    assert sw.mRID == "disc1"


def test_service_disconnect_builder_create(network, container):
    builder = ServiceDisconnectBuilder(network=network, container=container)
    sw = builder.create(mRID="svcdisc1")
    assert sw.mRID == "svcdisc1"


def test_elbow_builder_create(network, container):
    builder = ElbowBuilder(network=network, container=container)
    sw = builder.create(mRID="elbow1")
    assert sw.mRID == "elbow1"


def test_air_break_switch_builder_create(network, container):
    builder = AirBreakSwitchBuilder(network=network, container=container)
    sw = builder.create(mRID="abs1")
    assert sw.mRID == "abs1"


def test_hookstick_switch_builder_create(network, container):
    builder = HookstickSwitchBuilder(network=network, container=container)
    sw = builder.create(mRID="hook1")
    assert sw.mRID == "hook1"
