import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class SolarPanelInfoBuilder(ObjectBuilder):
    """
    Builder for solar panel catalog data (GDM SolarEquipment). Builder functions to be called in the following order:
    * create() - instantiate the SolarPanelInfo, e.g. pv_<name>
    * add_asset_info() - panel efficiency, DC ratings and reference test conditions
    Reference it from an instance with add_asset_datasheet(AssetDatasheet=...)
    """

    cim_class_name = "SolarPanelInfo"

    def add_asset_info(
        self,
        info: AI.SolarPanelInfo,
        *,
        efficiency: float | None = None,
        openCircuitVoltage: float | Qty | None = None,
        shortCircuitCurrent: float | Qty | None = None,
        referenceIrradiation: float | Qty | None = None,
        referenceTemperature: float | Qty | None = None,
    ) -> AI.SolarPanelInfo:
        """
        Adds the panel efficiency, DC ratings and reference test conditions
        * efficiency: panel conversion efficiency, float in percentage (e.g. 18.5)
        * openCircuitVoltage: DC open-circuit voltage at the reference condition, float in V or Qty('V')
        * shortCircuitCurrent: DC short-circuit current at the reference condition, float in A or Qty('A')
        * referenceIrradiation: irradiation at the reference test condition, float in W/m^2 or Qty('kW/m^2')
        * referenceTemperature: cell temperature at the reference test condition, float in degC or Qty('degC')
        """
        graph_write.set_attr(info, AI, "efficiency", efficiency)
        graph_write.set_attr(info, AI, "openCircuitVoltage", openCircuitVoltage)
        graph_write.set_attr(info, AI, "shortCircuitCurrent", shortCircuitCurrent)
        graph_write.set_attr(info, AI, "referenceIrradiation", referenceIrradiation)
        graph_write.set_attr(info, AI, "referenceTemperature", referenceTemperature)
        return info
