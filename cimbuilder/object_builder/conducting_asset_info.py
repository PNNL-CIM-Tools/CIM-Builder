from abc import ABC

import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class ConductingAssetInfoBuilder(ObjectBuilder, ABC):
    """
    Base builder for AC catalog data (wire, cable, inverter, switch, reactor and tap changer info),
    use one of its concrete subclasses. Builder functions to be called in the following order:
    * create() - instantiate the asset info
    * add_asset_info() - ratings shared by every ConductingAssetInfo plus the subclass's own fields
    Reference it from an instance with add_asset_datasheet(AssetDatasheet=...)
    """

    cim_class_name = "ConductingAssetInfo"

    def add_asset_info(
        self,
        info: AI.ConductingAssetInfo,
        *,
        phaseCount: str | None = None,
        ratedCurrent: float | Qty | None = None,
        ratedFrequency: float | Qty | None = None,
        ratedVoltage: float | Qty | None = None,
    ) -> AI.ConductingAssetInfo:
        """
        Adds the ratings shared by every ConductingAssetInfo
        * phaseCount: string, other|singlePhase|threePhase
        * ratedCurrent: rated current, float in A or Qty('A')
        * ratedFrequency: rated frequency, float in Hz or Qty('Hz')
        * ratedVoltage: rated voltage, float in V or Qty('kV')
        """
        graph_write.set_attr(info, AI, "phaseCount", self._enum("PhaseCountKind", phaseCount))
        graph_write.set_attr(info, AI, "ratedCurrent", ratedCurrent)
        graph_write.set_attr(info, AI, "ratedFrequency", ratedFrequency)
        graph_write.set_attr(info, AI, "ratedVoltage", ratedVoltage)
        return info
