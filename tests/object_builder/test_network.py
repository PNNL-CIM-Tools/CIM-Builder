import pytest
from cimgraph.core import set_model_scope
from cimgraph.core.env_vars import get_model_authority, get_model_name
from cimtables.units import Qty

from cimbuilder import object_builder as OB
from cimbuilder.network import new_feeder_model


@pytest.fixture
def scoped():
    """new_feeder_model sets the process-wide model scope, put it back afterwards"""
    authority, name = get_model_authority(), get_model_name()
    yield
    set_model_scope(authority, name)


def test_new_feeder_model(scoped):
    network = new_feeder_model(
        authority="https://example.org/gdm", model="probe", Feeder="fdr_p", name="p"
    )
    feeder = network.container
    assert network.find_by_mRID("fdr_p") is feeder
    assert feeder.name == "p"
    assert float(network.find_by_mRID("base_freq").frequency.to("Hz")) == 60
    assert get_model_authority() == "https://example.org/gdm"
    assert get_model_name() == "probe"


def test_two_feeder_system(scoped):
    """B1: a GDM system with two feeders, equipment carrying its own EquipmentContainer"""
    network = new_feeder_model(authority="https://example.org/gdm", model="two_feeders", Feeder="fdr_a")
    container = network.container
    sub_builder = OB.SubstationBuilder(network=network, container=container)
    sub_builder.create(mRID="sub_main")
    feeder_builder = OB.FeederBuilder(network=network, container=container)
    feeder_builder.add_connectivity(container, NormalEnergizingSubstation="sub_main")
    fdr_b = feeder_builder.create(mRID="fdr_b")
    feeder_builder.add_connectivity(fdr_b, NormalEnergizingSubstation="sub_main")

    bv = OB.BaseVoltageBuilder(network=network, container=container).create(
        mRID="bv_12_47kv", nominalVoltage=Qty(12.47, "kV")
    )
    node_builder = OB.ConnectivityNodeBuilder(network=network, container=container)
    node = node_builder.create(mRID="b1", name="b1")
    node_builder.add_connectivity(node, BaseVoltage=bv.mRID, ConnectivityNodeContainer="fdr_b")

    source_builder = OB.EnergySourceBuilder(network=network, container=container)
    source = source_builder.create(mRID="src_b")
    source_builder.add_connectivity(
        source, node="b1", nominalVoltage=Qty(12.47, "kV"), phases="ABC",
        EquipmentContainer="fdr_b", BaseVoltage=bv.mRID,
    )
    load_builder = OB.EnergyConsumerBuilder(network=network, container=container)
    load = load_builder.create(mRID="ld_b1")
    load_builder.add_connectivity(
        load, node="b1", phaseConnection="Y", phases="ABC", EquipmentContainer="fdr_b", BaseVoltage=bv.mRID
    )

    assert node.ConnectivityNodeContainer is fdr_b
    assert source.EquipmentContainer is fdr_b
    assert load.EquipmentContainer is fdr_b
    assert {f.mRID for f in network.find_by_mRID("sub_main").NormalEnergizedFeeder} == {"fdr_a", "fdr_b"}
