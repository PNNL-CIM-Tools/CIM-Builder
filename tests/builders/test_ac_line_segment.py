"""ACLineSegmentBuilder / PerLengthSequenceImpedanceBuilder /
PerLengthPhaseImpedanceBuilder tests (design: cimbuilder/development/
OBJECT_BUILDER_MIGRATION.md Phase 3, resolved against real .cimtbl reference
models and Visio modeling reference diagrams LineModel01-05 - see the
approved implementation plan at the time of writing for the full
field-location evidence).

Covers all four coexisting impedance representations: direct balanced PI
(shape 1, PSS/E), direct zero-sequence PI (shape 2), per-length balanced
reference (shape 3, OpenDSS LineCode), and per-length matrix reference
(shape 4, OpenDSS LineCode rmatrix/xmatrix/cmatrix) - see base.py's module
docstring.
"""

import importlib
import tempfile

import pytest
from cimgraph.core.env_vars import get_cim_profile
from cimgraph.databases import XMLFile
from cimgraph.models import BusBranchModel

from cimbuilder.builders.line import (
    ACLineSegmentBuilder,
    PerLengthPhaseImpedanceBuilder,
    PerLengthSequenceImpedanceBuilder,
)
from cimtables import graph_write
from cimtables.name_index import NameIndex
from cimtables.units import Qty

# Profile set per test via monkeypatch (+ cache_clear, since get_cim_profile
# is @cache'd with no args - a bare os.environ assignment at module scope
# would leak into every other test file collected in the same pytest
# process). Mirrors cimtables/tests/test_bind_cim18v17.py's cim fixture and
# tests/builders/test_power_transformer.py's own copy of the same fixture.


@pytest.fixture
def cim(monkeypatch):
    monkeypatch.setenv('CIMG_CIM_PROFILE', 'cim18v17')
    get_cim_profile.cache_clear()
    yield importlib.import_module('cimprofiles.cim18.cim18v17')
    get_cim_profile.cache_clear()


@pytest.fixture
def network(cim):
    conn = XMLFile(filename=tempfile.mktemp(suffix='.xml'))
    container = cim.Feeder(name='ieee13nodeckt')
    net = BusBranchModel(connection=conn, container=container, distributed=False)
    net.name_index = NameIndex()
    return net


# --- connectivity -----------------------------------------------------------

def test_add_connectivity_builds_two_terminals(network):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(name='650632')
    terminals = builder.add_connectivity(line, node1='rg60', node2='632', phases='ABC', length=Qty(2000, 'ft'))

    assert len(terminals) == 2
    assert terminals[0].ConnectivityNode.name == 'rg60'
    assert terminals[1].ConnectivityNode.name == '632'
    assert line.length.to('ft') == pytest.approx(2000)
    assert line.EquipmentContainer is network.container


def test_add_connectivity_builds_phase_children_in_order(network):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(name='632645')
    builder.add_connectivity(line, node1='632', node2='645', phases='CB')

    phases = line.ACLineSegmentPhases
    assert [p.phase.value for p in phases] == ['C', 'B']
    assert [p.sequenceNumber for p in phases] == [1, 2]


def test_add_connectivity_resolves_base_voltage(network, cim):
    bv = cim.BaseVoltage(name='bv_4p16kv')
    graph_write.add_to_graph(network, bv)

    builder = ACLineSegmentBuilder(network)
    line = builder.create(name='650632')
    builder.add_connectivity(line, node1='rg60', node2='632', BaseVoltage='bv_4p16kv')

    assert line.BaseVoltage is bv


# --- shape 1/2: direct PI (balanced + zero-sequence) ------------------------

def test_add_electrical_writes_balanced_pi_values(network):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(name='line1')
    builder.add_electrical(line, r=Qty(1.04, 'ohm'), x=Qty(33.4, 'ohm'),
                            bch=Qty(5.6e-6, 'S'), gch=Qty(0, 'S'))

    assert line.r.to('ohm') == pytest.approx(1.04)
    assert line.x.to('ohm') == pytest.approx(33.4)
    assert line.bch.to('S') == pytest.approx(5.6e-6)
    assert line.gch.to('S') == pytest.approx(0)


