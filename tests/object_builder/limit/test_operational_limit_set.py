import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.limit import OperationalLimitSetBuilder
from cimbuilder.object_builder.switch import BreakerBuilder

def test_add_limit_type_direction_wrapped_in_enum(network, container):
    builder = OperationalLimitSetBuilder(network=network, container=container)

    lim_type = builder.add_limit_type(mRID="normal_limit", name="normal", direction="high")

    assert lim_type.direction == network.cim.OperationalLimitDirectionKind("high")


def test_add_limit_type_without_direction(network, container):
    builder = OperationalLimitSetBuilder(network=network, container=container)
    limit_type = builder.add_limit_type(
        mRID="normal_limit",
        name="normal",
        acceptableDuration=Qty(999999, "s"),
        isInfiniteDuration=True,
    )
    assert limit_type.isInfiniteDuration is True


@pytest.fixture
def breaker(network, container, base_voltage):
    switch_builder = BreakerBuilder(network=network, container=container)
    switch = switch_builder.create(mRID="sw_brk1")
    switch_builder.add_connectivity(switch, node1="bus1", node2="bus2", BaseVoltage=base_voltage.mRID)
    return switch


@pytest.fixture
def builder(network, container):
    return OperationalLimitSetBuilder(network=network, container=container)


@pytest.mark.parametrize(
    "selector, expected_terminal",
    [
        ({}, None),
        ({"Terminal": "sw_brk1_T2"}, "sw_brk1_T2"),
        ({"terminal_sequence_number": 1}, "sw_brk1_T1"),
        ({"node_side_reference": "bus2"}, "sw_brk1_T2"),
    ],
)
def test_add_equipment(builder, breaker, selector, expected_terminal):
    limit_set = builder.create(mRID="sw_brk1_limits")
    builder.add_equipment(limit_set, Equipment=breaker.mRID, **selector)
    assert limit_set.Equipment is breaker
    assert getattr(limit_set.Terminal, "mRID", None) == expected_terminal


def test_add_equipment_two_selectors(builder, breaker):
    limit_set = builder.create(mRID="sw_brk1_limits")
    with pytest.raises(ValueError, match="give one of"):
        builder.add_equipment(
            limit_set, Equipment=breaker.mRID, Terminal="sw_brk1_T1", terminal_sequence_number=1
        )


def test_line_ampacity_limits(builder, breaker):
    """B13: normal and emergency ampacity on one set"""
    normal = builder.add_limit_type(mRID="olt_normal", isInfiniteDuration=True, direction="absoluteValue")
    emergency = builder.add_limit_type(
        mRID="olt_emergency", acceptableDuration=Qty(4, "hour"), direction="absoluteValue"
    )
    limit_set = builder.create(mRID="sw_brk1_limits")
    builder.add_equipment(limit_set, Equipment=breaker.mRID)
    _, normal_limit = builder.add_current_limit(
        limit_set, mRID="sw_brk1_normal", value=Qty(400, "A"), OperationalLimitType=normal.mRID
    )
    _, emergency_limit = builder.add_current_limit(
        limit_set, mRID="sw_brk1_emergency", value=Qty(600, "A"), OperationalLimitType=emergency.mRID
    )

    assert normal_limit.OperationalLimitSet is limit_set
    assert set(limit_set.OperationalLimitValue) == {normal_limit, emergency_limit}
    assert normal_limit.OperationalLimitType is normal
    assert emergency_limit.OperationalLimitType is emergency
    assert float(emergency_limit.value.to("A")) == 600


@pytest.mark.parametrize(
    "method, value, default_mRID",
    [
        ("add_voltage_limit", Qty(12.47, "kV"), "set1_voltage_limit_olt_normal"),
        ("add_current_limit", Qty(400, "A"), "set1_current_limit_olt_normal"),
        ("add_active_power_limit", Qty(5, "MW"), "set1_active_power_limit_olt_normal"),
        ("add_apparent_power_limit", Qty(6, "MVA"), "set1_apparent_power_limit_olt_normal"),
    ],
)
def test_limit_default_mrid(builder, method, value, default_mRID):
    builder.add_limit_type(mRID="olt_normal")
    limit_set = builder.create(mRID="set1")
    _, limit = getattr(builder, method)(limit_set, value=value, OperationalLimitType="olt_normal")
    assert limit.mRID == default_mRID
    assert limit.OperationalLimitSet is limit_set


def test_limit_unknown_type(builder):
    limit_set = builder.create(mRID="set1")
    with pytest.raises(ValueError, match="OperationalLimitType"):
        builder.add_current_limit(limit_set, value=Qty(400, "A"), OperationalLimitType="olt_missing")
