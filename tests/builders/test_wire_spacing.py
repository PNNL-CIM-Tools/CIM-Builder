"""WireConfigurationBuilder / ConductorDistanceSpacingBuilder /
XYSpacingBuilder tests (design: cimbuilder/development/
OBJECT_BUILDER_MIGRATION.md Phase 3, resolved against Visio modeling
reference diagrams LineModel04/05 - see the approved implementation plan at
the time of writing for the full field-location evidence).

Covers shape 5 (wire geometry reference): ACLineSegmentBuilder.add_wire_configuration
referencing a WireConfiguration template whose WireSpacing is either a
ConductorDistanceSpacing (LineModel04, GridLAB-D line_spacing equivalent) or
an XYSpacing (LineModel05, OpenDSS LineSpacing/LineGeometry equivalent) - see
cimbuilder/builders/line/base.py's and by_template.py's module docstrings.
"""

import importlib
import tempfile

import pytest
from cimgraph.core.env_vars import get_cim_profile
from cimgraph.databases import XMLFile
from cimgraph.models import BusBranchModel

from cimbuilder.builders.line import (
    ACLineSegmentBuilder,
    ConductorDistanceSpacingBuilder,
    WireConfigurationBuilder,
    XYSpacingBuilder,
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


# --- LineModel04: ConductorDistanceSpacing (GridLAB-D line_spacing) --------

def test_conductor_distance_spacing_builds_pairs(network):
    """Mirrors LineModel04's GridLAB-D example: object line_spacing:12 with
    distance_AB/distance_BC/distance_AC/... pairs."""
    spacing_builder = ConductorDistanceSpacingBuilder(network)
    spacing = spacing_builder.create(name='line_spacing_500')
    graph_write.add_to_graph(network, spacing)

    ab = spacing_builder.add_conductor_distance(
        spacing, sequenceNumber1=1, sequenceNumber2=2, distance=Qty(60.5, 'in'))
    bc = spacing_builder.add_conductor_distance(
        spacing, sequenceNumber1=2, sequenceNumber2=3, distance=Qty(60.5, 'in'))

    assert ab.sequenceNumber1 == 1
    assert ab.sequenceNumber2 == 2
    assert ab.distance.to('in') == pytest.approx(60.5)
    assert ab.ConductorDistanceSpacing is spacing
    assert bc.ConductorDistanceSpacing is spacing
    assert spacing.ConductorDistance == [ab, bc]


def test_wire_configuration_references_conductor_distance_spacing(network):
    spacing_builder = ConductorDistanceSpacingBuilder(network)
    spacing = spacing_builder.create(name='line_spacing_500')
    graph_write.add_to_graph(network, spacing)
    spacing_builder.add_conductor_distance(spacing, sequenceNumber1=1, sequenceNumber2=2, distance=Qty(60.5, 'in'))

    config_builder = WireConfigurationBuilder(network)
    config = config_builder.create(name='wireconfig_500')
    graph_write.add_to_graph(network, config)
    config_builder.add_rating(config, numberOfPhases=4, WireSpacing='line_spacing_500')

    assert config.WireSpacing is spacing
    assert config in spacing.WireConfiguration


# --- LineModel05: XYSpacing (OpenDSS LineSpacing/LineGeometry) -------------

def test_xy_spacing_builds_conductor_positions(network):
    """Mirrors LineModel05's OpenDSS example: LineGeometry.3PH_H-4_ACSR4...
    with cond=1..4 x=/h= positions."""
    spacing_builder = XYSpacingBuilder(network)
    spacing = spacing_builder.create(name='geometry_3ph_h4')
    graph_write.add_to_graph(network, spacing)

    cond1 = spacing_builder.add_conductor_position(
        spacing, sequenceNumber=1, xCoord=Qty(-0.6096, 'm'), yCoord=Qty(9.7536, 'm'))
    cond2 = spacing_builder.add_conductor_position(
        spacing, sequenceNumber=2, xCoord=Qty(0.1524, 'm'), yCoord=Qty(10.3632, 'm'))

    assert cond1.sequenceNumber == 1
    assert cond1.xCoord.to('m') == pytest.approx(-0.6096)
    assert cond1.yCoord.to('m') == pytest.approx(9.7536)
    assert cond1.XYSpacing is spacing
    assert cond2.XYSpacing is spacing
    assert spacing.XYConductorPosition == [cond1, cond2]


def test_wire_configuration_references_xy_spacing(network):
    spacing_builder = XYSpacingBuilder(network)
    spacing = spacing_builder.create(name='geometry_3ph_h4')
    graph_write.add_to_graph(network, spacing)
    spacing_builder.add_conductor_position(spacing, sequenceNumber=1, xCoord=Qty(-0.6096, 'm'), yCoord=Qty(9.7536, 'm'))

    config_builder = WireConfigurationBuilder(network)
    config = config_builder.create(name='wireconfig_geometry')
    graph_write.add_to_graph(network, config)
    config_builder.add_rating(config, numberOfPhases=3, installationType='overheadBare',
                               usage='distribution', WireSpacing='geometry_3ph_h4')

    assert config.WireSpacing is spacing
    assert config.installationType == network.cim.WireInstallationKind.overheadBare
    assert config.usage == network.cim.WireUsageKind.distribution


# --- ACLineSegmentBuilder.add_wire_configuration ---------------------------

def test_ac_line_segment_references_wire_configuration(network):
    spacing_builder = XYSpacingBuilder(network)
    spacing = spacing_builder.create(name='geometry_3ph_h4')
    graph_write.add_to_graph(network, spacing)

    config_builder = WireConfigurationBuilder(network)
    config = config_builder.create(name='wireconfig_geometry')
    graph_write.add_to_graph(network, config)
    config_builder.add_rating(config, WireSpacing='geometry_3ph_h4')

    line_builder = ACLineSegmentBuilder(network)
    line = line_builder.create(name='632670')
    target = line_builder.add_wire_configuration(line, WireConfiguration='wireconfig_geometry')

    assert target is config
    assert line.WireConfiguration is config


def test_add_wire_configuration_missing_template_raises(network):
    builder = ACLineSegmentBuilder(network)
    line = builder.create(name='line1')
    with pytest.raises(ValueError, match='not found in graph'):
        builder.add_wire_configuration(line, WireConfiguration='does_not_exist')


def test_add_rating_missing_wire_spacing_raises(network):
    builder = WireConfigurationBuilder(network)
    config = builder.create(name='wireconfig1')
    graph_write.add_to_graph(network, config)
    with pytest.raises(ValueError, match='not found in graph'):
        builder.add_rating(config, WireSpacing='does_not_exist')
