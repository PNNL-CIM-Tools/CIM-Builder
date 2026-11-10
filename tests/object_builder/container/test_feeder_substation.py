import pytest

from cimbuilder.object_builder.container import FeederBuilder, SubstationBuilder


def test_feeder_energized_by_substation(network, container):
    substation_builder = SubstationBuilder(network=network, container=container)
    substation = substation_builder.create(mRID="sub_ieee13", name="ieee13")
    substation_builder.add_connectivity(substation)

    feeder_builder = FeederBuilder(network=network, container=container)
    feeder = feeder_builder.create(mRID="fdr_ieee13", name="ieee13")
    feeder_builder.add_connectivity(feeder, NormalEnergizingSubstation=substation.mRID)

    assert feeder.NormalEnergizingSubstation is substation
    assert feeder in substation.NormalEnergizedFeeder
    assert network.find_by_mRID("fdr_ieee13") is feeder


def test_feeder_unknown_substation(network, container):
    feeder_builder = FeederBuilder(network=network, container=container)
    feeder = feeder_builder.create(mRID="fdr_1")
    with pytest.raises(ValueError, match="NormalEnergizingSubstation"):
        feeder_builder.add_connectivity(feeder, NormalEnergizingSubstation="sub_missing")
