import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH

from cimbuilder.builders.base import ObjectBuilder
from cimtables import graph_write

class EnergyConsumerPhaseBuilder(ObjectBuilder):
    """NOTE: despite the filename (consumer_phase.py, implying a per-phase
    EnergyConsumerPhase builder), this class is named and configured
    identically to load/consumer.py's EnergyConsumerBuilder
    (cim_class_name = 'EnergyConsumer', not 'EnergyConsumerPhase') and
    appears to be an abandoned/incomplete duplicate - see the bug note on
    add_connectivity below."""

    cim_class_name = 'EnergyConsumerPhase'

    def add_connectivity(self, load_phs, *, EnergyConsumer) -> None:
        """Currently a no-op stub (`pass`) - the `EnergyConsumer` parameter
        is accepted but never used, and no connectivity/FK is ever written.
        Calling this does nothing to `load_phs`."""
        pass

    def add_electrical(self, load_phs, *, pfixed=None, qfixed=None, pfixedPct=None, qfixedPct=None) -> None:
        """Adds electrical_unbalanced.EnergyConsumer's fixed-load parameters
        (the unbalanced/per-phase-profile counterpart to
        load/consumer.py's EnergyConsumerBuilder.add_electrical, which uses
        electrical_balanced instead).
        * pfixed: a Qty resolved to ActivePower (W, SI base).
        * qfixed: a Qty resolved to ReactivePower (VAr, SI base).
        * pfixedPct/qfixedPct: Qtys resolved to PerCent (dimensionless, SI base).
        A bare number for any of these is stored unconverted via plain setattr.
        """
        graph_write.set_attr(load_phs, EL_UNBAL, 'pfixed', pfixed)
        graph_write.set_attr(load_phs, EL_UNBAL, 'qfixed', qfixed)
        graph_write.set_attr(load_phs, EL_UNBAL, 'pfixedPct', pfixedPct)
        graph_write.set_attr(load_phs, EL_UNBAL, 'qfixedPct', qfixedPct)