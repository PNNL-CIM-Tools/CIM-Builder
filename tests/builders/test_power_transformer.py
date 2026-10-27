"""PowerTransformerBuilder / TransformerTankConfigurationBuilder tests
(design: cimbuilder/development/OBJECT_BUILDER_MIGRATION.md Phase 1, resolved
against real .cimtbl reference models - see the approved implementation plan
at the time of writing for the full field-location evidence).

Covers all three coexisting impedance representations: PI-direct-on-end
(shape 1, PSS/E), mesh-by-end (shape 2), and mesh-by-winding/template
(shape 3, OpenDSS/reusable templates) - see base.py's module docstring.
"""

import importlib
import tempfile

import pytest
from cimgraph.core.env_vars import get_cim_profile
from cimgraph.databases import XMLFile
from cimgraph.models import BusBranchModel

from cimbuilder.builders.transformer import PowerTransformerBuilder, TransformerTankConfigurationBuilder
from cimtables import graph_write
from cimtables.name_index import NameIndex
from cimtables.units import Qty

# Profile set per test via monkeypatch (+ cache_clear, since get_cim_profile
# is @cache'd with no args - a bare os.environ assignment at module scope
# would leak into every other test file collected in the same pytest
# process). Mirrors cimtables/tests/test_bind_cim18v17.py's cim fixture.


@pytest.fixture
def cim(monkeypatch):
    monkeypatch.setenv('CIMG_CIM_PROFILE', 'cim18v17')
    get_cim_profile.cache_clear()
    yield importlib.import_module('cimprofiles.cim18.cim18v17')
    get_cim_profile.cache_clear()


@pytest.fixture
def network(cim):
    conn = XMLFile(filename=tempfile.mktemp(suffix='.xml'))
    container = cim.Substation(name='test_substation')
    net = BusBranchModel(connection=conn, container=container, distributed=False)
    net.name_index = NameIndex()
    return net


# --- shape 1: PI-direct-on-end ---------------------------------------------

def test_add_connectivity_builds_one_end_per_winding(network, cim):
    builder = PowerTransformerBuilder(network)
    xfmr = builder.create(name='xfmr1')
    ends = builder.add_connectivity(xfmr, ends=[
        {'node': 'busA', 'endNumber': 1, 'connectionKind': 'Y'},
        {'node': 'busB', 'endNumber': 2, 'connectionKind': 'I'},
    ])

    assert len(ends) == 2
    assert ends[0].endNumber == 1
    assert ends[1].endNumber == 2
    assert ends[0].connectionKind == cim.WindingConnection.Y
    assert ends[1].connectionKind == cim.WindingConnection.I
    assert ends[0].Terminal.ConnectivityNode.name == 'busA'
    assert ends[1].Terminal.ConnectivityNode.name == 'busB'
    assert ends[0].PowerTransformer is xfmr
    assert ends[1].PowerTransformer is xfmr


def test_add_connectivity_uses_network_default_container(network):
    builder = PowerTransformerBuilder(network)
    xfmr = builder.create(name='xfmr1')
    builder.add_connectivity(xfmr, ends=[{'node': 'busA', 'endNumber': 1}])
    assert xfmr.EquipmentContainer is network.container


def test_add_electrical_writes_pi_model_values(network):
    builder = PowerTransformerBuilder(network)
    xfmr = builder.create(name='xfmr1')
    end1, end2 = builder.add_connectivity(xfmr, ends=[
        {'node': 'busA', 'endNumber': 1},
        {'node': 'busB', 'endNumber': 2},
    ])
    builder.add_electrical(end1, r=Qty(1.04, 'ohm'), x=Qty(33.4, 'ohm'),
                            b=Qty(-5.6e-6, 'S'), ratedS=Qty(200, 'MVA'), ratedU=Qty(230, 'kV'))
    builder.add_electrical(end2, r=Qty(52, 'ohm'), x=Qty(873, 'ohm'))

    assert end1.r.to('ohm') == pytest.approx(1.04)
    assert end1.x.to('ohm') == pytest.approx(33.4)
    assert end1.b.to('S') == pytest.approx(-5.6e-6)
    assert end1.ratedS.to('MVA') == pytest.approx(200)
    assert end1.ratedU.to('kV') == pytest.approx(230)
    assert end2.r.to('ohm') == pytest.approx(52)
    assert end2.x.to('ohm') == pytest.approx(873)
    # add_electrical never touches endNumber/connectionKind/Terminal
    assert end1.endNumber == 1


