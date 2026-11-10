import cimprofiles.cim18.cim18v17.operational_limit as LIM
from cimtables import Qty, graph_write

from cimbuilder.core.sort_terminals import (
    sort_terminals_by_node,
    sort_terminals_by_sequence,
)
from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class OperationalLimitSetBuilder(ObjectBuilder):
    """
    Builder for the set of operational limits of one piece of equipment. Builder functions to be called in the following order:
    * add_limit_type() - create each limit type (e.g. normal / emergency) once, shared by every set
    * create() - instantiate the OperationalLimitSet, e.g. <ln>_limits
    * add_equipment() - attach the set to its equipment and optionally one of its terminals
    * add_current_limit() / add_voltage_limit() / add_active_power_limit() / add_apparent_power_limit() - one limit per type
    """

    cim_class_name = "OperationalLimitSet"

    def add_limit_type(
        self,
        *,
        mRID: str | None = None,
        name: str | None = None,
        description: str | None = None,
        acceptableDuration: float | Qty | None = None,
        isInfiniteDuration: bool | None = None,
        direction: str | None = None,
    ) -> LIM.OperationalLimitType:
        """
        Create types of limit (e.g. normal / alert / emergency)
        * mRID: unique string key to identify the limit type
        * name: human-readable limit type name (e.g. "load dump low")
        * description: free-form comment text
        * acceptableDuration: time in seconds until trip when exceeding limit, float in s or Qty('s')
        * isInfiniteDuration: true for normal / alert
        * direction: string, high|low|absoluteValue
        """
        lim: LIM = self.cim  # type:ignore
        lim_type = lim.OperationalLimitType(
            name=name, mRID=mRID, description=description
        )
        graph_write.set_attr(lim_type, LIM, "acceptableDuration", acceptableDuration)
        graph_write.set_attr(lim_type, LIM, "isInfiniteDuration", isInfiniteDuration)
        if direction is not None:
            graph_write.set_attr(
                lim_type, LIM, "direction", lim.OperationalLimitDirectionKind(direction)
            )
        graph_write.add_to_graph(self.network, lim_type)
        return lim_type

    def add_equipment(
        self,
        limit_set: LIM.OperationalLimitSet,
        *,
        Equipment: mRID,
        Terminal: mRID | None = None,
        terminal_sequence_number: int | None = None,
        node_side_reference: mRID | None = None,
    ) -> LIM.OperationalLimitSet:
        """
        Attaches the set to its equipment. Give at most one terminal selector to also attach it to a terminal
        * Equipment: mRID of the limited equipment, e.g. ln_632645
        * Terminal: mRID of the limited Terminal
        * terminal_sequence_number: integer, sequenceNumber of the limited Terminal, starting at 1
        * node_side_reference: mRID of the ConnectivityNode on the limited side
        """
        lim: LIM = self.cim  # type:ignore
        selectors = [Terminal, terminal_sequence_number, node_side_reference]
        if sum(selector is not None for selector in selectors) > 1:
            raise ValueError(
                f"{limit_set.mRID!r}: give one of Terminal, terminal_sequence_number "
                f"or node_side_reference, got {selectors}"
            )
        equipment = graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=limit_set,
            profile_part=LIM,
            association_name="Equipment",
            target_class=lim.Equipment,
            target_mRID=Equipment,
        )

        if Terminal is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=limit_set,
                profile_part=LIM,
                association_name="Terminal",
                target_class=lim.Terminal,
                target_mRID=Terminal,
            )
        elif terminal_sequence_number is not None:
            terminals = sort_terminals_by_sequence(equipment)  # type:ignore
            graph_write.set_assc(limit_set, LIM, "Terminal", terminals[terminal_sequence_number - 1])
        elif node_side_reference is not None:
            terminal = sort_terminals_by_node(equipment, node_side_reference)  # type:ignore
            if terminal is None:
                raise ValueError(
                    f"{limit_set.mRID!r}: {Equipment!r} has no terminal on node {node_side_reference!r}"
                )
            graph_write.set_assc(limit_set, LIM, "Terminal", terminal)
        return limit_set

    def _add_limit(
        self,
        limit_set: LIM.OperationalLimitSet,
        limit_class_name: str,
        *,
        mRID: str,
        name: str | None,
        description: str | None,
        normalValue: float | Qty | None,
        value: float | Qty | None,
        OperationalLimitType: mRID,
    ) -> LIM.OperationalLimit:
        """Shared body of the add_*_limit methods: the limit, its values, its set and its type"""
        lim: LIM = self.cim  # type:ignore
        limit = getattr(lim, limit_class_name)(name=name, mRID=mRID, description=description)
        graph_write.set_attr(limit, LIM, "value", value)
        graph_write.set_attr(limit, LIM, "normalValue", normalValue)
        graph_write.set_assc(limit, LIM, "OperationalLimitSet", limit_set)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=limit,
            profile_part=LIM,
            association_name="OperationalLimitType",
            target_class=lim.OperationalLimitType,
            target_mRID=OperationalLimitType,
        )
        graph_write.add_to_graph(self.network, limit)
        return limit

    def add_voltage_limit(
        self,
        limit_set: LIM.OperationalLimitSet,
        *,
        mRID: str | None = None,
        name: str | None = None,
        description: str | None = None,
        normalValue: float | Qty | None = None,
        value: float | Qty | None = None,
        OperationalLimitType: mRID,
    ) -> tuple[LIM.OperationalLimitSet, LIM.VoltageLimit]:
        """
        Adds a new VoltageLimit to the OperationalLimitSet
        * mRID: unique string key, default <set>_voltage_limit_<type>
        * name: human-readable limit name
        * description: free-form comment text
        * normalValue: float in volts or Qty('V'|'kV')
        * value: float in volts or Qty('V'|'kV')
        * OperationalLimitType: mRID of the limit type (e.g. normal / alert / emergency)
        """
        if mRID is None:
            mRID = f"{limit_set.mRID}_voltage_limit_{OperationalLimitType}"
        limit = self._add_limit(
            limit_set,
            "VoltageLimit",
            mRID=mRID,
            name=name,
            description=description,
            normalValue=normalValue,
            value=value,
            OperationalLimitType=OperationalLimitType,
        )
        return limit_set, limit  # type:ignore

    def add_current_limit(
        self,
        limit_set: LIM.OperationalLimitSet,
        *,
        mRID: str | None = None,
        name: str | None = None,
        description: str | None = None,
        normalValue: float | Qty | None = None,
        value: float | Qty | None = None,
        OperationalLimitType: mRID,
    ) -> tuple[LIM.OperationalLimitSet, LIM.CurrentLimit]:
        """
        Adds a new CurrentLimit to the OperationalLimitSet
        * mRID: unique string key, default <set>_current_limit_<type> (e.g. ln_632645_normal)
        * name: human-readable limit name
        * description: free-form comment text
        * normalValue: float in amps or Qty('A')
        * value: float in amps or Qty('A')
        * OperationalLimitType: mRID of the limit type (e.g. normal / alert / emergency)
        """
        if mRID is None:
            mRID = f"{limit_set.mRID}_current_limit_{OperationalLimitType}"
        limit = self._add_limit(
            limit_set,
            "CurrentLimit",
            mRID=mRID,
            name=name,
            description=description,
            normalValue=normalValue,
            value=value,
            OperationalLimitType=OperationalLimitType,
        )
        return limit_set, limit  # type:ignore

    def add_active_power_limit(
        self,
        limit_set: LIM.OperationalLimitSet,
        *,
        mRID: str | None = None,
        name: str | None = None,
        description: str | None = None,
        normalValue: float | Qty | None = None,
        value: float | Qty | None = None,
        OperationalLimitType: mRID,
    ) -> tuple[LIM.OperationalLimitSet, LIM.ActivePowerLimit]:
        """
        Adds a new ActivePowerLimit to the OperationalLimitSet
        * mRID: unique string key, default <set>_active_power_limit_<type>
        * name: human-readable limit name
        * description: free-form comment text
        * normalValue: float in watts or Qty('W'|'kW'|'MW')
        * value: float in watts or Qty('W'|'kW'|'MW')
        * OperationalLimitType: mRID of the limit type (e.g. normal / alert / emergency)
        """
        if mRID is None:
            mRID = f"{limit_set.mRID}_active_power_limit_{OperationalLimitType}"
        limit = self._add_limit(
            limit_set,
            "ActivePowerLimit",
            mRID=mRID,
            name=name,
            description=description,
            normalValue=normalValue,
            value=value,
            OperationalLimitType=OperationalLimitType,
        )
        return limit_set, limit  # type:ignore

    def add_apparent_power_limit(
        self,
        limit_set: LIM.OperationalLimitSet,
        *,
        mRID: str | None = None,
        name: str | None = None,
        description: str | None = None,
        normalValue: float | Qty | None = None,
        value: float | Qty | None = None,
        OperationalLimitType: mRID,
    ) -> tuple[LIM.OperationalLimitSet, LIM.ApparentPowerLimit]:
        """
        Adds a new ApparentPowerLimit to the OperationalLimitSet
        * mRID: unique string key, default <set>_apparent_power_limit_<type>
        * name: human-readable limit name
        * description: free-form comment text
        * normalValue: float in VA or Qty('VA'|'kVA'|'MVA')
        * value: float in VA or Qty('VA'|'kVA'|'MVA')
        * OperationalLimitType: mRID of the limit type (e.g. normal / alert / emergency)
        """
        if mRID is None:
            mRID = f"{limit_set.mRID}_apparent_power_limit_{OperationalLimitType}"
        limit = self._add_limit(
            limit_set,
            "ApparentPowerLimit",
            mRID=mRID,
            name=name,
            description=description,
            normalValue=normalValue,
            value=value,
            OperationalLimitType=OperationalLimitType,
        )
        return limit_set, limit  # type:ignore
