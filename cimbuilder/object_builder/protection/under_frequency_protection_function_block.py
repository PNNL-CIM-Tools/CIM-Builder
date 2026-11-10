import cimprofiles.cim18.cim18v17.protection as PROT
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class UnderFrequencyProtectionFunctionBlockBuilder(ObjectBuilder):
    """
    Builder for an under-frequency load shedding (UFLS) stage. Builder functions to be called in
    the following order:
    * create() - instantiate the UnderFrequencyProtectionFunctionBlock, e.g. ufls_<Hz>_<breaker>
    * add_protection() - the pickup frequency
    """

    cim_class_name = "UnderFrequencyProtectionFunctionBlock"

    def add_protection(
        self,
        function_block: PROT.UnderFrequencyProtectionFunctionBlock,
        *,
        operateValue: float | Qty,
        # TODO: pending the UML fix, cim18v17 UnderFrequencyProtectionFunctionBlock has no
        # enabled, usage, ProtectedSwitch or ProtectionEquipment
        # enabled: bool | None = None,
        # ProtectedSwitch: mRID | None = None,
        # ProtectionEquipment: mRID | None = None,
    ) -> PROT.UnderFrequencyProtectionFunctionBlock:
        """
        Adds the protection profile layer
        * operateValue: pickup frequency, float in Hz or Qty(59.3, 'Hz')
        """
        graph_write.set_attr(function_block, PROT, "operateValue", operateValue)
        # graph_write.set_attr(function_block, PROT, "enabled", enabled)
        # graph_write.set_attr(function_block, PROT, "usage", f"ufls_{operateValue}")
        # graph_write.set_assc_from_mrid(
        #     network=self.network,
        #     source_object=function_block,
        #     profile_part=PROT,
        #     association_name="ProtectedSwitch",
        #     target_class=self.cim.ProtectedSwitch,
        #     target_mRID=ProtectedSwitch,
        # )
        # graph_write.set_assc_from_mrid(
        #     network=self.network,
        #     source_object=function_block,
        #     profile_part=PROT,
        #     association_name="ProtectionEquipment",
        #     target_class=self.cim.ProtectionEquipment,
        #     target_mRID=ProtectionEquipment,
        # )
        return function_block
