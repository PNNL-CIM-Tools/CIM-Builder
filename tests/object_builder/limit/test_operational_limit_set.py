import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.limit import OperationalLimitSetBuilder
from cimbuilder.object_builder.switch import BreakerBuilder

# cimbuilder.object_builder.limit.operational_limit_set imports the
# operational_limit profile-part submodule as LIM and uses it (not
# self.cim) as `target_class` in every set_assc_from_mrid call below.
# Every builder elsewhere in this codebase resolves associations using
# self.cim.<ClassName> (e.g. ac_line_segment.py's `cn.BaseVoltage` where
# `cn = self.cim`), matching the class objects are actually created with
# (ObjectBuilder.create() always instantiates via self.network.cim).
# LIM.<ClassName> is a structurally-identical but DISTINCT runtime class
# from self.cim.<ClassName> (same name, no shared base beyond
# Identity/object), so resolve()'s isinstance(obj, target_class) check
# always fails here, regardless of which real mRID is passed - this is a
# systemic bug affecting every association write in this file.


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


def test_add_equipment_wrong_target_class_for_resolve(network, container, base_voltage):
    """add_equipment's Equipment resolution uses
    target_class=LIM.Equipment (the literal submodule class) instead of
    self.cim.Equipment - raises ValueError for any real Equipment mRID,
    since the Breaker object was actually created via self.cim.Breaker."""
    switch_builder = BreakerBuilder(network=network, container=container)
    switch = switch_builder.create(mRID="brk1")
    switch_builder.add_connectivity(
        switch, node1="bus1", node2="bus2", BaseVoltage=base_voltage.mRID
    )

    builder = OperationalLimitSetBuilder(network=network, container=container)
    limit_set = builder.create(mRID="brk1_limits")

    with pytest.raises(ValueError, match="Equipment"):
        builder.add_equipment(limit_set, Equipment=switch.mRID, terminal_sequence_number=0)


def test_add_equipment_by_explicit_terminal_wrong_target_class(
    network, container, base_voltage
):
    """Same systemic LIM.<Class> vs self.cim.<Class> bug as the test above,
    this time surfacing on the Equipment resolve before the explicit
    Terminal mRID branch is even reached (add_equipment resolves Equipment
    unconditionally whenever Equipment is not None, before checking
    Terminal)."""
    switch_builder = BreakerBuilder(network=network, container=container)
    switch = switch_builder.create(mRID="brk2")
    switch, terminals, _ = switch_builder.add_connectivity(
        switch, node1="bus3", node2="bus4", BaseVoltage=base_voltage.mRID
    )

    builder = OperationalLimitSetBuilder(network=network, container=container)
    limit_set = builder.create(mRID="brk2_limits")

    with pytest.raises(ValueError, match="Equipment"):
        builder.add_equipment(limit_set, Equipment=switch.mRID, Terminal=terminals[0].mRID)


def test_add_voltage_limit_wrong_target_class_for_operational_limit_type(network, container):
    """add_voltage_limit resolves OperationalLimitType via
    target_class=LIM.OperationalLimitType instead of
    self.cim.OperationalLimitType - raises ValueError for any real
    OperationalLimitType mRID (created via add_limit_type's
    self.cim-based construction)."""
    builder = OperationalLimitSetBuilder(network=network, container=container)
    limit_set = builder.create(mRID="vlimit_set")
    limit_type = builder.add_limit_type(mRID="alert_high")

    with pytest.raises(ValueError, match="OperationalLimitType"):
        builder.add_voltage_limit(
            limit_set,
            normalValue=Qty(13.5, "kV"),
            value=Qty(14, "kV"),
            OperationalLimitType=limit_type.mRID,
        )


def test_add_current_limit_wrong_target_class_for_operational_limit_type(network, container):
    """Same systemic bug as test_add_voltage_limit_wrong_target_class_for_operational_limit_type."""
    builder = OperationalLimitSetBuilder(network=network, container=container)
    limit_set = builder.create(mRID="ilimit_set")
    limit_type = builder.add_limit_type(mRID="emergency_high")

    with pytest.raises(ValueError, match="OperationalLimitType"):
        builder.add_current_limit(
            limit_set,
            normalValue=Qty(400, "A"),
            value=Qty(600, "A"),
            OperationalLimitType=limit_type.mRID,
        )


def test_add_active_power_limit_wrong_target_class_for_operational_limit_type(network, container):
    """Same systemic bug as test_add_voltage_limit_wrong_target_class_for_operational_limit_type."""
    builder = OperationalLimitSetBuilder(network=network, container=container)
    limit_set = builder.create(mRID="mwlimit_set")
    limit_type = builder.add_limit_type(mRID="normal_mw")

    with pytest.raises(ValueError, match="OperationalLimitType"):
        builder.add_active_power_limit(
            limit_set,
            normalValue=Qty(5, "MW"),
            value=Qty(6, "MW"),
            OperationalLimitType=limit_type.mRID,
        )


def test_add_apparent_power_limit_wrong_target_class_for_operational_limit_type(network, container):
    """Same systemic bug as test_add_voltage_limit_wrong_target_class_for_operational_limit_type."""
    builder = OperationalLimitSetBuilder(network=network, container=container)
    limit_set = builder.create(mRID="mvalimit_set")
    limit_type = builder.add_limit_type(mRID="normal_mva")

    with pytest.raises(ValueError, match="OperationalLimitType"):
        builder.add_apparent_power_limit(
            limit_set,
            normalValue=Qty(5, "MVA"),
            value=Qty(6, "MVA"),
            OperationalLimitType=limit_type.mRID,
        )
