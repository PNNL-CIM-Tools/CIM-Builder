from abc import ABC

import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.conducting_asset_info import ConductingAssetInfoBuilder


class InverterInfoBuilder(ConductingAssetInfoBuilder, ABC):
    """
    Base builder for inverter catalog data, use GenerationInverterInfoBuilder (PV) or
    StorageInverterInfoBuilder (battery). Builder functions to be called in the following order:
    * create() - instantiate the inverter info, e.g. inv_<name>
    * add_asset_info() - inverter ratings
    Reference it from an instance with add_asset_datasheet(AssetDatasheet=...)
    """

    cim_class_name = "InverterInfo"

    def add_asset_info(
        self,
        info: AI.InverterInfo,
        *,
        apparentPowerMaximum: float | Qty | None = None,
        ratedVoltageMax: float | Qty | None = None,
        ratedVoltageMin: float | Qty | None = None,
        **kwargs,
    ) -> AI.InverterInfo:
        """
        Adds the inverter nameplate ratings, plus the ConductingAssetInfoBuilder ratings (phaseCount, ratedCurrent, ...)
        * apparentPowerMaximum: maximum apparent power rating, float in VA or Qty('kVA')
        * ratedVoltageMax: maximum AC voltage before trip, float in V or Qty('kV')
        * ratedVoltageMin: minimum AC voltage before trip, float in V or Qty('kV')
        """
        super().add_asset_info(info, **kwargs)
        graph_write.set_attr(info, AI, "apparentPowerMaximum", apparentPowerMaximum)
        graph_write.set_attr(info, AI, "ratedVoltageMax", ratedVoltageMax)
        graph_write.set_attr(info, AI, "ratedVoltageMin", ratedVoltageMin)
        return info


class GenerationInverterInfoBuilder(InverterInfoBuilder):
    """Builder for PV inverter catalog data (GDM InverterEquipment, PV)."""

    cim_class_name = "GenerationInverterInfo"


class StorageInverterInfoBuilder(InverterInfoBuilder):
    """Builder for battery inverter catalog data (GDM InverterEquipment, storage)."""

    cim_class_name = "StorageInverterInfo"

    def add_asset_info(
        self,
        info: AI.StorageInverterInfo,
        *,
        chargeRateActiveMax: float | Qty | None = None,
        chargeRateReactiveMax: float | Qty | None = None,
        storageCapacity: float | Qty | None = None,
        **kwargs,
    ) -> AI.StorageInverterInfo:
        """
        Adds the storage charge limits, plus every InverterInfoBuilder.add_asset_info field
        * chargeRateActiveMax: maximum active charging power, float in W or Qty('kW')
        * chargeRateReactiveMax: maximum reactive charging power, float in VAr or Qty('kVAr')
        * storageCapacity: maximum stored energy, float in J or Qty('kWh')
        """
        super().add_asset_info(info, **kwargs)
        graph_write.set_attr(info, AI, "chargeRateActiveMax", chargeRateActiveMax)
        graph_write.set_attr(info, AI, "chargeRateReactiveMax", chargeRateReactiveMax)
        graph_write.set_attr(info, AI, "storageCapacity", storageCapacity)
        return info