# --- shape 2: mesh-by-end ---------------------------------------------------

def test_add_mesh_impedance_between_two_ends(network):
    builder = PowerTransformerBuilder(network)
    xfmr = builder.create(name='xfmr1')
    end1, end2, end3 = builder.add_connectivity(xfmr, ends=[
        {'node': 'busA', 'endNumber': 1},
        {'node': 'busB', 'endNumber': 2},
        {'node': 'busC', 'endNumber': 3},
    ])
    mesh = builder.add_mesh_impedance(
        xfmr, FromTransformerEnd=end1.name, ToTransformerEnd=end2.name, r=Qty(34, 'ohm'), x=Qty(456, 'ohm'))

    assert mesh.FromTransformerEnd is end1
    assert mesh.ToTransformerEnd is end2
    assert mesh.r.to('ohm') == pytest.approx(34)
    assert mesh.x.to('ohm') == pytest.approx(456)
    assert mesh in end1.FromMeshImpedance
    assert mesh in end2.ToMeshImpedance


def test_add_mesh_impedance_unresolved_end_raises(network):
    builder = PowerTransformerBuilder(network)
    xfmr = builder.create(name='xfmr1')
    builder.add_connectivity(xfmr, ends=[{'node': 'busA', 'endNumber': 1}])
    with pytest.raises(ValueError, match='not both found'):
        builder.add_mesh_impedance(xfmr, FromTransformerEnd='xfmr1_end1', ToTransformerEnd='does_not_exist', r=1)


# --- add_tank / add_tap_changer --------------------------------------------

def test_add_tank_resolves_template_by_name(network):
    config_builder = TransformerTankConfigurationBuilder(network)
    config = config_builder.create(name='padmount_1ph_250kva')
    graph_write.add_to_graph(network, config)

    builder = PowerTransformerBuilder(network)
    xfmr = builder.create(name='padmount_2341')
    tank = builder.add_tank(xfmr, name='padmount_2341_tank', TankConfiguration='padmount_1ph_250kva')

    assert tank.PowerTransformer is xfmr
    assert tank.TankConfiguration is config


def test_add_tank_missing_template_raises(network):
    builder = PowerTransformerBuilder(network)
    xfmr = builder.create(name='xfmr1')
    with pytest.raises(ValueError, match='TankConfiguration'):
        builder.add_tank(xfmr, name='tank1', TankConfiguration='does_not_exist')


def test_add_tap_changer_builds_ratio_tap_changer(network):
    builder = PowerTransformerBuilder(network)
    xfmr = builder.create(name='xfmr1')
    [end1] = builder.add_connectivity(xfmr, ends=[{'node': 'busA', 'endNumber': 1}])
    tap_changer = builder.add_tap_changer(end1, highStep=16, lowStep=-16, initialDelay=Qty(30, 's'))

    assert tap_changer.highStep == 16
    assert tap_changer.lowStep == -16
    assert tap_changer.initialDelay.to('s') == pytest.approx(30)
    assert end1.RatioTapChanger is tap_changer
    assert tap_changer.TransformerEnd is end1


# --- shape 3: mesh-by-winding / template ------------------------------------

