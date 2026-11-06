from cimtables.units import Qty

from cimbuilder.object_builder.switch import (
    BreakerBuilder,
    LoadBreakSwitchBuilder,
    ProtectedSwitchBuilder,
    RecloserBuilder,
)


def test_protected_switch_add_electrical(network, container):
    builder = ProtectedSwitchBuilder(network=network, container=container)
    switch = builder.create(mRID="psw1")

    builder.add_electrical(
        switch,
        ratedCurrent=Qty(400, "A"),
        gangOperated=True,
        breakingCapacity=Qty(10, "kA"),
        makingCapacity=Qty(10, "kA"),
    )
    assert float(switch.breakingCapacity.to("kA")) == 10


def test_breaker_add_electrical(network, container):
    builder = BreakerBuilder(network=network, container=container)
    switch = builder.create(mRID="brk1")

    builder.add_electrical(
        switch,
        ratedCurrent=Qty(600, "A"),
        breakingCapacity=Qty(25, "kA"),
        makingCapacity=Qty(25, "kA"),
        inTransitTime=Qty(0.05, "s"),
    )
    assert float(switch.inTransitTime.to("s")) == 0.05


def test_recloser_builder_create(network, container):
    builder = RecloserBuilder(network=network, container=container)
    sw = builder.create(mRID="rec1")
    assert sw.mRID == "rec1"


def test_load_break_switch_builder_create(network, container):
    builder = LoadBreakSwitchBuilder(network=network, container=container)
    sw = builder.create(mRID="lbs1")
    assert sw.mRID == "lbs1"
