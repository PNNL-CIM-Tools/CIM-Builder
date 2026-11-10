import pytest

from cimbuilder.object_builder.line import OverheadWireInfoBuilder
from cimbuilder.object_builder.switch import SwitchBuilder


def test_add_asset_datasheet(network, container):
    wire_builder = OverheadWireInfoBuilder(network=network, container=container)
    wire_info = wire_builder.create(mRID="wire_556500_26_7", name="wire_556500_26_7")

    switch_builder = SwitchBuilder(network=network, container=container)
    switch = switch_builder.create(mRID="sw1")

    switch_builder.add_asset_datasheet(switch, AssetDatasheet=wire_info.mRID)
    assert switch.AssetDatasheet is wire_info
    assert switch in wire_info.PowerSystemResources


def test_add_asset_datasheet_unknown_mrid(network, container):
    switch_builder = SwitchBuilder(network=network, container=container)
    switch = switch_builder.create(mRID="sw1")

    with pytest.raises(ValueError, match="AssetDatasheet"):
        switch_builder.add_asset_datasheet(switch, AssetDatasheet="no_such_info")
