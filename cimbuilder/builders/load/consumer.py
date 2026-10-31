import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH

from cimbuilder.builders.base import ObjectBuilder
from cimtables import connectivity, graph_write


class EnergyConsumerBuilder(ObjectBuilder):
    cim_class_name = 'EnergyConsumer'

    def add_connectivity(self, load, *, node: str, container: object = None,
                          phaseConnection=None, grounded=None, customerCount=None, BaseVoltage=None) -> None:
        """Adds connectivity_unbalanced profile layer: terminal/node, phase
        connection, grounding, and base voltage.
        * node: mRID of the ConnectivityNode/TopologicalNode to connect to.
          Auto-vivified (an empty node with just that mRID) if not already
          in the graph - not a required-FK-raises-if-missing lookup.
        * container: a live EquipmentContainer object, NOT an mRID string -
          falls back to `self.container` if omitted.
        * phaseConnection: string value of
          connectivity_unbalanced.PhaseShuntConnectionKind (e.g. 'Y', 'D') -
          passed straight to set_attr with NO enum conversion, unlike the
          other builders in this package (e.g. WireConfigurationBuilder
          wraps its enum params in `self.cim.<Kind>(...)` first); if a bare
          string is passed here, set_attr will raise ValueError when the
          enum validation inside the generated CIM class rejects it, or it
          will be stored as a worse-than-useless literal str on a field
          typed as an enum. Likely a doc/behavior mismatch worth fixing
          separately.
        * grounded: plain bool, no unit wrapping.
        * customerCount: plain int, no unit wrapping.
        * BaseVoltage: mRID string of an existing BaseVoltage; resolved via
          set_assc_from_mrid, which raises ValueError if it's not already in
          the graph.

        Returns None (the created Terminal is not returned here, unlike
        ACLineSegmentBuilder.add_connectivity).
        """
        connectivity.add_connectivity(
            self.network, load, node_cols={'node': node},
            container=container if container is not None else self.container)
        graph_write.set_attr(load, CN, 'customerCount', customerCount)
        graph_write.set_attr(load, CN, 'grounded', grounded)
        graph_write.set_attr(load, CN, 'phaseConnection', phaseConnection)
        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(self.network, load, CN, 'BaseVoltage', self.cim.BaseVoltage, BaseVoltage)

    def add_electrical(self, load, *, pfixed=None, qfixed=None, pfixedPct=None, qfixedPct=None, LoadResponse=None) -> None:
        """Adds electrical_balanced.EnergyConsumer's fixed-load parameters.
        * pfixed: a Qty resolved to ActivePower (W, SI base) - e.g. Qty(5, 'kW').
        * qfixed: a Qty resolved to ReactivePower (VAr, SI base).
        * pfixedPct: a Qty resolved to PerCent (dimensionless, SI base) -
          fixed real power as a percentage of rated/nominal load.
        * qfixedPct: a Qty resolved to PerCent (dimensionless, SI base) -
          fixed reactive power as a percentage.
        A bare number for any of these is stored unconverted via plain
        setattr.
        * LoadResponse: mRID string of an existing LoadResponseCharacteristic;
          resolved via set_assc_from_mrid, which raises ValueError if it's
          not already in the graph. Left unset entirely when omitted.
        """
        graph_write.set_attr(load, EL_BAL, 'pfixed', pfixed)
        graph_write.set_attr(load, EL_BAL, 'qfixed', qfixed)
        graph_write.set_attr(load, EL_BAL, 'pfixedPct', pfixedPct)
        graph_write.set_attr(load, EL_BAL, 'qfixedPct', qfixedPct)

        if LoadResponse is not None:
            graph_write.set_assc_from_mrid(
                self.network, load, EL_BAL, 'LoadResponse', self.cim.LoadResponseCharacteristic, LoadResponse)

    def add_ssh(self, load, *, p=None, q=None) -> None:
        """Adds steady_state_hypothesis.EnergyConsumer's solved operating
        point (the SSH-profile counterpart to add_electrical's fixed/nameplate values).
        * p: a Qty resolved to ActivePower (W, SI base).
        * q: a Qty resolved to ReactivePower (VAr, SI base).
        A bare number for either is stored unconverted via plain setattr.
        """
        graph_write.set_attr(load, SSH, 'p', p)
        graph_write.set_attr(load, SSH, 'q', q)

