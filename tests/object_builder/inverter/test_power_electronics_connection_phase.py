import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.inverter import (
    PowerElectronicsConnectionBuilder,
    PowerElectronicsConnectionPhaseBuilder,
)


def test_power_electronics_connection_phase_add_connectivity_phase_wrapped_in_enum(
    network, container
):
    pec_builder = PowerElectronicsConnectionBuilder(network=network, container=container)
    pec = pec_builder.create(mRID="pec1", name="pec1")

    phs_builder = PowerElectronicsConnectionPhaseBuilder(network=network, container=container)
    phs = phs_builder.create(mRID="pec1_A")

    phs_builder.add_connectivity(phs, "A", pec.mRID)

    assert phs.phase == network.cim.SinglePhaseKind("A")


def test_power_electronics_connection_phase_add_ssh(network, container):
    phs_builder = PowerElectronicsConnectionPhaseBuilder(network=network, container=container)
    phs = phs_builder.create(mRID="pec1_A")

    phs_builder.add_ssh(phs, p=Qty(-100, "kW"), q=Qty(-20, "kVAr"))
    assert float(phs.p.to("kW")) == -100
