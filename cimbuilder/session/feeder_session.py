"""FeederSession — ergonomic wrapper for step-by-step feeder construction."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel, FeederModel
from cimgraph.databases import ConnectionInterface

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim


@dataclass
class FeederSession:
    """Holds feeder context for step-by-step feeder construction.

    Create via :meth:`new` or wrap an existing feeder with :meth:`from_existing`.

    Attributes:
        network:  GraphModel (FeederModel) containing the feeder.
        feeder:   The Feeder CIM object.
    """
    network: GraphModel
    feeder: "cim.Feeder"

    @classmethod
    def new(
        cls,
        connection: ConnectionInterface,
        name: str,
        mRID: str | None = None,
    ) -> "FeederSession":
        """Create a new empty feeder and wrap it in a session.

        Args:
            connection: ConnectionInterface for the new FeederModel.
            name:       Human-readable feeder name.
            mRID:       Optional stable mRID; one is generated if not provided.
        """
        cim = get_cim()
        feeder = cim.Feeder(name=name)
        if mRID:
            feeder.mRID = mRID
        network = FeederModel(connection=connection, container=feeder, distributed=False)
        network.add_to_graph(feeder)
        return cls(network=network, feeder=feeder)

    @classmethod
    def from_existing(
        cls,
        network: GraphModel,
        feeder: "cim.Feeder",
    ) -> "FeederSession":
        """Wrap an already-constructed feeder network."""
        return cls(network=network, feeder=feeder)

    def add_energy_consumer(
        self,
        name: str,
        node: "str | cim.ConnectivityNode",
        *,
        p_kW: float | None = None,
        q_kVAr: float | None = None,
    ) -> "cim.EnergyConsumer":
        """Add an EnergyConsumer to the feeder."""
        from cimbuilder.object_builder.load.new_energy_consumer import new_energy_consumer
        return new_energy_consumer(
            self.network, self.feeder, name, node,
            p_kW=p_kW, q_kVAr=q_kVAr,
        )

    def add_btm_pv(
        self,
        name: str,
        node: "str | cim.ConnectivityNode",
        *,
        p_kW: float | None = None,
        rated_S_kVA: float | None = None,
    ) -> dict:
        """Add a behind-the-meter PV unit (PEC + PhotoVoltaicUnit)."""
        from cimbuilder.composite_builder.btm_pv_unit import new_btm_pv_unit
        return new_btm_pv_unit(
            self.network, self.feeder, name, node,
            p_kW=p_kW, rated_S_kVA=rated_S_kVA,
        )

    def add_battery(
        self,
        name: str,
        node: "str | cim.ConnectivityNode",
        *,
        p_kW: float | None = None,
        rated_S_kVA: float | None = None,
        rated_E_kWh: float | None = None,
    ) -> dict:
        """Add a battery energy storage system (PEC + BatteryUnit)."""
        from cimbuilder.composite_builder.battery_unit import new_battery_unit
        return new_battery_unit(
            self.network, self.feeder, name, node,
            p_kW=p_kW, rated_S_kVA=rated_S_kVA, rated_E_kWh=rated_E_kWh,
        )
