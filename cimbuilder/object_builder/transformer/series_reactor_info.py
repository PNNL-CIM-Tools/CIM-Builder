import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.conducting_asset_info import ConductingAssetInfoBuilder


class SeriesReactorInfoBuilder(ConductingAssetInfoBuilder):
    """
    Builder for series reactor catalog data (GDM ReactorEquipment). Builder functions to be called in the following order:
    * create() - instantiate the SeriesReactorInfo, e.g. reac_<name>
    * add_asset_info() - ratings, construction and oil data
    Reference it from an instance with add_asset_datasheet(AssetDatasheet=...)
    """

    cim_class_name = "SeriesReactorInfo"

    def add_asset_info(
        self,
        info: AI.SeriesReactorInfo,
        *,
        ratedInductance: float | None = None,
        ratedReactivePower: float | Qty | None = None,
        maxPowerLoss: float | Qty | None = None,
        ratedImpulseWithstandVoltage: float | Qty | None = None,
        ratedMechanicalCurrent: float | None = None,
        ratedThermalCurrent: float | None = None,
        coreType: str | None = None,
        insulationMedium: str | None = None,
        circulationAndCoolingType: str | None = None,
        temperatureClass: str | None = None,
        temperatureRise: float | None = None,
        oilType: str | None = None,
        oilPreservationType: str | None = None,
        volumeOfOil: float | None = None,
        oilWeight: float | None = None,
        coreCoilsWeight: float | None = None,
        tankAndFittingsWeight: float | None = None,
        **kwargs,
    ) -> AI.SeriesReactorInfo:
        """
        Adds the reactor nameplate, plus the ConductingAssetInfoBuilder ratings (phaseCount, ratedCurrent, ...).
        Fields documented "no CIM unit" are bare floats in cim18v17 - convert before passing
        * ratedInductance: rated inductance, float, no CIM unit
        * ratedReactivePower: rated reactive power, float in VAr or Qty('kVAr')
        * maxPowerLoss: maximum power loss, float in VA or Qty('kVA') (typed ApparentPower in cim18v17)
        * ratedImpulseWithstandVoltage: BIL, float in V or Qty('kV')
        * ratedMechanicalCurrent: rated mechanical (short-time peak) current, float, no CIM unit
        * ratedThermalCurrent: rated thermal (short-time) current, float, no CIM unit
        * coreType: string, air|concrete|none|other|steel
        * insulationMedium: string, air|oil|other
        * circulationAndCoolingType: string, oilForcedAirForced|oilForcedAirNatural|oilNaturalAirForced|oilNaturalAirNatural|other
        * temperatureClass: free text insulation temperature class
        * temperatureRise: rated temperature rise, float, no CIM unit
        * oilType: free text oil type
        * oilPreservationType: string, conservator|freeBreathing|nitrogenBlanket|other
        * volumeOfOil: oil volume, float, no CIM unit
        * oilWeight: oil weight, float, no CIM unit
        * coreCoilsWeight: core and coils weight, float, no CIM unit
        * tankAndFittingsWeight: tank and fittings weight, float, no CIM unit
        """
        super().add_asset_info(info, **kwargs)
        graph_write.set_attr(info, AI, "ratedInductance", ratedInductance)
        graph_write.set_attr(info, AI, "ratedReactivePower", ratedReactivePower)
        graph_write.set_attr(info, AI, "maxPowerLoss", maxPowerLoss)
        graph_write.set_attr(info, AI, "ratedImpulseWithstandVoltage", ratedImpulseWithstandVoltage)
        graph_write.set_attr(info, AI, "ratedMechanicalCurrent", ratedMechanicalCurrent)
        graph_write.set_attr(info, AI, "ratedThermalCurrent", ratedThermalCurrent)
        graph_write.set_attr(info, AI, "coreType", self._enum("ReactorCoreKind", coreType))
        graph_write.set_attr(
            info, AI, "insulationMedium", self._enum("ReactorInsulationMediumKind", insulationMedium)
        )
        graph_write.set_attr(
            info,
            AI,
            "circulationAndCoolingType",
            self._enum("CirculationAndCoolingKind", circulationAndCoolingType),
        )
        graph_write.set_attr(info, AI, "temperatureClass", temperatureClass)
        graph_write.set_attr(info, AI, "temperatureRise", temperatureRise)
        graph_write.set_attr(info, AI, "oilType", oilType)
        graph_write.set_attr(
            info, AI, "oilPreservationType", self._enum("OilPreservationKind", oilPreservationType)
        )
        graph_write.set_attr(info, AI, "volumeOfOil", volumeOfOil)
        graph_write.set_attr(info, AI, "oilWeight", oilWeight)
        graph_write.set_attr(info, AI, "coreCoilsWeight", coreCoilsWeight)
        graph_write.set_attr(info, AI, "tankAndFittingsWeight", tankAndFittingsWeight)
        return info
