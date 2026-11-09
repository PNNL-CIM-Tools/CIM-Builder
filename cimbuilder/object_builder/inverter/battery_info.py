import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class BatteryInfoBuilder(ObjectBuilder):
    """
    Builder for battery catalog data (GDM BatteryEquipment). Builder functions to be called in the following order:
    * create() - instantiate the BatteryInfo, e.g. batt_<name>
    * add_asset_info() - chemistry, cell count and capacity
    Reference it from an instance with add_asset_datasheet(AssetDatasheet=...)
    """

    cim_class_name = "BatteryInfo"

    def add_asset_info(
        self,
        info: AI.BatteryInfo,
        *,
        batteryType: str | None = None,
        cellChemistry: str | None = None,
        numberOfCells: int | None = None,
        ratedCapacity: float | Qty | None = None,
        usableCapacity: float | Qty | None = None,
    ) -> AI.BatteryInfo:
        """
        Adds the battery chemistry and capacity ratings
        * batteryType: string, leadAcid|lithiumIon|lithiumIronPhosphate|nickelMetalHydride|other|sodiumIon|solidState
        * cellChemistry: free text cell chemistry, e.g. 'NMC'
        * numberOfCells: integer, number of cells in the battery
        * ratedCapacity: nameplate energy capacity, float in J or Qty('kWh')
        * usableCapacity: usable energy capacity (after depth-of-discharge limits), float in J or Qty('kWh')
        """
        graph_write.set_attr(info, AI, "batteryType", self._enum("BatteryTypeKind", batteryType))
        graph_write.set_attr(info, AI, "cellChemistry", cellChemistry)
        graph_write.set_attr(info, AI, "numberOfCells", numberOfCells)
        graph_write.set_attr(info, AI, "ratedCapacity", ratedCapacity)
        graph_write.set_attr(info, AI, "usableCapacity", usableCapacity)
        return info
