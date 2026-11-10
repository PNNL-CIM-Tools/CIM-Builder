import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class CoolingInfoBuilder(ObjectBuilder):
    """
    Builder for transformer cooling catalog data (GDM PowerTransformerEquipment cooling_class).
    Builder functions to be called in the following order:
    * create() - instantiate the CoolingInfo, e.g. cool_<name>
    * add_asset_info() - cooling class
    Reference it from an instance with add_asset_datasheet(AssetDatasheet=...)
    """

    cim_class_name = "CoolingInfo"

    def add_asset_info(
        self,
        info: AI.CoolingInfo,
        *,
        typeOfCooling: str | None = None,
    ) -> AI.CoolingInfo:
        """
        Adds the cooling class
        * typeOfCooling: cooling class string, e.g. 'ONAN', 'ONAF' (free text, no CIM enum on this field)
        """
        graph_write.set_attr(info, AI, "typeOfCooling", typeOfCooling)
        return info
