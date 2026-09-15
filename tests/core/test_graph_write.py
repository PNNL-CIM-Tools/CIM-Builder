"""Phase 3 graph-write core tests (design: CIMTBL_DESIGN.md §12.3).

set_attr binds a Qty into the right CIMUnit subclass (verified via .to()) or
passes a plain scalar straight through; add_to_graph writes to both
network.graph and network.name_index at the same call site; resolve is a
never-raising O(1) NameIndex lookup.
"""

import os
import tempfile

import pytest

os.environ['CIMG_CIM_PROFILE'] = 'cimhub_2026'

import cimgraph.data_profile.cimhub_2026 as cim
from cimgraph.databases import XMLFile
from cimgraph.models import BusBranchModel

from cimbuilder.core import graph_write
from cimbuilder.core.name_index import NameIndex
from cimbuilder.core.units import Qty


@pytest.fixture
def network():
    conn = XMLFile(filename=tempfile.mktemp(suffix='.xml'))
    container = cim.Feeder(name='test_feeder')
    net = BusBranchModel(connection=conn, container=container, distributed=False)
    net.name_index = NameIndex()
    return net


def test_set_attr_none_sets_none():
    bv = cim.BaseVoltage(name='bv')
    graph_write.set_attr(bv, 'nominalVoltage', None)
    assert bv.nominalVoltage is None


def test_set_attr_plain_scalar_passes_through():
    line = cim.ACLineSegment(name='line')
    graph_write.set_attr(line, 'circuitNumber', 1)
    assert line.circuitNumber == 1


def test_set_attr_qty_with_unit_binds_cimunit():
    bv = cim.BaseVoltage(name='bv')
    graph_write.set_attr(bv, 'nominalVoltage', Qty(115.0, 'kV'))
    assert bv.nominalVoltage.to('V') == 115000.0


def test_set_attr_qty_blank_unit_assumes_base_si():
    freq = cim.BaseFrequency(name='f')
    graph_write.set_attr(freq, 'frequency', Qty(60.0, ''))
    assert freq.frequency.to('Hz') == 60.0


def test_set_attr_qty_on_non_quantity_attr_raises():
    bv = cim.BaseVoltage(name='bv')
    with pytest.raises(ValueError, match='not a CIMUnit-typed attribute'):
        graph_write.set_attr(bv, 'name', Qty(1.0, 'V'))


def test_link_sets_association_attribute():
    line = cim.ACLineSegment(name='line')
    bv = cim.BaseVoltage(name='bv')
    graph_write.link(line, 'BaseVoltage', bv)
    assert line.BaseVoltage is bv


def test_add_to_graph_populates_graph_and_name_index(network):
    bv = cim.BaseVoltage(name='bv_1')
    graph_write.add_to_graph(network, bv)
    assert network.graph[cim.BaseVoltage][bv.identifier] is bv
    assert network.name_index.get(cim.BaseVoltage, 'bv_1') is bv


def test_resolve_returns_none_on_miss(network):
    assert graph_write.resolve(network, cim.BaseVoltage, 'nonexistent') is None


def test_resolve_returns_bound_object_on_hit(network):
    bv = cim.BaseVoltage(name='bv_1')
    graph_write.add_to_graph(network, bv)
    assert graph_write.resolve(network, cim.BaseVoltage, 'bv_1') is bv
