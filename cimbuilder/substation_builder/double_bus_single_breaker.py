import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN

from cimbuilder.object_builder.switch import BreakerBuilder, DisconnectorBuilder
from cimbuilder.substation_builder.substation_builder import SubstationBuilder

mRID = str


class DoubleBusSingleBreakerSubstationBuilder(SubstationBuilder):
    """
    Double bus single breaker layout: buses <vl>_bus_1 and <vl>_bus_2 joined by a bus tie breaker
    bay. Each branch has one breaker, fed from either bus through a pair of bus selector
    disconnectors, only one of them normally closed.
    See SubstationBuilder for the call order.
    """

    def add_buses(
        self, voltage_level: CN.VoltageLevel
    ) -> tuple[CN.VoltageLevel, list[CN.BusbarSection], list[CN.Switch]]:
        """Adds the two buses and the bus tie. Returns the voltage level, its busbars and its bus
        tie switches"""
        bus1 = self._bus_node(voltage_level, 1)
        bus2 = self._bus_node(voltage_level, 2)
        busbars = [self._add_busbar(voltage_level, bus1), self._add_busbar(voltage_level, bus2)]
        switches = self._add_breaker_bay(
            voltage_level, prefix=f"{voltage_level.mRID}_tie", node1=bus1, node2=bus2
        )
        return voltage_level, busbars, switches

    def add_branch(
        self, voltage_level: CN.VoltageLevel, *, number: int, node: mRID, bus: int = 1
    ) -> tuple[CN.VoltageLevel, list[CN.Switch]]:
        """
        Connects node through bus selectors <vl>_<number>_sel_1 / _sel_2 - <vl>_<number>_j1 -
        breaker - <vl>_<number>_j2 - line disconnector - node
        * number: bay number, unique within the voltage level, prefixes the bay mRIDs <vl>_<number>
        * node: mRID of the branch ConnectivityNode (e.g. a feeder head node), created if missing
        * bus: 1 or 2, the bus whose selector is normally closed, the other is normally open
        """
        if bus not in (1, 2):
            raise ValueError(f"bus must be 1 or 2, got {bus}")
        bus1 = self._require_node(self._bus_node(voltage_level, 1))
        bus2 = self._require_node(self._bus_node(voltage_level, 2))
        prefix = f"{voltage_level.mRID}_{number}"
        junction1 = f"{prefix}_j1"
        junction2 = f"{prefix}_j2"
        switches = [
            self._add_switch(
                DisconnectorBuilder,
                voltage_level,
                mRID=f"{prefix}_sel_1",
                node1=bus1,
                node2=junction1,
                normalOpen=bus != 1,
            ),
            self._add_switch(
                DisconnectorBuilder,
                voltage_level,
                mRID=f"{prefix}_sel_2",
                node1=bus2,
                node2=junction1,
                normalOpen=bus != 2,
            ),
            self._add_switch(
                BreakerBuilder, voltage_level, mRID=f"{prefix}_brk", node1=junction1, node2=junction2
            ),
            self._add_switch(
                DisconnectorBuilder, voltage_level, mRID=f"{prefix}_d", node1=junction2, node2=node
            ),
        ]
        return voltage_level, switches
