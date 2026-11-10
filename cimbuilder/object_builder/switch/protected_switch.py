import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, graph_write

from cimbuilder.object_builder.switch.switch import SwitchBuilder


class ProtectedSwitchBuilder(SwitchBuilder):
    cim_class_name = "ProtectedSwitch"

    def add_electrical(
        self,
        switch: EL_BAL.ProtectedSwitch,
        *,
        ratedCurrent: float | Qty | None = None,
        gangOperated: bool | None = None,
        motorOperated: bool | None = None,
        remotelyOperated: bool | None = None,
        loadBreak: bool | None = None,
        breakingCapacity: float | Qty | None = None,
        makingCapacity: float | Qty | None = None,
    ) -> EL_BAL.ProtectedSwitch:
        """
        Adds balanced electrical parameters for the protected switch
        * ratedCurrent: max normal operating current, float in amps or Qty('A')
        * gangOperated: boolean, all phases operate together if true
        * motorOperated: boolean, operated by motor (not hand-crank) if true
        * remotelyOperated: boolean, can be operated by SCADA if true
        * loadBreak: boolean, can be opened under load (has vacuum/SF6/arc chute) if true ratings.
        * breakingCapacity: max current this switch can safely interrupt, float in amps or Qty('A')
        * makingCapacity: max current this switch can safely close onto, float in amps or Qty('A')
        """
        super().add_electrical(
            switch=switch,
            ratedCurrent=ratedCurrent,
            gangOperated=gangOperated,
            motorOperated=motorOperated,
            remotelyOperated=remotelyOperated,
            loadBreak=loadBreak,
        )
        graph_write.set_attr(switch, EL_BAL, "breakingCapacity", breakingCapacity)
        graph_write.set_attr(switch, EL_BAL, "makingCapacity", makingCapacity)
        return switch


class BreakerBuilder(ProtectedSwitchBuilder):
    cim_class_name = "Breaker"

    def add_electrical(
        self,
        switch: EL_BAL.Breaker,
        *,
        ratedCurrent: float | Qty | None = None,
        gangOperated: bool | None = None,
        motorOperated: bool | None = None,
        remotelyOperated: bool | None = None,
        loadBreak: bool | None = None,
        breakingCapacity: float | Qty | None = None,
        makingCapacity: float | Qty | None = None,
        inTransitTime: float | Qty | None = None,
    ) -> EL_BAL.Breaker:
        """
        Adds balanced electrical parameters for the protected switch
        * ratedCurrent: max normal operating current, float in amps or Qty('A')
        * gangOperated: boolean, all phases operate together if true
        * motorOperated: boolean, operated by motor (not hand-crank) if true
        * remotelyOperated: boolean, can be operated by SCADA if true
        * loadBreak: boolean, can be opened under load (has vacuum/SF6/arc chute) if true ratings.
        * breakingCapacity: max current this switch can safely interrupt, float in amps or Qty('A')
        * makingCapacity: max current this switch can safely close onto, float in amps or Qty('A')
        * inTransitTime: time the breaker's contacts spend transitioning from closed to open, float in seconds or Qty('s')
        """
        super().add_electrical(
            switch=switch,
            breakingCapacity=breakingCapacity,
            makingCapacity=makingCapacity,
            ratedCurrent=ratedCurrent,
            gangOperated=gangOperated,
            motorOperated=motorOperated,
            remotelyOperated=remotelyOperated,
            loadBreak=loadBreak,
        )
        graph_write.set_attr(switch, EL_BAL, "inTransitTime", inTransitTime)
        return switch


class RecloserBuilder(ProtectedSwitchBuilder):
    cim_class_name = "Recloser"


class LoadBreakSwitchBuilder(ProtectedSwitchBuilder):
    cim_class_name = "LoadBreakSwitch"
