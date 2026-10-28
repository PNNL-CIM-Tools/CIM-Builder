"""Switch builder tests (design: cimbuilder/development/
OBJECT_BUILDER_MIGRATION.md Phase 4, resolved against the Visio modeling
reference diagram (Switch) - see cimbuilder/builders/switch/switch.py's
module docstring for the full field-location evidence).

Covers SwitchBuilder (base) and its subclass chain: ProtectedSwitchBuilder,
BreakerBuilder, RecloserBuilder, LoadBreakSwitchBuilder, DisconnectorBuilder,
FuseBuilder - every leaf except BreakerBuilder is a pure cim_class_name
override, so these tests exercise the inherited methods through each
concrete subclass rather than re-testing SwitchBuilder's logic per class.
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
    FuseBuilder,
    LoadBreakSwitchBuilder,
    RecloserBuilder,
)
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


def test_add_connectivity_builds_two_terminals_with_distinct_names(network):
    """Mirrors the double-UUID bug new_disconnector.py had: t1's name seeded
    twice, t2 never seeded. connectivity.add_connectivity names each
    terminal from its own index, so this can't regress silently."""
    builder = DisconnectorBuilder(network)
    switch = builder.create(name='sw1')
    terminals = builder.add_connectivity(switch, node1='busA', node2='busB')

    assert len(terminals) == 2
    assert terminals[0].name != terminals[1].name
    assert terminals[0].sequenceNumber == 1
    assert terminals[1].sequenceNumber == 2
    assert switch.Terminals == terminals


def test_add_connectivity_builds_phase_children_in_order(network):
    builder = BreakerBuilder(network)
    switch = builder.create(name='brk1')
    terminals = builder.add_connectivity(switch, node1='busA', node2='busB', phases='CB')

    assert [t.phases for t in terminals] == [network.cim.PhaseCode.BC, network.cim.PhaseCode.BC]
    phase_children = switch.SwitchPhase
    assert len(phase_children) == 2
    # SwitchPhase has no sequenceNumber - it carries phaseSide1/phaseSide2
    # instead (both set to the same SinglePhaseKind), per add_phase_children's
    # own handling of that shape.
    assert [p.phaseSide1 for p in phase_children] == [network.cim.SinglePhaseKind.C, network.cim.SinglePhaseKind.B]


def test_add_switching_writes_fields_across_part_modules(network):
    """open -> steady_state_hypothesis; everything else (normalOpen/retained/
    areaBoundary/topologicalUsage/gangOperated/motorOperated/
    remotelyOperated) -> connectivity_unbalanced - the one part module that
    defines every leaf class, so these fields work on any SwitchBuilder
    subclass, unlike ratedCurrent (see switch.py's module docstring)."""
    builder = DisconnectorBuilder(network)
    switch = builder.create(name='sw1')
    builder.add_switching(
        switch, open=True, normalOpen=True, retained=False, areaBoundary=False,
        topologicalUsage='busTie', gangOperated=True, motorOperated=False,
        remotelyOperated=True)

    assert switch.open is True
    assert switch.normalOpen is True
    assert switch.retained is False
    assert switch.areaBoundary is False
    assert switch.topologicalUsage == network.cim.TopologicalUsageKind.busTie
    assert switch.gangOperated is True
    assert switch.motorOperated is False
    assert switch.remotelyOperated is True


def test_protected_switch_builder_adds_breaking_capacity(network):
    """breakingCapacity (electrical_unbalanced.ProtectedSwitch) is only
    reachable on Breaker/LoadBreakSwitch, not Recloser - see switch.py's
    module docstring - so this test uses LoadBreakSwitchBuilder."""
    builder = LoadBreakSwitchBuilder(network)
    switch = builder.create(name='lbs1')
    builder.add_protection(switch, breakingCapacity=Qty(10000, 'A'))

    assert switch.breakingCapacity.to('A') == pytest.approx(10000)


def test_breaker_builder_adds_in_transit_time_on_top_of_inherited_methods(network):
    builder = BreakerBuilder(network)
    switch = builder.create(name='brk1')
    builder.add_connectivity(switch, node1='busA', node2='busB')
    builder.add_switching(switch, open=False)
    builder.add_protection(switch, breakingCapacity=Qty(10000, 'A'))
    builder.add_breaker_rating(switch, inTransitTime=Qty(0.05, 's'))

    assert switch.open is False
    assert switch.breakingCapacity.to('A') == pytest.approx(10000)
    assert switch.inTransitTime.to('s') == pytest.approx(0.05)


def test_recloser_builder_breaking_capacity_not_reachable(network):
    """Documents the real limit confirmed in switch.py's docstring:
    electrical_unbalanced has no Recloser class, so breakingCapacity raises
    on a Recloser instance despite RecloserBuilder inheriting add_protection."""
    builder = RecloserBuilder(network)
    switch = builder.create(name='rec1')
    with pytest.raises(ValueError, match="has no class named 'Recloser'"):
        builder.add_protection(switch, breakingCapacity=Qty(10000, 'A'))


def test_load_break_switch_builder_is_a_pure_subclass(network):
    builder = LoadBreakSwitchBuilder(network)
    switch = builder.create(name='lbs1')
    builder.add_connectivity(switch, node1='busA', node2='busB')
    builder.add_switching(switch, normalOpen=False)
    builder.add_protection(switch, breakingCapacity=Qty(5000, 'A'))

    assert type(switch).__name__ == 'LoadBreakSwitch'
    assert switch.normalOpen is False
    assert switch.breakingCapacity.to('A') == pytest.approx(5000)


def test_fuse_builder_is_a_pure_subclass(network):
    builder = FuseBuilder(network)
    fuse = builder.create(name='fuse1')
    builder.add_connectivity(fuse, node1='busA', node2='busB')
    builder.add_switching(fuse, normalOpen=False, gangOperated=True)

    assert type(fuse).__name__ == 'Fuse'
    assert fuse.normalOpen is False
    assert fuse.gangOperated is True
