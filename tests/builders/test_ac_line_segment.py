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
import os
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
from cimtables import graph_write, impedance, parser, validate
from cimtables.binder import bind_row
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
    return net


# --- connectivity -----------------------------------------------------------

def test_add_connectivity_builds_two_terminals(network):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='650632')
    terminals = builder.add_connectivity(line, node1='rg60', node2='632', phases='ABC', length=Qty(2000, 'ft'))

    assert len(terminals) == 2
    assert terminals[0].ConnectivityNode.mRID == 'rg60'
    assert terminals[1].ConnectivityNode.mRID == '632'
    assert line.length.to('ft') == pytest.approx(2000)
    assert line.EquipmentContainer is network.container


def test_add_connectivity_builds_phase_children_in_order(network):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='632645')
    builder.add_connectivity(line, node1='632', node2='645', phases='CB')

    phases = line.ACLineSegmentPhases
    assert [p.phase.value for p in phases] == ['C', 'B']
    assert [p.sequenceNumber for p in phases] == [1, 2]


def test_add_connectivity_resolves_base_voltage(network, cim):
    bv = cim.BaseVoltage(mRID='bv_4p16kv')
    graph_write.add_to_graph(network, bv)

    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='650632')
    builder.add_connectivity(line, node1='rg60', node2='632', BaseVoltage='bv_4p16kv')

    assert line.BaseVoltage is bv


# --- shape 1/2: direct PI (balanced + zero-sequence) ------------------------

def test_add_electrical_writes_balanced_pi_values(network):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='line1')
    builder.add_electrical(line, r=Qty(1.04, 'ohm'), x=Qty(33.4, 'ohm'),
                            bch=Qty(5.6e-6, 'S'), gch=Qty(0, 'S'))

    assert line.r.to('ohm') == pytest.approx(1.04)
    assert line.x.to('ohm') == pytest.approx(33.4)
    assert line.bch.to('S') == pytest.approx(5.6e-6)
    assert line.gch.to('S') == pytest.approx(0)


def test_add_short_circuit_writes_zero_sequence_pi_values(network):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='line1')
    builder.add_short_circuit(line, r0=Qty(3.0, 'ohm'), x0=Qty(10.0, 'ohm'),
                               b0ch=Qty(1.2e-6, 'S'), g0ch=Qty(0, 'S'))

    assert line.r0.to('ohm') == pytest.approx(3.0)
    assert line.x0.to('ohm') == pytest.approx(10.0)
    assert line.b0ch.to('S') == pytest.approx(1.2e-6)


# --- system-base (pu) impedance ---------------------------------------------
# ACLineSegment has no self-contained rating pair (no ratedS/ratedU anywhere
# in this profile), so a relative r/x/r0/x0 needs CIMG_SYSTEM_MVA_BASE (the
# PSS/E-RAW-SBASE equivalent) paired with the line's own BaseVoltage, not
# cimtables.impedance.resolve_winding_z_base's candidate-rating-pair walk.
# `pu`, not `percent`: percent/%Z is a nameplate-impedance convention for
# transformer tanks (OpenDSS %R/%Xhl), not how line impedance is expressed
# relative to a system base.

@pytest.fixture
def system_mva_base(monkeypatch):
    monkeypatch.setenv('CIMG_SYSTEM_MVA_BASE', '100')
    impedance.get_system_mva_base.cache_clear()
    yield
    impedance.get_system_mva_base.cache_clear()


def test_add_electrical_converts_pu_impedance_using_system_base(network, system_mva_base):
    bv = network.cim.BaseVoltage(mRID='bv_115kv', nominalVoltage=network.cim.Voltage(115, 'kV'))
    graph_write.add_to_graph(network, bv)

    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='line1')
    builder.add_connectivity(line, node1='rg60', node2='632', BaseVoltage='bv_115kv')

    builder.add_electrical(line, r=Qty(0.01, 'pu'), x=Qty(0.05, 'pu'))

    z_base = (115e3 ** 2) / 100e6
    assert line.r.to('ohm') == pytest.approx(0.01 * z_base)
    assert line.x.to('ohm') == pytest.approx(0.05 * z_base)


def test_add_short_circuit_converts_pu_impedance_using_system_base(network, system_mva_base):
    bv = network.cim.BaseVoltage(mRID='bv_115kv', nominalVoltage=network.cim.Voltage(115, 'kV'))
    graph_write.add_to_graph(network, bv)

    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='line1')
    builder.add_connectivity(line, node1='rg60', node2='632', BaseVoltage='bv_115kv')

    builder.add_short_circuit(line, r0=Qty(0.02, 'pu'), x0=Qty(0.08, 'pu'))

    z_base = (115e3 ** 2) / 100e6
    assert line.r0.to('ohm') == pytest.approx(0.02 * z_base)
    assert line.x0.to('ohm') == pytest.approx(0.08 * z_base)


def test_add_electrical_pu_impedance_without_system_mva_base_raises(network):
    impedance.get_system_mva_base.cache_clear()
    bv = network.cim.BaseVoltage(mRID='bv_115kv', nominalVoltage=network.cim.Voltage(115, 'kV'))
    graph_write.add_to_graph(network, bv)

    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='line1')
    builder.add_connectivity(line, node1='rg60', node2='632', BaseVoltage='bv_115kv')

    with pytest.raises(ValueError, match='needs a z_base'):
        builder.add_electrical(line, r=Qty(0.01, 'pu'))
    impedance.get_system_mva_base.cache_clear()


def test_add_electrical_pu_impedance_without_base_voltage_raises(network, system_mva_base):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='line1')

    with pytest.raises(ValueError, match='needs a z_base'):
        builder.add_electrical(line, r=Qty(0.01, 'pu'))


