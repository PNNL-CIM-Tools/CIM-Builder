import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class SubstationBuilder(ObjectBuilder):
    """
    Builder for substations. Builder functions to be called in the following order:
    * create() - instantiate the Substation, e.g. sub_<name>
    * add_connectivity() - optional, the SubGeographicalRegion holding the substation
    Link feeders with FeederBuilder.add_connectivity(NormalEnergizingSubstation=...)
    """

    cim_class_name = "Substation"

    def add_connectivity(
        self,
        substation: CN.Substation,
        *,
        Region: mRID | None = None,
    ) -> CN.Substation:
        """
        * Region: mRID of the SubGeographicalRegion, e.g. srgn_<name>
        """
        cn: CN = self.cim  # type: ignore
        if Region is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=substation,
                profile_part=CN,
                association_name="Region",
                target_class=cn.SubGeographicalRegion,
                target_mRID=Region,
            )
        return substation
