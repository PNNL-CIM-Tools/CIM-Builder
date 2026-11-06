import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.inverter import (
    PowerElectronicsConnectionBuilder,
    PowerElectronicsConnectionPhaseBuilder,
)


def test_power_electronics_connection_phase_add_connectivity_phase_not_wrapped_in_enum(
    network, container
):
    """add_connectivity calls
    graph_write.set_attr(inverter_phs, CN, "phase", phase) with the raw
    `phase` string, instead of wrapping it as cn.SinglePhaseKind(phase) the
    way e.g. switch_phase.py's add_connectivity does for phaseSide1/2.
    CN.PowerElectronicsConnectionPhase.phase is a SinglePhaseKind-typed
    field, so set_attr's own type check rejects the plain str - this is
    unconditional (phase isn't optional) and raises for every call."""
    pec_builder = PowerElectronicsConnectionBuilder(network=network, container=container)
    pec = pec_builder.create(mRID="pec1", name="pec1")

    phs_builder = PowerElectronicsConnectionPhaseBuilder(network=network, container=container)
    phs = phs_builder.create(mRID="pec1_A")

    with pytest.raises(TypeError, match="SinglePhaseKind"):
        phs_builder.add_connectivity(phs, "A", pec.mRID)


def test_power_electronics_connection_phase_add_ssh(network, container):
    phs_builder = PowerElectronicsConnectionPhaseBuilder(network=network, container=container)
    phs = phs_builder.create(mRID="pec1_A")

    phs_builder.add_ssh(phs, p=Qty(-100, "kW"), q=Qty(-20, "kVAr"))
    assert float(phs.p.to("kW")) == -100
