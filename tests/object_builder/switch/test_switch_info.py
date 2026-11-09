from cimtables.units import Qty

from cimbuilder.object_builder.switch import SwitchInfoBuilder


def test_switch_info_add_asset_info(network, container):
    builder = SwitchInfoBuilder(network=network, container=container)
    info = builder.create(mRID="sw_info_cat1", name="sw_info_cat1")

    builder.add_asset_info(info, breakingCapacity=Qty(10, "kA"))
    assert float(info.breakingCapacity.to("kA")) == 10
