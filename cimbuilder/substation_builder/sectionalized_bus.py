import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN

from cimbuilder.substation_builder.substation_builder import SubstationBuilder

mRID = str


class SectionalizedBusSubstationBuilder(SubstationBuilder):
    """
    Sectionalized bus layout: buses <vl>_bus_1 .. <vl>_bus_<n> in a line, each adjacent pair joined
    by a bus tie breaker bay, each branch through its own breaker bay to one section.
    See SubstationBuilder for the call order.
    """

    def add_buses(
        self, voltage_level: CN.VoltageLevel, *, sections: int = 2
    ) -> tuple[CN.VoltageLevel, list[CN.BusbarSection], list[CN.Switch]]:
        """
        Adds the bus sections and the bus ties between them. Returns the voltage level, its busbars
        and its bus tie switches
        * sections: number of bus sections
        """
        busbars = []
        for section in range(1, sections + 1):
            busbars.append(self._add_busbar(voltage_level, self._bus_node(voltage_level, section)))

        switches = []
        for section in range(1, sections):
            switches += self._add_breaker_bay(
                voltage_level,
                prefix=f"{voltage_level.mRID}_tie_{section}",
                node1=self._bus_node(voltage_level, section),
                node2=self._bus_node(voltage_level, section + 1),
            )
        return voltage_level, busbars, switches

    def add_branch(
        self, voltage_level: CN.VoltageLevel, *, section: int, number: int, node: mRID
    ) -> tuple[CN.VoltageLevel, list[CN.Switch]]:
        """
        Connects node to one bus section through bus - disconnector - breaker - disconnector - node
        * section: bus section number, 1 .. sections
        * number: bay number, unique within the voltage level, prefixes the bay mRIDs <vl>_<number>
        * node: mRID of the branch ConnectivityNode (e.g. a feeder head node), created if missing
        """
        bus = self._require_node(self._bus_node(voltage_level, section))
        switches = self._add_breaker_bay(
            voltage_level, prefix=f"{voltage_level.mRID}_{number}", node1=bus, node2=node
        )
        return voltage_level, switches
