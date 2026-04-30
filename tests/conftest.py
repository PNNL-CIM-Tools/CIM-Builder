"""Shared pytest fixtures for CIM-Builder tests.

See ``.development/STYLE_GUIDE.md`` for test conventions.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from cimgraph.databases import XMLFile, get_cim_profile
from cimgraph.models import DistributedArea, FeederModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2023 as cim


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Ensure CIMG_CIM_PROFILE is set to cimhub_2023 for every test."""
    monkeypatch.setenv("CIMG_CIM_PROFILE", "cimhub_2023")
    yield


@pytest.fixture
def cim_profile():
    """Return the active CIM profile module."""
    return get_cim()


@pytest.fixture
def tmp_xml(tmp_path):
    """Return (path, XMLFile) for a temp XML destination."""
    path = tmp_path / "test.xml"
    return path, XMLFile(filename=str(path))


@pytest.fixture
def simple_substation_network(tmp_path):
    """Create a DistributedArea with an empty Substation and one BaseVoltage.

    Returns a dict::

        {
            'network': GraphModel,
            'substation': cim.Substation,
            'base_voltage': cim.BaseVoltage,
            'connection': XMLFile,
            'path': Path,
        }
    """
    cim = get_cim()
    path = tmp_path / "simple_substation.xml"
    connection = XMLFile(filename=str(path))

    substation = cim.Substation(name="test_sub")
    substation.uuid(name="test_sub")

    network = DistributedArea(
        connection=connection,
        container=substation,
        distributed=False,
    )
    network.add_to_graph(substation)

    bv = cim.BaseVoltage(name="BaseV_115000", nominalVoltage=115000)
    bv.uuid(name="BaseV_115000")
    network.add_to_graph(bv)

    return {
        "network": network,
        "substation": substation,
        "base_voltage": bv,
        "connection": connection,
        "path": path,
    }


@pytest.fixture
def connectivity_nodes(simple_substation_network):
    """Create two ConnectivityNodes in simple_substation_network.

    Returns a dict ``{'node1': ..., 'node2': ...}``.
    """
    cim = get_cim()
    net = simple_substation_network["network"]
    sub = simple_substation_network["substation"]

    n1 = cim.ConnectivityNode(name="node1")
    n1.uuid(name="node1")
    n1.ConnectivityNodeContainer = sub
    net.add_to_graph(n1)

    n2 = cim.ConnectivityNode(name="node2")
    n2.uuid(name="node2")
    n2.ConnectivityNodeContainer = sub
    net.add_to_graph(n2)

    return {"node1": n1, "node2": n2}


@pytest.fixture
def minimal_feeder(tmp_path):
    """Create a minimal feeder network with a single sourcebus + EnergySource.

    Returns ``(feeder, feeder_network)``.
    """
    cim = get_cim()
    path = tmp_path / "minimal_feeder.xml"
    connection = XMLFile(filename=str(path))

    feeder = cim.Feeder(mRID="TEST-FEEDER-001")
    feeder.name = "test_feeder"
    feeder_network = FeederModel(
        connection=connection,
        container=feeder,
        distributed=False,
    )

    source_node = cim.ConnectivityNode(name="sourcebus")
    source_node.ConnectivityNodeContainer = feeder
    feeder_network.add_to_graph(source_node)

    energy_source = cim.EnergySource(name="source")
    energy_source.EquipmentContainer = feeder
    terminal = cim.Terminal(name="source_t1", sequenceNumber=1)
    terminal.ConnectivityNode = source_node
    terminal.ConductingEquipment = energy_source
    energy_source.Terminals.append(terminal)
    feeder_network.add_to_graph(energy_source)
    feeder_network.add_to_graph(terminal)

    feeder.NormalHeadTerminal = terminal
    feeder_network.add_to_graph(feeder)

    return feeder, feeder_network
