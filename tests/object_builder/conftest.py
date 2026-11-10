"""Shared fixtures for exercising every cimbuilder.object_builder.*Builder
method against a real cim18v17 FeederModel graph, so any hand-typed CIM
attribute/association name that doesn't exist on the target profile class
fails loudly (ValueError from cimtables.graph_write) instead of silently.
"""
import os

import pytest

os.environ.setdefault("CIMG_CIM_PROFILE", "cim18v17")
os.environ.setdefault("CIMG_USE_UNITS", "TRUE")
os.environ.setdefault("CIMG_SYSTEM_MVA_BASE", "100")

import cimprofiles.cim18.cim18v17 as cim
from cimgraph.models import FeederModel
from cimtables.units import Qty


@pytest.fixture
def network():
    feeder = cim.Feeder(name="test_feeder")
    net = FeederModel(container=feeder, connection=None)
    net.add_to_graph(feeder)
    return net


@pytest.fixture
def container(network):
    return network.container


@pytest.fixture
def base_voltage(network, container):
    from cimbuilder.object_builder.base import BaseVoltageBuilder

    builder = BaseVoltageBuilder(network=network, container=container)
    return builder.create(mRID="bv_12_47kV", nominalVoltage=Qty(12.47, "kV"))