def test_add_electrical_converts_pu_admittance_using_system_base(network, system_mva_base):
    bv = network.cim.BaseVoltage(mRID='bv_115kv', nominalVoltage=network.cim.Voltage(115, 'kV'))
    graph_write.add_to_graph(network, bv)

    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='line1')
    builder.add_connectivity(line, node1='rg60', node2='632', BaseVoltage='bv_115kv')

    builder.add_electrical(line, bch=Qty(0.0528, 'pu'))

    y_base = 100e6 / (115e3 ** 2)
    assert line.bch.to('S') == pytest.approx(0.0528 * y_base)


def test_add_electrical_pu_admittance_without_system_mva_base_raises(network):
    impedance.get_system_mva_base.cache_clear()
    bv = network.cim.BaseVoltage(mRID='bv_115kv', nominalVoltage=network.cim.Voltage(115, 'kV'))
    graph_write.add_to_graph(network, bv)

    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='line1')
    builder.add_connectivity(line, node1='rg60', node2='632', BaseVoltage='bv_115kv')

    with pytest.raises(ValueError, match='needs a y_base'):
        builder.add_electrical(line, bch=Qty(0.0528, 'pu'))
    impedance.get_system_mva_base.cache_clear()


def test_ieee13_line_1_2_bch_pu_row_binds_end_to_end(network, system_mva_base):
    """Regression: cimbuilder/development/ieee13.cimtbl's line_1_2 row
    (bch (pu)=0.05280, r (pu)=1.93800E-2, x (pu)=5.91700E-2, BaseVoltage=
    base_115) previously raised pint.errors.DimensionalityError inside
    bind_row - bch (pu) on a siemens-typed field went straight to plain
    setattr with no gate at all, since set_attr's relative-conversion gate
    was ohm-only before this fix. Binds the real fixture row through the
    real pipeline (parser -> validate -> bind_row), not a hand-written Qty
    call, so this is the actual data that motivated the fix, not just a
    constructed example."""
    bv = network.cim.BaseVoltage(mRID='base_115', nominalVoltage=network.cim.Voltage(115000, 'V'))
    graph_write.add_to_graph(network, bv)
    container = network.cim.Feeder(mRID='transmission_line')
    graph_write.add_to_graph(network, container)

    sample_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'cimbuilder', 'development', 'ieee13.cimtbl')
    records, _ = parser.parse_file(sample_path)
    rows = [validate.validate(r) for r in records if r.cim_class == 'ACLineSegment']
    row = next(r for r in rows if r.mRID == 'line_1_2')

    line = bind_row(network, row)

    z_base = (115000 ** 2) / 100e6
    y_base = 1.0 / z_base
    assert line.r.to('ohm') == pytest.approx(0.01938 * z_base)
    assert line.x.to('ohm') == pytest.approx(0.05917 * z_base)
    assert line.bch.to('S') == pytest.approx(0.0528 * y_base)


# --- shape 3: per-length balanced reference ---------------------------------

def test_per_length_sequence_impedance_builder(network):
    seq_builder = PerLengthSequenceImpedanceBuilder(network)
    seq = seq_builder.create(mRID='linecode1')
    graph_write.add_to_graph(network, seq)
    seq_builder.add_electrical(seq, r=Qty(0.306, 'ohm/mi'), x=Qty(0.6276, 'ohm/mi'),
                            bch=Qty(0, 'S/mi'), calculatedFrequency=Qty(60, 'Hz'))

    line_builder = ACLineSegmentBuilder(network)
    line = line_builder.create(mRID='line1')
    target = line_builder.add_per_length_impedance(line, PerLengthImpedance='linecode1')

    assert target is seq
    assert line.PerLengthImpedance is seq
    assert seq.r.to('ohm/mi') == pytest.approx(0.306)


def test_add_per_length_impedance_missing_template_raises(network):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(mRID='line1')
    with pytest.raises(ValueError, match='not found in graph'):
        builder.add_per_length_impedance(line, PerLengthImpedance='does_not_exist')


# --- shape 4: per-length matrix reference -----------------------------------

def test_mtx601_pole_top_example(network):
    """Mirrors /home/ande188/CIMTBL-Models/distribution/IEEE/IEEE13_CDPSM/
    linecodes.cimtbl's mtx601 + lines.cimtbl's 650632 line end to end via the
    direct/manual API."""
    matrix_builder = PerLengthPhaseImpedanceBuilder(network)
    mtx601 = matrix_builder.create(mRID='mtx601')
    graph_write.add_to_graph(network, mtx601)
    matrix_builder.add_electrical_earthing(mtx601, conductorCount=3, calculatedFrequency=Qty(60, 'Hz'))
    matrix_builder.add_phase_impedance_data(mtx601, entries=[
        {'row': 1, 'column': 1, 'r': Qty(0.3465, 'ohm/mi'), 'x': Qty(1.0179, 'ohm/mi')},
        {'row': 2, 'column': 1, 'r': Qty(0.1560, 'ohm/mi'), 'x': Qty(0.5017, 'ohm/mi')},
        {'row': 2, 'column': 2, 'r': Qty(0.3375, 'ohm/mi'), 'x': Qty(1.0478, 'ohm/mi')},
        {'row': 3, 'column': 1, 'r': Qty(0.1580, 'ohm/mi'), 'x': Qty(0.4236, 'ohm/mi')},
        {'row': 3, 'column': 2, 'r': Qty(0.1535, 'ohm/mi'), 'x': Qty(0.3849, 'ohm/mi')},
        {'row': 3, 'column': 3, 'r': Qty(0.3414, 'ohm/mi'), 'x': Qty(1.0348, 'ohm/mi')},
    ])

    line_builder = ACLineSegmentBuilder(network)
    line = line_builder.create(mRID='650632')
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