def test_template_tier_builds_the_ct5_pole_top_example(network):
    """Mirrors /home/ande188/CIMTBL-Models/distribution/IEEE/IEEE13_CDPSM/xfmrcodes.cimtbl's
    ct5 example end to end via the direct/manual API."""
    builder = TransformerTankConfigurationBuilder(network)
    config = builder.create(name='ct5')
    graph_write.add_to_graph(network, config)
    builder.add_rating(config, percentImpedance=Qty(2.08, 'percent'),
                        percentMagnetizingCurrent=Qty(0.5, 'percent'),
                        noLoadLoss=Qty(10, 'W'), loadLoss=Qty(60, 'W'))

    h1 = builder.add_phase_end(config, name='ct5_h1', endNumber=1, sequenceNumber=1,
                                phase='X', phaseNeutralU=Qty(2400, 'V'))
    x1 = builder.add_phase_end(config, name='ct5_x1', endNumber=2, sequenceNumber=2,
                                phase='s1', phaseNeutralU=Qty(120, 'V'))
    n = builder.add_phase_end(config, name='ct5_n', endNumber=2, sequenceNumber=4,
                               phase='N', phaseNeutralU=Qty(0, 'V'))

    wdg1 = builder.add_winding(config, name='ct5_wdg1', ratedS=Qty(5, 'kVA'), baseS=Qty(5, 'kVA'),
                                ratedU=Qty(4160, 'V'), baseU=Qty(2400, 'V'), r=Qty(0.6, 'percent'),
                                FromTransformerEnd='ct5_h1', ToTransformerEnd='ct5_n')
    wdg2 = builder.add_winding(config, name='ct5_wdg2', ratedS=Qty(2.5, 'kVA'), baseS=Qty(5, 'kVA'),
                                ratedU=Qty(240, 'V'), baseU=Qty(120, 'V'), r=Qty(1.2, 'percent'),
                                FromTransformerEnd='ct5_x1', ToTransformerEnd='ct5_n')

    mesh = builder.add_mesh_impedance(FromWinding='ct5_wdg1', ToWinding='ct5_wdg2', x=Qty(2.04, 'percent'))

    assert config.TransformerPhaseEnd == [h1, x1, n]
    assert wdg1.FromTransformerEnd is h1
    assert wdg1.ToTransformerEnd is n
    assert wdg1.TankConfiguration is config
    # r=0.6% on wdg1 (baseU=2400V, baseS=5kVA) -> z_base = 2400**2/5000 = 1152 ohm
    assert wdg1.r.to('ohm') == pytest.approx(0.006 * (2400 ** 2 / 5000))
    assert mesh.FromWinding is wdg1
    assert mesh.ToWinding is wdg2
    # x=2.04% on the mesh, z_base from FromWinding (wdg1): same 1152 ohm base
    assert mesh.x.to('ohm') == pytest.approx(0.0204 * (2400 ** 2 / 5000))


def test_add_tank_references_template_built_separately(network, cim):
    """The instance tier (padmount_example.cimtbl's shape): a bare
    PowerTransformer + PowerTransformerEnd connectivity + a TransformerTank
    referencing a template built by TransformerTankConfigurationBuilder."""
    config_builder = TransformerTankConfigurationBuilder(network)
    config = config_builder.create(name='padmount_1ph_250kva')
    graph_write.add_to_graph(network, config)
    config_builder.add_rating(config, percentImpedance=Qty(2.56, 'percent'),
                               noLoadLoss=Qty(310, 'W'), loadLoss=Qty(2050, 'W'))

    xfmr_builder = PowerTransformerBuilder(network)
    xfmr = xfmr_builder.create(name='padmount_2341')
    ends = xfmr_builder.add_connectivity(xfmr, ends=[
        {'node': 'cn_2341_hv', 'endNumber': 1, 'connectionKind': 'Y'},
        {'node': 'cn_2341_lv', 'endNumber': 2, 'connectionKind': 'I'},
    ])
    tank = xfmr_builder.add_tank(xfmr, name='padmount_2341_tank', TankConfiguration='padmount_1ph_250kva')

    assert tank.PowerTransformer is xfmr
    assert tank.TankConfiguration is config
    assert ends[0].connectionKind == cim.WindingConnection.Y
    # the instance carries no impedance at all - that's entirely on the template
    assert ends[0].r is None
