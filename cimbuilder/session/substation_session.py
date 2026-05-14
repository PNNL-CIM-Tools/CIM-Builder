"""SubstationSession — ergonomic wrapper around the topology_builder free functions."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from cimgraph.databases import ConnectionInterface
from cimgraph.models import GraphModel

from cimbuilder.topology_builder.single_bus import (
    new_single_bus_substation,
    add_feeder_to_single_bus,
    add_branch_to_single_bus,
)
from cimbuilder.topology_builder.double_bus_single_breaker import (
    new_double_bus_single_breaker_substation,
    add_feeder_to_double_bus_single_breaker,
    add_branch_to_double_bus_single_breaker,
)
from cimbuilder.topology_builder.main_and_transfer import (
    new_main_and_transfer_substation,
    add_feeder_to_main_and_transfer,
    add_branch_to_main_and_transfer,
)
from cimbuilder.topology_builder.ring_bus import (
    new_ring_bus_substation,
    add_feeder_to_ring_bus,
    add_branch_to_ring_bus,
)
from cimbuilder.topology_builder.sectionalized_bus import (
    new_sectionalized_bus_substation,
    add_feeder_to_sectionalized_bus,
    add_branch_to_sectionalized_bus,
)
from cimbuilder.topology_builder.breaker_and_a_half import (
    new_breaker_and_half_substation,
    add_feeder_to_breaker_and_half,
    add_branch_to_breaker_and_half,
)

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim


@dataclass
class SubstationSession:
    """Ergonomic wrapper that holds substation context across multiple builder calls.

    Don't instantiate directly — use one of the factory classmethods:
    :meth:`single_bus`, :meth:`double_bus_single_breaker`, :meth:`main_and_transfer`,
    :meth:`ring_bus`, :meth:`sectionalized_bus`, :meth:`breaker_and_half`.

    Attributes:
        network:    GraphModel containing the substation.
        substation: The Substation CIM object.
        base_voltage: BaseVoltage for all switching equipment.
        topology:   String key identifying the topology (used for dispatch).
        _buses:     Internal bus references; content depends on topology.
    """
    network: GraphModel
    substation: "cim.Substation"
    base_voltage: "cim.BaseVoltage"
    topology: str
    _buses: dict = field(default_factory=dict, repr=False)

    # ------------------------------------------------------------------
    # Factory classmethods
    # ------------------------------------------------------------------

    @classmethod
    def single_bus(
        cls,
        connection: ConnectionInterface,
        name: str,
        base_voltage: "int | float | cim.BaseVoltage",
        *,
        network: GraphModel | None = None,
    ) -> "SubstationSession":
        """Create a single-bus substation session."""
        result = new_single_bus_substation(connection, name, base_voltage, network=network)
        return cls(
            network=result["network"],
            substation=result["substation"],
            base_voltage=result["base_voltage"],
            topology="single_bus",
            _buses={"main_bus": result["main_bus"]},
        )

    @classmethod
    def double_bus_single_breaker(
        cls,
        connection: ConnectionInterface,
        name: str,
        base_voltage: "int | float | cim.BaseVoltage",
        *,
        network: GraphModel | None = None,
    ) -> "SubstationSession":
        """Create a double-bus single-breaker substation session."""
        result = new_double_bus_single_breaker_substation(connection, name, base_voltage,
                                                          network=network)
        return cls(
            network=result["network"],
            substation=result["substation"],
            base_voltage=result["base_voltage"],
            topology="double_bus_single_breaker",
            _buses={"north_bus": result["north_bus"], "south_bus": result["south_bus"]},
        )

    @classmethod
    def main_and_transfer(
        cls,
        connection: ConnectionInterface,
        name: str,
        base_voltage: "int | float | cim.BaseVoltage",
        *,
        network: GraphModel | None = None,
    ) -> "SubstationSession":
        """Create a main-and-transfer substation session."""
        result = new_main_and_transfer_substation(connection, name, base_voltage, network=network)
        return cls(
            network=result["network"],
            substation=result["substation"],
            base_voltage=result["base_voltage"],
            topology="main_and_transfer",
            _buses={"main_bus": result["main_bus"], "transfer_bus": result["transfer_bus"]},
        )

    @classmethod
    def ring_bus(
        cls,
        connection: ConnectionInterface,
        name: str,
        base_voltage: "int | float | cim.BaseVoltage",
        *,
        total_sections: int = 4,
        network: GraphModel | None = None,
    ) -> "SubstationSession":
        """Create a ring-bus substation session."""
        result = new_ring_bus_substation(connection, name, base_voltage,
                                         total_sections=total_sections, network=network)
        return cls(
            network=result["network"],
            substation=result["substation"],
            base_voltage=result["base_voltage"],
            topology="ring_bus",
            _buses={"buses": result["buses"]},
        )

    @classmethod
    def sectionalized_bus(
        cls,
        connection: ConnectionInterface,
        name: str,
        base_voltage: "int | float | cim.BaseVoltage",
        *,
        total_sections: int = 2,
        network: GraphModel | None = None,
    ) -> "SubstationSession":
        """Create a sectionalized-bus substation session."""
        result = new_sectionalized_bus_substation(connection, name, base_voltage,
                                                   total_sections=total_sections, network=network)
        return cls(
            network=result["network"],
            substation=result["substation"],
            base_voltage=result["base_voltage"],
            topology="sectionalized_bus",
            _buses={"buses": result["buses"]},
        )

    @classmethod
    def breaker_and_half(
        cls,
        connection: ConnectionInterface,
        name: str,
        base_voltage: "int | float | cim.BaseVoltage",
        *,
        total_bus_ties: int = 2,
        network: GraphModel | None = None,
    ) -> "SubstationSession":
        """Create a breaker-and-a-half substation session."""
        result = new_breaker_and_half_substation(connection, name, base_voltage,
                                                  total_bus_ties=total_bus_ties, network=network)
        return cls(
            network=result["network"],
            substation=result["substation"],
            base_voltage=result["base_voltage"],
            topology="breaker_and_half",
            _buses={"bus_tie_junctions": result["bus_tie_junctions"],
                    "main_bus_1": result["main_bus_1"],
                    "main_bus_2": result["main_bus_2"]},
        )

    # ------------------------------------------------------------------
    # Instance methods — dispatch on topology
    # ------------------------------------------------------------------

    def add_feeder(
        self,
        breaker_number: int,
        feeder_network: GraphModel,
        feeder: "cim.Feeder",
        *,
        sourcebus: "cim.ConnectivityNode | None" = None,
        # ring_bus / sectionalized_bus extra args
        bus_number: int | None = None,
        section_number: int | None = None,
        # breaker_and_half extra arg
        tie_number: int | None = None,
    ) -> dict:
        """Add a feeder bay, dispatching to the right topology function.

        Args:
            breaker_number: Integer identifier for the bay (seeds equipment names).
            feeder_network: GraphModel containing the feeder.
            feeder:         Feeder to connect.
            sourcebus:      Optional explicit head ConnectivityNode.
            bus_number:     Ring-bus only — 1-based index into buses list.
            section_number: Sectionalized-bus only — 1-based section index.
            tie_number:     Breaker-and-half only — 0-based tie column index.

        Returns:
            dict from the underlying topology function.
        """
        t = self.topology
        if t == "single_bus":
            return add_feeder_to_single_bus(
                self.network, self.substation, self._buses["main_bus"],
                self.base_voltage, breaker_number, feeder_network, feeder,
                sourcebus,
            )
        if t == "double_bus_single_breaker":
            return add_feeder_to_double_bus_single_breaker(
                self.network, self.substation,
                self._buses["north_bus"], self._buses["south_bus"],
                self.base_voltage, breaker_number, feeder_network, feeder, sourcebus,
            )
        if t == "main_and_transfer":
            return add_feeder_to_main_and_transfer(
                self.network, self.substation,
                self._buses["main_bus"], self._buses["transfer_bus"],
                self.base_voltage, breaker_number, feeder_network, feeder, sourcebus,
            )
        if t == "ring_bus":
            if bus_number is None:
                raise ValueError("ring_bus topology requires bus_number=")
            return add_feeder_to_ring_bus(
                self.network, self.substation, self._buses["buses"],
                self.base_voltage, bus_number, feeder_network, feeder, sourcebus,
            )
        if t == "sectionalized_bus":
            if section_number is None:
                raise ValueError("sectionalized_bus topology requires section_number=")
            return add_feeder_to_sectionalized_bus(
                self.network, self.substation, self._buses["buses"],
                self.base_voltage, section_number, breaker_number, feeder_network, feeder, sourcebus,
            )
        if t == "breaker_and_half":
            if tie_number is None:
                raise ValueError("breaker_and_half topology requires tie_number=")
            return add_feeder_to_breaker_and_half(
                self.network, self.substation, self._buses["bus_tie_junctions"],
                self.base_voltage, breaker_number, tie_number, feeder_network, feeder, sourcebus,
            )
        raise ValueError(f"Unknown topology: {t!r}")

    def add_branch(
        self,
        breaker_number: int,
        branch_terminal: "cim.Terminal",
        *,
        bus_number: int | None = None,
        section_number: int | None = None,
        tie_number: int | None = None,
    ) -> dict:
        """Add a branch bay, dispatching to the right topology function.

        Args:
            breaker_number:  Integer identifier for the bay.
            branch_terminal: Terminal to wire into the takeoff junction.
            bus_number:      Ring-bus only — 1-based bus index.
            section_number:  Sectionalized-bus only — 1-based section index.
            tie_number:      Breaker-and-half only — 0-based tie column index.

        Returns:
            dict from the underlying topology function.
        """
        t = self.topology
        if t == "single_bus":
            return add_branch_to_single_bus(
                self.network, self.substation, self._buses["main_bus"],
                self.base_voltage, breaker_number, branch_terminal,
            )
        if t == "double_bus_single_breaker":
            return add_branch_to_double_bus_single_breaker(
                self.network, self.substation,
                self._buses["north_bus"], self._buses["south_bus"],
                self.base_voltage, breaker_number, branch_terminal,
            )
        if t == "main_and_transfer":
            return add_branch_to_main_and_transfer(
                self.network, self.substation,
                self._buses["main_bus"], self._buses["transfer_bus"],
                self.base_voltage, breaker_number, branch_terminal,
            )
        if t == "ring_bus":
            if bus_number is None:
                raise ValueError("ring_bus topology requires bus_number=")
            return add_branch_to_ring_bus(
                self.network, self.substation, self._buses["buses"],
                self.base_voltage, bus_number, branch_terminal,
            )
        if t == "sectionalized_bus":
            if section_number is None:
                raise ValueError("sectionalized_bus topology requires section_number=")
            return add_branch_to_sectionalized_bus(
                self.network, self.substation, self._buses["buses"],
                self.base_voltage, section_number, breaker_number, branch_terminal,
            )
        if t == "breaker_and_half":
            if tie_number is None:
                raise ValueError("breaker_and_half topology requires tie_number=")
            return add_branch_to_breaker_and_half(
                self.network, self.substation, self._buses["bus_tie_junctions"],
                self.base_voltage, breaker_number, tie_number, branch_terminal,
            )
        raise ValueError(f"Unknown topology: {t!r}")

    def add_linear_shunt_compensator(
        self,
        breaker_number: int,
        name: str,
        *,
        b_per_section: float | None = None,
        g_per_section: float | None = None,
        bus_number: int | None = None,
        section_number: int | None = None,
        tie_number: int | None = None,
    ) -> "cim.LinearShuntCompensator":
        """Add a shunt compensator (capacitor/reactor) bay.

        Creates the branch bay then attaches a LinearShuntCompensator to the
        takeoff junction.

        Args:
            b_per_section: Susceptance per section in S (positive = capacitive).
            g_per_section: Conductance per section in S.
        """
        from cimbuilder.object_builder.shunt.new_linear_shunt_compensator import (
            new_linear_shunt_compensator,
        )
        from cimbuilder._profile import get_cim
        cim = get_cim()

        terminal = cim.Terminal(name=f"{name}_t1")
        terminal.uuid(name=f"{name}_t1")

        bay = self.add_branch(
            breaker_number, terminal,
            bus_number=bus_number,
            section_number=section_number,
            tie_number=tie_number,
        )
        junction = bay["junctions"][-1] if "junctions" in bay else bay["junction"]

        return new_linear_shunt_compensator(
            self.network, self.substation, name, junction,
            base_voltage=self.base_voltage,
            b_per_section=b_per_section,
            g_per_section=g_per_section,
        )

    def upload(self) -> None:
        """Upload the substation network to the backing store."""
        self.network.upload()

    def write_xml(self, filename: str) -> None:
        """Write the substation network to an XML file."""
        from cimgraph import utils as cim_utils
        cim_utils.write_xml(self.network, filename)
