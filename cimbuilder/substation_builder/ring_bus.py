import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN

from cimbuilder.object_builder.switch import DisconnectorBuilder
from cimbuilder.substation_builder.substation_builder import SubstationBuilder

mRID = str


class RingBusSubstationBuilder(SubstationBuilder):
    """
    Ring bus layout: buses <vl>_bus_1 .. <vl>_bus_<n> closed in a ring by a breaker bay between each
    adjacent pair, each branch through a single disconnector to one bus.
    See SubstationBuilder for the call order.
    """

    def add_buses(
        self, voltage_level: CN.VoltageLevel, *, sections: int = 4
    ) -> tuple[CN.VoltageLevel, list[CN.BusbarSection], list[CN.Switch]]:
        """
        Adds the ring buses and the breaker bays between them. Returns the voltage level, its
        busbars and its ring switches
        * sections: number of buses in the ring, at least 3
        """
        if sections < 3:
            raise ValueError(f"a ring bus needs at least 3 sections, got {sections}")

        busbars = []
        for section in range(1, sections + 1):
            busbars.append(self._add_busbar(voltage_level, self._bus_node(voltage_level, section)))

        switches = []
        for section in range(1, sections + 1):
            next_section = section % sections + 1
            switches += self._add_breaker_bay(
                voltage_level,
                prefix=f"{voltage_level.mRID}_ring_{section}",
                node1=self._bus_node(voltage_level, section),
                node2=self._bus_node(voltage_level, next_section),
            )
        return voltage_level, busbars, switches

    def add_branch(
        self, voltage_level: CN.VoltageLevel, *, section: int, node: mRID
    ) -> tuple[CN.VoltageLevel, list[CN.Switch]]:
        """
        Connects node to one ring bus through a disconnector <vl>_<section>_d
        * section: ring bus number, 1 .. sections
        * node: mRID of the branch ConnectivityNode (e.g. a feeder head node), created if missing
        """
        bus = self._require_node(self._bus_node(voltage_level, section))
        disconnector = self._add_switch(
            DisconnectorBuilder,
            voltage_level,
            mRID=f"{voltage_level.mRID}_{section}_d",
            node1=bus,
            node2=node,
        )
        return voltage_level, [disconnector]
