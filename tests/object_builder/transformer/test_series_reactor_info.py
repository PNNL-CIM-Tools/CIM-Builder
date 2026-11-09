from cimbuilder.object_builder.transformer import SeriesReactorInfoBuilder


def test_series_reactor_info_add_asset_info(network, container):
    builder = SeriesReactorInfoBuilder(network=network, container=container)
    info = builder.create(mRID="reac_cat1", name="reac_cat1")

    builder.add_asset_info(info, ratedInductance=0.001)
    assert info.ratedInductance == 0.001
