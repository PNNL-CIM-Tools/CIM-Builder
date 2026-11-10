import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN

from cimbuilder.object_builder.switch import DisconnectorBuilder
from cimbuilder.substation_builder.substation_builder import SubstationBuilder

mRID = str


class MainAndTransferSubstationBuilder(SubstationBuilder):
    """
    Main-and-transfer layout: main bus <vl>_bus_main and transfer bus <vl>_bus_transfer joined by a
    bus tie breaker bay. Each branch has its own breaker bay to the main bus, plus a normally open
    bypass disconnector to the transfer bus so the branch breaker can be taken out for maintenance.
    See SubstationBuilder for the call order.
    """

    def add_buses(
        self, voltage_level: CN.VoltageLevel
    ) -> tuple[CN.VoltageLevel, list[CN.BusbarSection], list[CN.Switch]]:
        """Adds the main and transfer buses and the bus tie. Returns the voltage level, its busbars
        and its bus tie switches"""
        main_bus = self._bus_node(voltage_level, "main")
        transfer_bus = self._bus_node(voltage_level, "transfer")
        busbars = [
            self._add_busbar(voltage_level, main_bus),
            self._add_busbar(voltage_level, transfer_bus),
        ]
        switches = self._add_breaker_bay(
            voltage_level, prefix=f"{voltage_level.mRID}_tie", node1=main_bus, node2=transfer_bus
        )
        return voltage_level, busbars, switches

    def add_branch(
        self, voltage_level: CN.VoltageLevel, *, number: int, node: mRID
    ) -> tuple[CN.VoltageLevel, list[CN.Switch]]:
        """
        Connects node to the main bus through main bus - disconnector - breaker - disconnector - node,
        and to the transfer bus through the normally open bypass disconnector <vl>_<number>_bypass
        * number: bay number, unique within the voltage level, prefixes the bay mRIDs <vl>_<number>
        * node: mRID of the branch ConnectivityNode (e.g. a feeder head node), created if missing
        """
        main_bus = self._require_node(self._bus_node(voltage_level, "main"))
        transfer_bus = self._require_node(self._bus_node(voltage_level, "transfer"))
        prefix = f"{voltage_level.mRID}_{number}"
        switches = self._add_breaker_bay(voltage_level, prefix=prefix, node1=main_bus, node2=node)
        bypass = self._add_switch(
            DisconnectorBuilder,
            voltage_level,
            mRID=f"{prefix}_bypass",
            node1=node,
            node2=transfer_bus,
            normalOpen=True,
        )
        return voltage_level, switches + [bypass]
