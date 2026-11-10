import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.conducting_asset_info import ConductingAssetInfoBuilder


class TapChangerInfoBuilder(ConductingAssetInfoBuilder):
    """
    Builder for tap changer / regulator catalog data (B17's regulator template: the CYME
    regulator database and the GDM catalog), the only cim18v17 AssetInfo home for tap data.
    Builder functions to be called in the following order:
    * create() - instantiate the TapChangerInfo, e.g. tci_<name>
    * add_asset_info() - nameplate ratings and tap range
    Reference it from an instance with add_asset_datasheet(AssetDatasheet=...). No cim18v17
    EquipmentConfiguration exists for an AutoTransformer, so the impedance/nameplate side of
    B17 (FirstRatedKVA.. bonus table, the regulator's series mesh) has no template home yet -
    still an open decision, see CIM_BUILDER_REQUESTS.md B17.
    """

    cim_class_name = "TapChangerInfo"

    def add_asset_info(
        self,
        info: AI.TapChangerInfo,
        *,
        ratedApparentPower: float | Qty | None = None,
        neutralU: float | Qty | None = None,
        bil: float | Qty | None = None,
        frequency: float | Qty | None = None,
        ctRating: float | Qty | None = None,
        ctRatio: float | None = None,
        ptRatio: float | None = None,
        isTcul: bool | None = None,
        highStep: int | None = None,
        lowStep: int | None = None,
        neutralStep: int | None = None,
        stepVoltageIncrement: float | None = None,
        stepPhaseIncrement: float | Qty | None = None,
        stepReactiveIncrement: float | None = None,
        **kwargs,
    ) -> AI.TapChangerInfo:
        """
        Adds the regulator/tap changer nameplate and tap range, plus the ConductingAssetInfoBuilder ratings
        (phaseCount, ratedCurrent, ratedFrequency, ratedVoltage - CYME RatedKVLN is line-to-neutral)
        * ratedApparentPower: through rating, float in VA or Qty('kVA')
        * neutralU: neutral point voltage, float in V or Qty('kV'), use instead of ratedVoltage for a wye neutral
        * bil: basic insulation level, float in V or Qty('kV')
        * frequency: frequency at which the ratings apply, float in Hz or Qty('Hz')
        * ctRating: current transformer primary rating, float in A or Qty('A')
        * ctRatio: current transformer ratio, float
        * ptRatio: potential transformer ratio, float
        * isTcul: boolean, tap changer under load if true
        * highStep: highest tap position (e.g. +16 for 32 taps at +-10%)
        * lowStep: lowest tap position (e.g. -16)
        * neutralStep: tap position at 0% boost/buck
        * stepVoltageIncrement: percent voltage change per tap step (e.g. 0.625 for 32 taps at +-10%), float
        * stepPhaseIncrement: phase shift per tap step, float in degrees or Qty('deg')
        * stepReactiveIncrement: percent reactance change per tap step, float
        Use cimbuilder.core.tap_steps.tap_steps_from_boost_buck for highStep/lowStep/stepVoltageIncrement
        """
        super().add_asset_info(info, **kwargs)
        graph_write.set_attr(info, AI, "ratedApparentPower", ratedApparentPower)
        graph_write.set_attr(info, AI, "neutralU", neutralU)
        graph_write.set_attr(info, AI, "bil", bil)
        graph_write.set_attr(info, AI, "frequency", frequency)
        graph_write.set_attr(info, AI, "ctRating", ctRating)
        graph_write.set_attr(info, AI, "ctRatio", ctRatio)
        graph_write.set_attr(info, AI, "ptRatio", ptRatio)
        graph_write.set_attr(info, AI, "isTcul", isTcul)
        graph_write.set_attr(info, AI, "highStep", highStep)
        graph_write.set_attr(info, AI, "lowStep", lowStep)
        graph_write.set_attr(info, AI, "neutralStep", neutralStep)
        graph_write.set_attr(info, AI, "stepVoltageIncrement", stepVoltageIncrement)
        graph_write.set_attr(info, AI, "stepPhaseIncrement", stepPhaseIncrement)
        graph_write.set_attr(info, AI, "stepReactiveIncrement", stepReactiveIncrement)
        return info