def test_add_short_circuit_writes_zero_sequence_pi_values(network):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(name='line1')
    builder.add_short_circuit(line, r0=Qty(3.0, 'ohm'), x0=Qty(10.0, 'ohm'),
                               b0ch=Qty(1.2e-6, 'S'), g0ch=Qty(0, 'S'))

    assert line.r0.to('ohm') == pytest.approx(3.0)
    assert line.x0.to('ohm') == pytest.approx(10.0)
    assert line.b0ch.to('S') == pytest.approx(1.2e-6)


# --- shape 3: per-length balanced reference ---------------------------------

def test_per_length_sequence_impedance_builder(network):
    seq_builder = PerLengthSequenceImpedanceBuilder(network)
    seq = seq_builder.create(name='linecode1')
    graph_write.add_to_graph(network, seq)
    seq_builder.add_rating(seq, r=Qty(0.306, 'ohm/mi'), x=Qty(0.6276, 'ohm/mi'),
                            bch=Qty(0, 'S/mi'), calculatedFrequency=Qty(60, 'Hz'))

    line_builder = ACLineSegmentBuilder(network)
    line = line_builder.create(name='line1')
    target = line_builder.add_per_length_impedance(line, PerLengthImpedance='linecode1')

    assert target is seq
    assert line.PerLengthImpedance is seq
    assert seq.r.to('ohm/mi') == pytest.approx(0.306)


def test_add_per_length_impedance_missing_template_raises(network):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(name='line1')
    with pytest.raises(ValueError, match='not found in graph'):
        builder.add_per_length_impedance(line, PerLengthImpedance='does_not_exist')


# --- shape 4: per-length matrix reference -----------------------------------

def test_mtx601_pole_top_example(network):
    """Mirrors /home/ande188/CIMTBL-Models/distribution/IEEE/IEEE13_CDPSM/
    linecodes.cimtbl's mtx601 + lines.cimtbl's 650632 line end to end via the
    direct/manual API."""
    matrix_builder = PerLengthPhaseImpedanceBuilder(network)
    mtx601 = matrix_builder.create(name='mtx601')
    graph_write.add_to_graph(network, mtx601)
    matrix_builder.add_rating(mtx601, conductorCount=3, calculatedFrequency=Qty(60, 'Hz'))
    matrix_builder.add_phase_impedance_data(mtx601, entries=[
        {'row': 1, 'column': 1, 'r': Qty(0.3465, 'ohm/mi'), 'x': Qty(1.0179, 'ohm/mi')},
        {'row': 2, 'column': 1, 'r': Qty(0.1560, 'ohm/mi'), 'x': Qty(0.5017, 'ohm/mi')},
        {'row': 2, 'column': 2, 'r': Qty(0.3375, 'ohm/mi'), 'x': Qty(1.0478, 'ohm/mi')},
        {'row': 3, 'column': 1, 'r': Qty(0.1580, 'ohm/mi'), 'x': Qty(0.4236, 'ohm/mi')},
        {'row': 3, 'column': 2, 'r': Qty(0.1535, 'ohm/mi'), 'x': Qty(0.3849, 'ohm/mi')},
        {'row': 3, 'column': 3, 'r': Qty(0.3414, 'ohm/mi'), 'x': Qty(1.0348, 'ohm/mi')},
    ])

    line_builder = ACLineSegmentBuilder(network)
    line = line_builder.create(name='650632')
    line_builder.add_connectivity(line, node1='rg60', node2='632', phases='ABC', length=Qty(2000, 'ft'))
    line_builder.add_per_length_impedance(line, PerLengthImpedance='mtx601')

    assert line.PerLengthImpedance is mtx601
    assert mtx601.conductorCount == 3
    assert len(mtx601.PhaseImpedanceData) == 6
    diag = next(d for d in mtx601.PhaseImpedanceData if d.row == 1 and d.column == 1)
    assert diag.PhaseImpedance is mtx601
    assert diag.r.to('ohm/mi') == pytest.approx(0.3465)
    phases = line.ACLineSegmentPhases
    assert [p.sequenceNumber for p in phases] == [1, 2, 3]
