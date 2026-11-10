import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN

from cimbuilder.substation_builder.substation_builder import SubstationBuilder

mRID = str


class SingleBusSubstationBuilder(SubstationBuilder):
    """
    Single bus layout: one bus <vl>_bus_1, each branch through its own breaker bay.
    See SubstationBuilder for the call order.
    """

    def add_buses(
        self, voltage_level: CN.VoltageLevel
    ) -> tuple[CN.VoltageLevel, list[CN.BusbarSection], list[CN.Switch]]:
        """Adds the bus. Returns the voltage level, its busbars and its bus tie switches (none)"""
        busbar = self._add_busbar(voltage_level, self._bus_node(voltage_level, 1))
        return voltage_level, [busbar], []

    def add_branch(
        self, voltage_level: CN.VoltageLevel, *, number: int, node: mRID
    ) -> tuple[CN.VoltageLevel, list[CN.Switch]]:
        """
        Connects node to the bus through bus - disconnector - breaker - disconnector - node
        * number: bay number, unique within the voltage level, prefixes the bay mRIDs <vl>_<number>
        * node: mRID of the branch ConnectivityNode (e.g. a feeder head node), created if missing
        """
        bus = self._require_node(self._bus_node(voltage_level, 1))
        switches = self._add_breaker_bay(
            voltage_level, prefix=f"{voltage_level.mRID}_{number}", node1=bus, node2=node
        )
        return voltage_level, switches
