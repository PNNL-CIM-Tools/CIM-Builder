import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class ConnectivityNodeBuilder(ObjectBuilder):
    """
    Builder for named buses. Builder functions to be called in the following order:
    * create() - instantiate the ConnectivityNode, mRID = the bare bus name (e.g. 671)
    * add_connectivity() - BaseVoltage and the containing Feeder or Substation
    Build nodes before the equipment on them: equipment add_connectivity reuses a node by mRID,
    and only auto-creates a bare one (no name, no BaseVoltage) when it is missing
    """

    cim_class_name = "ConnectivityNode"

    def add_connectivity(
        self,
        node: CN.ConnectivityNode,
        *,
        BaseVoltage: mRID | None = None,
        ConnectivityNodeContainer: mRID | None = None,
    ) -> CN.ConnectivityNode:
        """
        * BaseVoltage: mRID string of the BaseVoltage
        * ConnectivityNodeContainer: mRID of the Feeder, Substation or VoltageLevel containing the node.
          Defaults to the builder's container
        """
        cn: CN = self.cim  # type: ignore
        if ConnectivityNodeContainer is None:
            ConnectivityNodeContainer = self.container.mRID
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=node,
            profile_part=CN,
            association_name="ConnectivityNodeContainer",
            target_class=cn.ConnectivityNodeContainer,
            target_mRID=ConnectivityNodeContainer,
        )
        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=node,
                profile_part=CN,
                association_name="BaseVoltage",
                target_class=cn.BaseVoltage,
                target_mRID=BaseVoltage,
            )
        return node
