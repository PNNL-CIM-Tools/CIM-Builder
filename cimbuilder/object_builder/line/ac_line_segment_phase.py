
import cimprofiles.cim18.cim18v17.asset_deployment as AD
import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class ACLineSegmentPhaseBuilder(ObjectBuilder):
    cim_class_name = "ACLineSegmentPhase"

    def add_connectivity(
        self,
        line_phs: CN.ACLineSegmentPhase,
        sequenceNumber: int,
        phase: str,
        ACLineSegment: str,
    ) -> CN.ACLineSegmentPhase:
        """
        Add connectivity and phasing information
        * sequenceNumber: integer for indexing of wire position / impedance matrix
        * phase: Single phase kind, A|B|C|N|s1|s2|X|Y
        """
        cn: CN = self.cim  # type: ignore
        graph_write.set_attr(line_phs, CN, "sequenceNumber", sequenceNumber)
        graph_write.set_attr(line_phs, CN, "phase", phase)
        if ACLineSegment is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=line_phs,
                profile_part=CN,
                association_name="ACLineSegment",
                target_class=cn.ACLineSegment,
                target_mRID=ACLineSegment,
            )
        return line_phs

    def add_asset_deployment(
        self, line_phs, *, WireInfo
    ) -> tuple[AD.ACLineSegmentPhase, AD.WireInfo]:
        """
        Associates the line phase with an existing conductor AssetInfo
        * WireInfo: mRID string of the target WireInfo
        """
        ad: AD = self.cim  # type: ignore
        wire_info: AD.WireInfo = graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=line_phs,
            profile_part=AD,
            association_name="WireInfo",
            target_class=ad.WireInfo,
            target_mRID=WireInfo,
        )
        return line_phs, wire_info
