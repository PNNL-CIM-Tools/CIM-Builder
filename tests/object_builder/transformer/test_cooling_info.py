from cimbuilder.object_builder.transformer import CoolingInfoBuilder


def test_cooling_info_add_asset_info(network, container):
    builder = CoolingInfoBuilder(network=network, container=container)
    info = builder.create(mRID="cool_cat1", name="cool_cat1")

    builder.add_asset_info(info, typeOfCooling="ONAN")
    assert info.typeOfCooling == "ONAN"
