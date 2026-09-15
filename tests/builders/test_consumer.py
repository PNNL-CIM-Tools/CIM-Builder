"""Phase 5 EnergyConsumerBuilder tests (design: CIMTBL_DESIGN.md §4, §8.1,
cimbuilder/development/GRAPH_WRITE_CONTRACT.md).

Covers the direct Builder API in isolation, then from_table end to end against
real validated EnergyConsumerRows parsed out of ieee13.cimtbl - including the
load_sub row, whose EquipmentContainer overrides its table's header-level
default (see dsl/parser.py's table_stmt).

Builders are stateless: create() returns the object directly, every add_<part>
method takes it as an explicit first parameter, and add() (not build()) adds
it to the graph.
"""

import os
import tempfile

import pytest

os.environ['CIMG_CIM_PROFILE'] = 'cimhub_2026'

import cimgraph.data_profile.cimhub_2026 as cim
from cimgraph.databases import XMLFile
from cimgraph.models import BusBranchModel

from cimbuilder.builders.consumer import EnergyConsumerBuilder
from cimbuilder.core import graph_write
from cimbuilder.core.name_index import NameIndex
from cimbuilder.core.units import Qty
from cimbuilder.dsl import parser, validate

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'cimbuilder', 'development')


@pytest.fixture
def network():
    conn = XMLFile(filename=tempfile.mktemp(suffix='.xml'))
    container = cim.Feeder(name='test_feeder')
    net = BusBranchModel(connection=conn, container=container, distributed=False)
    net.name_index = NameIndex()
    return net


# --- direct API -------------------------------------------------------------

def test_create_add_connectivity_add_electrical_add(network):
    builder = EnergyConsumerBuilder(network)
    load = builder.create(name='load_671')
    builder.add_connectivity(load, node='671')
    builder.add_electrical(load, p=Qty(1155.0, 'kW'), q=Qty(660.0, 'kVAr'))
    consumer = builder.add(load)

    assert consumer.name == 'load_671'
    assert consumer.p.to('kW') == pytest.approx(1155.0)
    assert consumer.q.to('kVAr') == pytest.approx(660.0)
    assert len(consumer.Terminals) == 1
    node = graph_write.resolve(network, cim.ConnectivityNode, '671')
    assert node is not None
    assert consumer.Terminals[0].ConnectivityNode is node


def test_add_connectivity_uses_network_default_container(network):
    builder = EnergyConsumerBuilder(network)
    load = builder.create(name='load_671')
    builder.add_connectivity(load, node='671')
    consumer = builder.add(load)
    assert consumer.EquipmentContainer is network.container


def test_add_connectivity_explicit_container_overrides_default(network):
    other = cim.Feeder(name='other_feeder')
    builder = EnergyConsumerBuilder(network, container=other)
    load = builder.create(name='load_671')
    builder.add_connectivity(load, node='671')
    consumer = builder.add(load)
    assert consumer.EquipmentContainer is other


def test_add_references_resolves_existing_targets(network):
    base_voltage = cim.BaseVoltage(name='base_4160')
    graph_write.add_to_graph(network, base_voltage)
    load_response = cim.LoadResponseCharacteristic(name='zip_constantPQ')
    graph_write.add_to_graph(network, load_response)

    builder = EnergyConsumerBuilder(network)
    load = builder.create(name='load_671')
    builder.add_connectivity(load, node='671')
    builder.add_references(load, BaseVoltage='base_4160', LoadResponse='zip_constantPQ')
    consumer = builder.add(load)

    assert consumer.BaseVoltage is base_voltage
    assert consumer.LoadResponse is load_response
    assert consumer in base_voltage.ConductingEquipment


def test_add_references_unresolved_name_links_none(network):
    builder = EnergyConsumerBuilder(network)
    load = builder.create(name='load_671')
    builder.add_connectivity(load, node='671')
    builder.add_references(load, BaseVoltage='does_not_exist')
    consumer = builder.add(load)
    assert consumer.BaseVoltage is None


# --- from_table, against the real sample ------------------------------------

