"""Switch builder tests (design: cimbuilder/development/
OBJECT_BUILDER_MIGRATION.md Phase 4, resolved against the Visio modeling
reference diagram (Switch) - see cimbuilder/builders/switch/switch.py's and
switch_phase.py's module docstrings for the full field-location evidence).

Covers SwitchBuilder (base, switch.py), its subclass chain
(ProtectedSwitchBuilder/BreakerBuilder/RecloserBuilder/LoadBreakSwitchBuilder,
protected_switch.py), and SwitchPhaseBuilder (switch_phase.py) - the
per-SwitchPhase-row builder that lets a switch carry a different phase on
each side (phaseSide1 != phaseSide2), which the generic
cimtables.connectivity.add_phase_children cannot express.
"""

import importlib
import tempfile

import pytest
from cimgraph.core.env_vars import get_cim_profile
from cimgraph.databases import XMLFile
from cimgraph.models import BusBranchModel

from cimbuilder.builders.switch import (
    BreakerBuilder,
    DisconnectorBuilder,
    LoadBreakSwitchBuilder,
    ProtectedSwitchBuilder,
    RecloserBuilder,
)
from cimtables import graph_write
from cimtables.name_index import NameIndex
from cimtables.units import Qty


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


def _add(network, obj):
    graph_write.add_to_graph(network, obj)
    return obj


def test_add_connectivity_builds_two_terminals_with_distinct_names(network):
    """Mirrors the double-UUID bug new_disconnector.py had: t1's name seeded
    twice, t2 never seeded. connectivity.add_connectivity names each
    terminal from its own index, so this can't regress silently."""
    builder = DisconnectorBuilder(network)
    switch = _add(network, builder.create(name='sw1'))
    terminals = builder.add_connectivity(switch, node1='busA', node2='busB')

    assert len(terminals) == 2
    assert terminals[0].name != terminals[1].name
    assert terminals[0].sequenceNumber == 1
    assert terminals[1].sequenceNumber == 2
    assert switch.Terminals == terminals


def test_add_connectivity_same_phase_both_sides(network):
    """The symmetric case: one SwitchPhase row, same phase on both sides."""
    builder = DisconnectorBuilder(network)
    switch = _add(network, builder.create(name='sw1'))
    terminals = builder.add_connectivity(
        switch, node1='busA', node2='busB', phaseSide1=['A'], phaseSide2=['A'])

    assert terminals[0].phases == network.cim.PhaseCode.A
    assert terminals[1].phases == network.cim.PhaseCode.A
    assert len(switch.SwitchPhase) == 1
    assert switch.SwitchPhase[0].phaseSide1 == network.cim.SinglePhaseKind.A
    assert switch.SwitchPhase[0].phaseSide2 == network.cim.SinglePhaseKind.A


def test_add_connectivity_different_phase_per_side(network):
    """The case add_phase_children cannot express: phase A on side 1, phase
    B on side 2 (an open-phase/cross-connected switch) - each terminal gets
    only its own side's phase, not a shared canonical set."""
    builder = DisconnectorBuilder(network)
    switch = _add(network, builder.create(name='sw1'))
    terminals = builder.add_connectivity(
        switch, node1='busA', node2='busB', phaseSide1=['A'], phaseSide2=['B'])

    assert terminals[0].phases == network.cim.PhaseCode.A
    assert terminals[1].phases == network.cim.PhaseCode.B
    assert len(switch.SwitchPhase) == 1
    switch_phase = switch.SwitchPhase[0]
    assert switch_phase.phaseSide1 == network.cim.SinglePhaseKind.A
    assert switch_phase.phaseSide2 == network.cim.SinglePhaseKind.B
    assert switch_phase.Switch is switch


def test_add_connectivity_multiple_rows_build_per_terminal_superset(network):
    """Two SwitchPhase rows (A<->A, B<->C): terminal 1's phases is the
    superset {A, B} = AB; terminal 2's is {A, C} = AC - independently, not a
    single shared set the way a line's phases= would produce."""
    builder = DisconnectorBuilder(network)
    switch = _add(network, builder.create(name='sw1'))
    terminals = builder.add_connectivity(
        switch, node1='busA', node2='busB',
        phaseSide1=['A', 'B'], phaseSide2=['A', 'C'])

    assert terminals[0].phases == network.cim.PhaseCode.AB
    assert terminals[1].phases == network.cim.PhaseCode.AC
    assert len(switch.SwitchPhase) == 2
    rows = [(p.phaseSide1, p.phaseSide2) for p in switch.SwitchPhase]
    assert rows == [
        (network.cim.SinglePhaseKind.A, network.cim.SinglePhaseKind.A),
        (network.cim.SinglePhaseKind.B, network.cim.SinglePhaseKind.C),
    ]


def test_add_connectivity_mismatched_phase_side_lengths_raises(network):
    builder = DisconnectorBuilder(network)
    switch = _add(network, builder.create(name='sw1'))
    with pytest.raises(ValueError, match='parallel lists of equal length'):
        builder.add_connectivity(switch, node1='busA', node2='busB', phaseSide1=['A', 'B'], phaseSide2=['A'])


def test_breaker_builder_add_electrical_writes_shared_and_own_fields(network):
    """BreakerBuilder's add_electrical overrides ProtectedSwitchBuilder's,
    which overrides SwitchBuilder's - each super().add_electrical() call
    layers in its own class's fields on top, all through electrical_balanced
    (the only part module that defines Switch/ProtectedSwitch/Breaker as
    real classes, which is why Breaker - unlike Disconnector/Recloser/
    LoadBreakSwitch - is where this chain actually reaches the graph without
    raising; see switch.py's module docstring)."""
    builder = BreakerBuilder(network)
    switch = _add(network, builder.create(name='brk1'))
    builder.add_connectivity(switch, node1='busA', node2='busB')
    builder.add_electrical(
        switch, ratedCurrent=Qty(600, 'A'), gangOperated=True,
        breakingCapacity=Qty(10000, 'A'), inTransitTime=Qty(0.05, 's'))

    assert switch.ratedCurrent.to('A') == pytest.approx(600)
    assert switch.gangOperated is True
    assert switch.breakingCapacity.to('A') == pytest.approx(10000)
    assert switch.inTransitTime.to('s') == pytest.approx(0.05)


def test_protected_switch_builder_add_electrical(network):
    builder = ProtectedSwitchBuilder(network)
    switch = _add(network, builder.create(name='ps1'))
    builder.add_electrical(switch, breakingCapacity=Qty(5000, 'A'))

    assert switch.breakingCapacity.to('A') == pytest.approx(5000)


@pytest.mark.parametrize('builder_cls', [RecloserBuilder, LoadBreakSwitchBuilder, DisconnectorBuilder])
def test_add_electrical_reachable_on_every_leaf(network, builder_cls):
    """electrical_balanced now defines every leaf class (Disconnector/Fuse/
    ProtectedSwitch/Breaker/LoadBreakSwitch/Recloser/Sectionaliser) after a
    profile rebuild - each as a pure type-tag subclass inheriting
    Switch.ratedCurrent (and ProtectedSwitch.breakingCapacity for the
    protected ones), so add_electrical no longer raises on any of them."""
    builder = builder_cls(network)
    switch = _add(network, builder.create(name='sw1'))
    builder.add_electrical(switch, ratedCurrent=Qty(100, 'A'))

    assert switch.ratedCurrent.to('A') == pytest.approx(100)
