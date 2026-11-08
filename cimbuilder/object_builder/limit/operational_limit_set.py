import cimprofiles.cim18.cim18v17.operational_limit as LIM
from cimtables import Qty, graph_write

from cimbuilder.core.sort_terminals import (
    sort_terminals_by_node,
    sort_terminals_by_sequence,
)
from cimbuilder.object_builder.object_builder import ObjectBuilder


class OperationalLimitSetBuilder(ObjectBuilder):
    cim_class_name = "OperationalLimitSet"

    def add_limit_type(
        self,
        *,
        mRID: str | None = None,
        name: str | None = None,
        description: str | None = None,
        acceptableDuration: float | None = None,
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
        Equipment: str,
        Terminal: str | None = None,
        terminal_sequence_number: int | None = None,
        node_side_reference: str | None = None,
    ) -> LIM.OperationalLimitSet:

        if Equipment is not None:
            eq_object = graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=limit_set,
                profile_part=LIM,
                association_name="Equipment",
                target_class=LIM.Equipment,
                target_mRID=Equipment,
            )

        if Terminal is None:
            if terminal_sequence_number is not None:
                terminals = sort_terminals_by_sequence(eq_object)  # type:ignore
                terminal = terminals[terminal_sequence_number]
            elif node_side_reference is not None:
                terminal = sort_terminals_by_node(eq_object, node_side_reference)  # type:ignore
            graph_write.set_assc(limit_set, LIM, "Terminal", terminal)

        else:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=limit_set,
                profile_part=LIM,
                association_name="Terminal",
                target_class=LIM.Terminal,
                target_mRID=Terminal,
            )

        return limit_set

    def add_voltage_limit(
        self,
        limit_set: LIM.OperationalLimitSet,
        *,
        mRID: str | None = None,
        name: str | None = None,
        description: str | None = None,
        normalValue: float | Qty | None = None,
        value: float | Qty | None = None,
        OperationalLimitType: str,
    ) -> tuple[LIM.OperationalLimitSet, LIM.VoltageLimit]:
        """
        Adds a new ActivePowerLimit to the OperationalLimitSet
        * mRID: unique string key to identify the limit type
        * name: human-readable limit type name (e.g. "load dump low")
        * description: free-form comment text
        * normalValue: float in volts or Qty('V'|'kV')
        * value: float in volts or Qty('V'|'kV')
        * OperationalLimitType: mRID of the limit type (e.g. normal / alert / emergency)
        """
        lim: LIM = self.cim  # type:ignore
        if mRID is None:
            mRID = f"{limit_set.mRID}_voltage_limit_{OperationalLimitType}"
        volt_limit = lim.VoltageLimit(name=name, mRID=mRID, description=description)
        graph_write.set_attr(volt_limit, LIM, "value", value)
        graph_write.set_attr(volt_limit, LIM, "normalValue", normalValue)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=limit_set,
            profile_part=LIM,
            association_name="OperationalLimitType",
            target_class=LIM.OperationalLimitType,
            target_mRID=OperationalLimitType,
        )
        graph_write.add_to_graph(self.network, volt_limit)
        return limit_set, volt_limit

    def add_current_limit(
        self,
        limit_set: LIM.OperationalLimitSet,
        *,
        mRID: str | None = None,
        name: str | None = None,
        description: str | None = None,
        normalValue: float | Qty | None = None,
        value: float | Qty | None = None,
        OperationalLimitType: str,
    ) -> tuple[LIM.OperationalLimitSet, LIM.CurrentLimit]:
        """
        Adds a new CurrentLimit to the OperationalLimitSet
        * mRID: unique string key to identify the limit type
        * name: human-readable limit type name (e.g. "load dump low")
        * description: free-form comment text
        * normalValue: float in amps or Qty('A')
        * value: float in amps or Qty('A')
        * OperationalLimitType: mRID of the limit type (e.g. normal / alert / emergency)
        """
        lim: LIM = self.cim  # type:ignore
        if mRID is None:
            mRID = f"{limit_set.mRID}_current_limit_{OperationalLimitType}"
        current_limit = lim.CurrentLimit(name=name, mRID=mRID, description=description)
        graph_write.set_attr(current_limit, LIM, "value", value)
        graph_write.set_attr(current_limit, LIM, "normalValue", normalValue)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=limit_set,
            profile_part=LIM,
            association_name="OperationalLimitType",
            target_class=LIM.OperationalLimitType,
            target_mRID=OperationalLimitType,
        )
        graph_write.add_to_graph(self.network, current_limit)
        return limit_set, current_limit

    def add_active_power_limit(
            self,
            limit_set: LIM.OperationalLimitSet,
            *,
            mRID: str | None = None,
            name: str | None = None,
            description: str | None = None,
            normalValue: float | Qty | None = None,
            value: float | Qty | None = None,
            OperationalLimitType: str,
        ) -> tuple[LIM.OperationalLimitSet, LIM.ActivePowerLimit]:
            """
            Adds a new ActivePowerLimit to the OperationalLimitSet
            * mRID: unique string key to identify the limit type
            * name: human-readable limit type name (e.g. "load dump low")
            * description: free-form comment text
            * normalValue: float in watts or Qty('W'|'kW'|'MW')
            * value: float in watts or Qty('W'|'kW'|'MW')
            * OperationalLimitType: mRID of the limit type (e.g. normal / alert / emergency)
            """
            lim: LIM = self.cim  # type:ignore
            if mRID is None:
                mRID = f"{limit_set.mRID}_active_power_limit_{OperationalLimitType}"
            mw_limit = lim.ActivePowerLimit(name=name, mRID=mRID, description=description)
            graph_write.set_attr(mw_limit, LIM, "value", value)
            graph_write.set_attr(mw_limit, LIM, "normalValue", normalValue)
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=limit_set,
                profile_part=LIM,
                association_name="OperationalLimitType",
                target_class=LIM.OperationalLimitType,
                target_mRID=OperationalLimitType,
            )
            graph_write.add_to_graph(self.network, mw_limit)
            return limit_set, mw_limit

    def add_apparent_power_limit(
            self,
            limit_set: LIM.OperationalLimitSet,
            *,
            mRID: str | None = None,
            name: str | None = None,
            description: str | None = None,
            normalValue: float | Qty | None = None,
            value: float | Qty | None = None,
            OperationalLimitType: str,
        ) -> tuple[LIM.OperationalLimitSet, LIM.ApparentPowerLimit]:
            """
            Adds a new ActivePowerLimit to the OperationalLimitSet
            * mRID: unique string key to identify the limit type
            * name: human-readable limit type name (e.g. "load dump low")
            * description: free-form comment text
            * normalValue: float in VA or Qty('VA'|'kVA'|'MVA')
            * value: float in VA or Qty('VA'|'kVA'|'MVA')
            * OperationalLimitType: mRID of the limit type (e.g. normal / alert / emergency)
            """
            lim: LIM = self.cim  # type:ignore
            if mRID is None:
                mRID = f"{limit_set.mRID}_apparent_power_limit_{OperationalLimitType}"
            mva_limit = lim.ApparentPowerLimit(name=name, mRID=mRID, description=description)
            graph_write.set_attr(mva_limit, LIM, "value", value)
            graph_write.set_attr(mva_limit, LIM, "normalValue", normalValue)
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=limit_set,
                profile_part=LIM,
                association_name="OperationalLimitType",
                target_class=LIM.OperationalLimitType,
                target_mRID=OperationalLimitType,
            )
            graph_write.add_to_graph(self.network, mva_limit)
            return limit_set, mva_limit