@pytest.fixture
def ieee13_energy_consumer_rows():
    records, _ = parser.parse_file(os.path.join(SAMPLES_DIR, 'ieee13.cimtbl'))
    return [
        validate.validate(r) for r in records
        if r.cim_class == 'EnergyConsumer'
    ]


@pytest.fixture
def network_with_referents(network):
    """The BaseVoltage/LoadResponseCharacteristic/container objects the real
    ieee13 EnergyConsumer rows reference by name, so add_references has
    something real to resolve against."""
    for name in ('base_4160', 'base_480', 'base_115'):
        graph_write.add_to_graph(network, cim.BaseVoltage(name=name))
    for name in ('zip_constantPQ', 'zip_constantZ'):
        graph_write.add_to_graph(network, cim.LoadResponseCharacteristic(name=name))
    graph_write.add_to_graph(network, cim.Feeder(name='ieee_13_debug'))
    graph_write.add_to_graph(network, cim.Feeder(name='sub'))
    return network


def _build_all(network, rows):
    built = {}
    for row in rows:
        builder = EnergyConsumerBuilder(network)
        load = builder.from_table(row)
        consumer = builder.add(load)
        built[consumer.name] = consumer
    return built


def test_from_table_builds_all_ieee13_energy_consumers(network_with_referents, ieee13_energy_consumer_rows):
    built = _build_all(network_with_referents, ieee13_energy_consumer_rows)
    assert set(built) == {'load_671', 'load_634', 'load_646', 'load_sub'}


def test_from_table_sets_electrical_values(network_with_referents, ieee13_energy_consumer_rows):
    built = _build_all(network_with_referents, ieee13_energy_consumer_rows)
    load_671 = built['load_671']
    assert load_671.p.to('kW') == pytest.approx(1155.0)
    assert load_671.q.to('kVAr') == pytest.approx(660.0)


def test_from_table_resolves_base_voltage_and_load_response(network_with_referents, ieee13_energy_consumer_rows):
    built = _build_all(network_with_referents, ieee13_energy_consumer_rows)
    load_671 = built['load_671']
    assert load_671.BaseVoltage is graph_write.resolve(network_with_referents, cim.BaseVoltage, 'base_4160')
    assert load_671.LoadResponse is graph_write.resolve(
        network_with_referents, cim.LoadResponseCharacteristic, 'zip_constantPQ'
    )


def test_from_table_equipment_container_default_and_row_override(network_with_referents, ieee13_energy_consumer_rows):
    # load_671/634/646 sit in a table whose header defaults EquipmentContainer
    # to ieee_13_debug; load_sub's row supplies its own trailing value ('sub'),
    # which must override that default (dsl/parser.py's table_stmt).
    built = _build_all(network_with_referents, ieee13_energy_consumer_rows)
    ieee_13_debug = graph_write.resolve(network_with_referents, cim.Feeder, 'ieee_13_debug')
    sub = graph_write.resolve(network_with_referents, cim.Feeder, 'sub')

    assert built['load_671'].EquipmentContainer is ieee_13_debug
    assert built['load_634'].EquipmentContainer is ieee_13_debug
    assert built['load_646'].EquipmentContainer is ieee_13_debug
    assert built['load_sub'].EquipmentContainer is sub


def test_from_table_auto_vivifies_connectivity_node(network_with_referents, ieee13_energy_consumer_rows):
    built = _build_all(network_with_referents, ieee13_energy_consumer_rows)
    node_671 = graph_write.resolve(network_with_referents, cim.ConnectivityNode, '671')
    assert node_671 is not None
    assert built['load_671'].Terminals[0].ConnectivityNode is node_671


def test_from_table_missing_equipment_container_raises(network, ieee13_energy_consumer_rows):
    # network fixture has no Feeder/Substation built at all - every row's
    # EquipmentContainer name is unresolvable, which must fail fast rather
    # than silently fall back to network.container (§12.3: resolve() never
    # raises, but a Builder deciding a named FK is missing is free to).
    load_671 = next(r for r in ieee13_energy_consumer_rows if r.name == 'load_671')
    with pytest.raises(ValueError, match='EquipmentContainer'):
        EnergyConsumerBuilder(network).from_table(load_671)
