from typing import Optional

import cimprofiles.cim18.cim18v17.asset_deployment as AD

from cimbuilder.object_builder.object_builder import ObjectBuilder
from cimtables import connectivity, graph_write, impedance
from cimtables.units import Qty

class ACLineSegmentBuilder(ObjectBuilder):
    cim_class_name = 'ACLineSegmentPhase'

    def add_asset_deployment(self, line_phase, *, WireInfo):
        """
        Associates the line phase with an existing conductor AssetInfo
        * WireInfo: mRID string of the target WireInfo
        """
        self.cim:AD # type: ignore
        target:AD.WireInfo = graph_write.set_assc_from_mrid(
            self.network, line_phase, AD, 'WireInfo', self.cim.WireInfo, WireInfo)
        return target
    
