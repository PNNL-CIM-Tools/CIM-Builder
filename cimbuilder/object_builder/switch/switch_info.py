import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.conducting_asset_info import ConductingAssetInfoBuilder


class SwitchInfoBuilder(ConductingAssetInfoBuilder):
    """
    Builder for switch catalog data (GDM CircuitBreakerEquipment). Builder functions to be called in the following order:
    * create() - instantiate the SwitchInfo, e.g. sw_info_<name>
    * add_asset_info() - interrupting rating, operation and gas/oil data
    Reference it from an instance with add_asset_datasheet(AssetDatasheet=...)
    """

    cim_class_name = "SwitchInfo"

    def add_asset_info(
        self,
        info: AI.SwitchInfo,
        *,
        breakingCapacity: float | Qty | None = None,
        ratedInterruptingTime: float | Qty | None = None,
        ratedImpulseWithstandVoltage: float | Qty | None = None,
        isSinglePhase: bool | None = None,
        isUnganged: bool | None = None,
        lowPressureAlarm: float | Qty | None = None,
        lowPressureLockOut: float | Qty | None = None,
        oilVolumePerTank: float | Qty | None = None,
        **kwargs,
    ) -> AI.SwitchInfo:
        """
        Adds the switch nameplate, plus the ConductingAssetInfoBuilder ratings (phaseCount, ratedCurrent, ...)
        * breakingCapacity: maximum current the switch can interrupt, float in A or Qty('kA')
        * ratedInterruptingTime: rated interrupting time, float in s or Qty('ms')
        * ratedImpulseWithstandVoltage: BIL, float in V or Qty('kV')
        * isSinglePhase: boolean, single-phase device if true
        * isUnganged: boolean, phases operate independently if true
        * lowPressureAlarm: gas pressure that raises an alarm, float in Pa or Qty('psi')
        * lowPressureLockOut: gas pressure that locks out operation, float in Pa or Qty('psi')
        * oilVolumePerTank: oil volume per tank, float in m^3 or Qty('gallon')
        """
        super().add_asset_info(info, **kwargs)
        graph_write.set_attr(info, AI, "breakingCapacity", breakingCapacity)
        graph_write.set_attr(info, AI, "ratedInterruptingTime", ratedInterruptingTime)
        graph_write.set_attr(info, AI, "ratedImpulseWithstandVoltage", ratedImpulseWithstandVoltage)
        graph_write.set_attr(info, AI, "isSinglePhase", isSinglePhase)
        graph_write.set_attr(info, AI, "isUnganged", isUnganged)
        graph_write.set_attr(info, AI, "lowPressureAlarm", lowPressureAlarm)
        graph_write.set_attr(info, AI, "lowPressureLockOut", lowPressureLockOut)
        graph_write.set_attr(info, AI, "oilVolumePerTank", oilVolumePerTank)
        return info
