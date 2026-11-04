from abc import ABC

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.short_circuit as SC
from cimtables import Qty, connectivity, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class ConnectorBuilder(ObjectBuilder, ABC):
    cim_class_name = "Connector"

    def add_connectivity(
        self,
        conn: CN.Connector,
        *,
        node: str,
        EquipmentContainer: str | None = None,
        BaseVoltage: str,
    ) -> tuple[CN.Connector, CN.Terminal]:
        """
        Adds base connectivity layer of terminals, base voltage, phasing
        * node: mRID of the ConnectivityNode or TopologicalNode
        * EquipmentContainer: mRID of the VoltageLevel or Feeder containing the busbar.
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore

        if EquipmentContainer is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=conn,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=EquipmentContainer,
            )
        else:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=conn,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=self.container.mRID,
            )

        if len(conn.Terminals) != 1:
            terminals = connectivity.add_connectivity(
                network=self.network,
                equipment=conn,
                node_cols={"node": node},
                equipment_container=conn.EquipmentContainer,
            )

        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=conn,
                profile_part=CN,
                association_name="BaseVoltage",
                target_class=cn.BaseVoltage,
                target_mRID=BaseVoltage,
            )
        return (conn, terminals[0])


class BusbarSectionBuilder(ConnectorBuilder):
    cim_class_name = "BusbarSection"

    def add_connectivity(
        self,
        busbar: CN.BusbarSection,
        *,
        node: str,
        EquipmentContainer: str | None = None,
        BaseVoltage: str,
    ) -> tuple[CN.BusbarSection, CN.Terminal]:
        return super().add_connectivity(
            busbar,
            node=node,
            EquipmentContainer=EquipmentContainer,
            BaseVoltage=BaseVoltage,
        )  # type:ignore

    def add_short_circuit(
        self, busbar: SC.BusbarSection, *, ipMax: float | Qty | None = None
    ) -> SC.BusbarSection:
        """
        * ipMax: Max allowable peak short-circuit current, float in A or Qty('kA')
        """
        graph_write.set_attr(busbar, SC, "ipMax", ipMax)

        return busbar


class JuntionBuilder(ConnectorBuilder):
    cim_class_name = "Junction"

    def add_connectivity(
        self,
        conn: CN.Junction,
        *,
        node: str,
        EquipmentContainer: str | None = None,
        BaseVoltage: str,
    ) -> tuple[CN.Junction, CN.Terminal]:
        return super().add_connectivity(
            conn,
            node=node,
            EquipmentContainer=EquipmentContainer,
            BaseVoltage=BaseVoltage,
        )  # type:ignore
