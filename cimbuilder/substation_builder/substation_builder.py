import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimtables import graph_write

from cimbuilder.object_builder.container import BayBuilder, VoltageLevelBuilder
from cimbuilder.object_builder.container import (
    SubstationBuilder as SubstationContainerBuilder,
)
from cimbuilder.object_builder.switch import (
    BreakerBuilder,
    DisconnectorBuilder,
    SwitchBuilder,
)
from cimbuilder.object_builder.topology import (
    BusbarSectionBuilder,
    ConnectivityNodeBuilder,
)

mRID = str


class SubstationBuilder(SubstationContainerBuilder):
    """
    Base for node-breaker substation layout builders. Builder functions to be called in the following order:
    * create() - instantiate the Substation, e.g. sub_<name>
    * add_connectivity() - optional, the SubGeographicalRegion holding the substation
    * add_voltage_level() - one VoltageLevel per nominal voltage in the substation
    * add_bay() - optional, a Bay describing a breaker/busbar arrangement in a VoltageLevel
    * add_buses() - layout subclasses, the busbars and bus ties of one VoltageLevel
    * add_branch() - layout subclasses, the switches connecting a line, transformer, shunt or
      feeder head node to the buses
    Layout nodes and switches go in the VoltageLevel, with mRIDs prefixed by the VoltageLevel mRID.
    Link feeders with FeederBuilder.add_connectivity(NormalEnergizingSubstation=...)
    """

    def add_voltage_level(
        self,
        substation: CN.Substation,
        *,
        mRID: str | None = None,
        name: str | None = None,
        description: str | None = None,
        BaseVoltage: mRID,
    ) -> tuple[CN.Substation, CN.VoltageLevel]:
        """
        * mRID: string identifier of the VoltageLevel, e.g. vl_<substation>_<kV>
        * name: human-readable name of the VoltageLevel
        * description: free form comment text
        * BaseVoltage: mRID string of the BaseVoltage of every node and switch in the level
        """
        builder = VoltageLevelBuilder(self.network, self.container)
        voltage_level: CN.VoltageLevel = builder.create(
            mRID=mRID, name=name, description=description
        )  # type: ignore
        builder.add_connectivity(voltage_level, Substation=substation.mRID, BaseVoltage=BaseVoltage)
        return substation, voltage_level

    def add_bay(
        self,
        voltage_level: CN.VoltageLevel,
        *,
        mRID: str | None = None,
        name: str | None = None,
        description: str | None = None,
        breakerConfiguration: str | None = None,
        busBarConfiguration: str | None = None,
    ) -> tuple[CN.VoltageLevel, CN.Bay]:
        """
        * mRID: string identifier of the Bay
        * name: human-readable name of the Bay
        * description: free form comment text
        * breakerConfiguration: string, singleBreaker|breakerAndAHalf|doubleBreaker|noBreaker
        * busBarConfiguration: string, singleBus|doubleBus|mainWithTransfer|ringBus
        """
        builder = BayBuilder(self.network, self.container)
        bay: CN.Bay = builder.create(mRID=mRID, name=name, description=description)  # type: ignore
        builder.add_connectivity(
            bay,
            VoltageLevel=voltage_level.mRID,
            breakerConfiguration=breakerConfiguration,
            busBarConfiguration=busBarConfiguration,
        )
        return voltage_level, bay

    # Shared layout pieces, used by the add_buses()/add_branch() of each layout subclass

    def _bus_node(self, voltage_level: CN.VoltageLevel, label: str | int) -> mRID:
        """mRID of a layout bus node, e.g. <vl>_bus_1 or <vl>_bus_main"""
        return f"{voltage_level.mRID}_bus_{label}"

    def _require_node(self, node: mRID) -> mRID:
        """node unchanged, raising if add_buses() has not built it"""
        cn: CN = self.cim  # type: ignore
        if graph_write.resolve(self.network, cn.ConnectivityNode, node) is None:
            raise ValueError(f"node {node!r} not found: call add_buses() before add_branch()")
        return node

    def _node(self, voltage_level: CN.VoltageLevel, node: mRID) -> CN.ConnectivityNode:
        """The ConnectivityNode with mRID node, created in the VoltageLevel if missing"""
        cn: CN = self.cim  # type: ignore
        existing = graph_write.resolve(self.network, cn.ConnectivityNode, node)
        if existing is not None:
            return existing  # type: ignore
        builder = ConnectivityNodeBuilder(self.network, voltage_level)
        new_node: CN.ConnectivityNode = builder.create(mRID=node)  # type: ignore
        return builder.add_connectivity(new_node, BaseVoltage=voltage_level.BaseVoltage.mRID)

    def _add_busbar(self, voltage_level: CN.VoltageLevel, node: mRID) -> CN.BusbarSection:
        """A new bus node with a BusbarSection, mRID <node>_bbs, on it"""
        self._node(voltage_level, node)
        builder = BusbarSectionBuilder(self.network, voltage_level)
        busbar: CN.BusbarSection = builder.create(mRID=f"{node}_bbs")  # type: ignore
        busbar, _ = builder.add_connectivity(
            busbar, node=node, BaseVoltage=voltage_level.BaseVoltage.mRID
        )
        return busbar

    def _add_switch(
        self,
        builder_class: type[SwitchBuilder],
        voltage_level: CN.VoltageLevel,
        *,
        mRID: str,
        node1: mRID,
        node2: mRID,
        normalOpen: bool = False,
    ) -> CN.Switch:
        """A new switch between node1 and node2, creating either node in the VoltageLevel if missing"""
        self._node(voltage_level, node1)
        self._node(voltage_level, node2)
        builder = builder_class(self.network, voltage_level)
        switch: CN.Switch = builder.create(mRID=mRID)  # type: ignore
        builder.add_connectivity(
            switch,
            node1=node1,
            node2=node2,
            normalOpen=normalOpen,
            BaseVoltage=voltage_level.BaseVoltage.mRID,
        )
        builder.add_ssh(switch, open=normalOpen)
        return switch

    def _add_breaker_bay(
        self, voltage_level: CN.VoltageLevel, *, prefix: str, node1: mRID, node2: mRID
    ) -> list[CN.Switch]:
        """
        A breaker between two isolating disconnectors, node1 - <prefix>_d1 - <prefix>_j1 -
        <prefix>_brk - <prefix>_j2 - <prefix>_d2 - node2
        """
        junction1 = f"{prefix}_j1"
        junction2 = f"{prefix}_j2"
        return [
            self._add_switch(
                DisconnectorBuilder, voltage_level, mRID=f"{prefix}_d1", node1=node1, node2=junction1
            ),
            self._add_switch(
                BreakerBuilder, voltage_level, mRID=f"{prefix}_brk", node1=junction1, node2=junction2
            ),
            self._add_switch(
                DisconnectorBuilder, voltage_level, mRID=f"{prefix}_d2", node1=junction2, node2=node2
            ),
        ]
