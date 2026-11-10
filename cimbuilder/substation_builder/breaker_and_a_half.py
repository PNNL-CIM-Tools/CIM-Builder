import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN

from cimbuilder.object_builder.switch import DisconnectorBuilder
from cimbuilder.substation_builder.substation_builder import SubstationBuilder

mRID = str


class BreakerAndHalfSubstationBuilder(SubstationBuilder):
    """
    Breaker-and-a-half layout: buses <vl>_bus_1 and <vl>_bus_2 joined by diameters of three breaker
    bays in series, bus_1 - bay - side_1 - bay - side_2 - bay - bus_2, two branches per diameter
    (one on each side node), so each branch shares its middle breaker with its neighbour.
    See SubstationBuilder for the call order.
    """

    def _side_node(self, voltage_level: CN.VoltageLevel, diameter: int, side: int) -> mRID:
        """mRID of the branch connection point on a diameter, <vl>_dia_<diameter>_side_<side>"""
        return f"{voltage_level.mRID}_dia_{diameter}_side_{side}"

    def add_buses(
        self, voltage_level: CN.VoltageLevel, *, diameters: int = 2
    ) -> tuple[CN.VoltageLevel, list[CN.BusbarSection], list[CN.Switch]]:
        """
        Adds the two buses and the diameters between them. Returns the voltage level, its busbars
        and its diameter switches
        * diameters: number of diameters, each takes two branches
        """
        bus1 = self._bus_node(voltage_level, 1)
        bus2 = self._bus_node(voltage_level, 2)
        busbars = [self._add_busbar(voltage_level, bus1), self._add_busbar(voltage_level, bus2)]

        switches = []
        for diameter in range(1, diameters + 1):
            prefix = f"{voltage_level.mRID}_dia_{diameter}"
            side1 = self._side_node(voltage_level, diameter, 1)
            side2 = self._side_node(voltage_level, diameter, 2)
            switches += self._add_breaker_bay(
                voltage_level, prefix=f"{prefix}_1", node1=bus1, node2=side1
            )
            switches += self._add_breaker_bay(
                voltage_level, prefix=f"{prefix}_2", node1=side1, node2=side2
            )
            switches += self._add_breaker_bay(
                voltage_level, prefix=f"{prefix}_3", node1=side2, node2=bus2
            )
        return voltage_level, busbars, switches

    def add_branch(
        self, voltage_level: CN.VoltageLevel, *, diameter: int, side: int, node: mRID
    ) -> tuple[CN.VoltageLevel, list[CN.Switch]]:
        """
        Connects node to one side of a diameter through a disconnector <vl>_dia_<diameter>_side_<side>_d
        * diameter: diameter number, 1 .. diameters
        * side: 1 (next to bus_1) or 2 (next to bus_2)
        * node: mRID of the branch ConnectivityNode (e.g. a feeder head node), created if missing
        """
        if side not in (1, 2):
            raise ValueError(f"side must be 1 or 2, got {side}")
        side_node = self._require_node(self._side_node(voltage_level, diameter, side))
        disconnector = self._add_switch(
            DisconnectorBuilder,
            voltage_level,
            mRID=f"{side_node}_d",
            node1=side_node,
            node2=node,
        )
        return voltage_level, [disconnector]
