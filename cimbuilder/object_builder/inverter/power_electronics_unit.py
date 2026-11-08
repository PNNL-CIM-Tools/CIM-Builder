import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class PowerElectronicsUnitBuilder(ObjectBuilder):
    cim_class_name = "PowerElectronicsUnit"

    def add_electrical(
        self,
        unit: EL_BAL.PowerElectronicsUnit,
        *,
        minP: float | Qty | None = None,
        maxP: float | Qty | None = None,
        aggregate: bool | None = None,
        PowerElectronicsConnection: str,
    ) -> EL_BAL.PowerElectronicsUnit:
        """Adds electrical_balanced.PowerElectronicsUnit's fixed-unit parameters.
        * minP: minimum nameplate unit, float in watts or Qty("kW"|"MW")
        * minP: minimum nameplate unit, float in watts or Qty("kW"|"MW")
        * PowerElectronicsConnection: mRID of the inverter this unit is connected to
        """

        el_bal: EL_BAL = self.cim  # type:ignore
        graph_write.set_attr(unit, EL_BAL, "minP", minP)
        graph_write.set_attr(unit, EL_BAL, "maxP", maxP)
        graph_write.set_attr(unit, EL_BAL, "aggregate", aggregate)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=unit,
            profile_part=EL_BAL,
            association_name="PowerElectronicsConnection",
            target_class=el_bal,
            target_mRID=PowerElectronicsConnection,
        )

        return unit

    def add_ssh(
        self,
        unit: SSH.PowerElectronicsUnit,
        *,
        p: float | Qty | None = None,
        inService: bool | None = None,
    ) -> SSH.PowerElectronicsUnit:
        """
        Adds real-time p/q values from measurement or basecase.
        Use load sign convention (positive = flow out of node)
        * p: instantaneous active power, float in watts or Qty('kW'|'MW')
        * q: instantaneous reactive power, float in VArs or Qty('kVAr'|'MVAr')
        * inService: boolean, unit is de-energized if false
        """
        graph_write.set_attr(unit, SSH, "p", p)
        graph_write.set_attr(unit, SSH, "inService", inService)
        return unit


class PhotoVoltaicUnitBuilder(PowerElectronicsUnitBuilder):
    cim_class_name = "PhotoVoltaicUnit"


class PowerElectronicsWindUnitBuilder(PowerElectronicsUnitBuilder):
    cim_class_name = "PowerElectronicsWindUnit"


class ChargingUnitBuilder(PowerElectronicsUnitBuilder):
    cim_class_name = "ChargingUnit"


class BatteryUnitBuilder(PowerElectronicsUnitBuilder):
    cim_class_name = "BatteryUnit"

    def add_electrical(
        self,
        unit: EL_BAL.BatteryUnit,
        *,
        minP: float | Qty | None = None,
        maxP: float | Qty | None = None,
        ratedE: float | Qty | None = None,
        minimumE: float | Qty | None = None,
        idlingP: float | Qty | None = None,
        chargingEfficiency: float | Qty | None = None,
        dischargingEfficiency: float | Qty | None = None,
        aggregate: bool | None = None,
        PowerElectronicsConnection: str,
    ) -> EL_BAL.BatteryUnit:

        super().add_electrical(
            unit,
            minP=minP,
            maxP=maxP,
            aggregate=aggregate,
            PowerElectronicsConnection=PowerElectronicsConnection,
        )

        graph_write.set_attr(unit, EL_BAL, "ratedE", ratedE)
        graph_write.set_attr(unit, EL_BAL, "minimumE", minimumE)
        graph_write.set_attr(unit, EL_BAL, "idlingP", idlingP)
        graph_write.set_attr(unit, EL_BAL, "chargingEfficiency", chargingEfficiency)
        graph_write.set_attr(
            unit, EL_BAL, "dischargingEfficiency", dischargingEfficiency
        )

        return unit

    def add_ssh(
        self,
        unit: SSH.BatteryUnit,
        *,
        p: float | Qty | None = None,
        storedE: float | Qty | None = None,
        batteryState: str | None = None,
        inService: bool | None = None,
    ) -> SSH.BatteryUnit:
        ssh: SSH = self.cim  # type: ignore
        super().add_ssh(unit, p=p, inService=inService)
        graph_write.set_attr(unit, SSH, "storedE", storedE)
        if batteryState is not None:
            graph_write.set_attr(
                unit, SSH, "batteryState", ssh.BatteryStateKind(batteryState)
            )
        return unit
