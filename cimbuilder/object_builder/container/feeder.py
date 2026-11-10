import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class FeederBuilder(ObjectBuilder):
    """
    Builder for distribution feeders. A model may hold several, each piece of equipment names its own
    EquipmentContainer. Builder functions to be called in the following order:
    * create() - instantiate the Feeder, e.g. fdr_<name>
    * add_connectivity() - optional, the Substation that normally energizes the feeder and its head Terminal
    """

    cim_class_name = "Feeder"

    def add_connectivity(
        self,
        feeder: CN.Feeder,
        *,
        NormalEnergizingSubstation: mRID | None = None,
        NormalHeadTerminal: mRID | None = None,
    ) -> CN.Feeder:
        """
        * NormalEnergizingSubstation: mRID of the Substation feeding this feeder, e.g. sub_<name>
        * NormalHeadTerminal: mRID of the feeder-side Terminal of the feeder head breaker
        """
        cn: CN = self.cim  # type: ignore
        if NormalEnergizingSubstation is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=feeder,
                profile_part=CN,
                association_name="NormalEnergizingSubstation",
                target_class=cn.Substation,
                target_mRID=NormalEnergizingSubstation,
            )
        if NormalHeadTerminal is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=feeder,
                profile_part=CN,
                association_name="NormalHeadTerminal",
                target_class=cn.Terminal,
                target_mRID=NormalHeadTerminal,
            )
        return feeder
