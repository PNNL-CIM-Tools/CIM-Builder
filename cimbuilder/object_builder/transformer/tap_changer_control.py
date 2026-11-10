import cimprofiles.cim18.cim18v17.regulating_control as RC
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.control.regulating_control import (
    RegulatingControlBuilder,
)

mRID = str


class TapChangerControlBuilder(RegulatingControlBuilder):
    """
    Builder for the voltage control of one or more tap changers, e.g. three single-phase
    regulators on one controller. Builder functions to be called in the following order:
    * create() - instantiate the TapChangerControl
    * add_regulating_control() - regulated Terminal, target band, voltage limits and line drop compensation
    Attach tap changers with TapChangerBuilder.add_regulating_control(TapChangerControl=...)
    """

    cim_class_name = "TapChangerControl"

    def add_regulating_control(
        self,
        control: RC.TapChangerControl,
        *,
        Terminal: mRID,
        mode: str,
        targetValue: float,
        targetDeadband: float,
        monitoredPhase: str | None = None,
        ptRatio: float | None = None,
        ctRatio: float | None = None,
        discrete: bool | None = None,
        enabled: bool | None = None,
        lineDropCompensation: bool | None = None,
        lineDropR: float | Qty | None = None,
        lineDropX: float | Qty | None = None,
        maxLimitVoltage: float | Qty | None = None,
        minLimitVoltage: float | Qty | None = None,
        reversible: bool | None = None,
    ) -> RC.TapChangerControl:
        """
        Adds the regulated Terminal and control settings
        * Terminal: mRID of the regulated Terminal, the L side of a type A regulator or the LV side of an LTC
        * mode: string, voltage|currentFlow|activePower|reactivePower|powerFactor|admittance|temperature|timeScheduled
        * targetValue: band center, float in V on the primary side (PT secondary basis x ptRatio)
        * targetDeadband: bandwidth, float in V on the primary side (PT secondary basis x ptRatio)
        * monitoredPhase: phase-code string of the sensed phase, e.g. A
        * ptRatio: PT ratio, primary to secondary, float (e.g. 63.5)
        * ctRatio: CT ratio, primary to secondary, float
        * discrete: boolean, true for stepped tap control
        * enabled: boolean, control is in service if true
        * lineDropCompensation: boolean, line drop compensation is used if true
        * lineDropR: line drop compensator resistance, float in ohm or Qty('ohm')
        * lineDropX: line drop compensator reactance, float in ohm or Qty('ohm')
        * maxLimitVoltage: upper voltage limit (runaway protection), float in V or Qty('kV')
        * minLimitVoltage: lower voltage limit (runaway protection), float in V or Qty('kV')
        * reversible: boolean, the control can regulate in reverse power flow if true
        """
        super().add_regulating_control(
            control,
            Terminal=Terminal,
            mode=mode,
            targetValue=targetValue,
            targetDeadband=targetDeadband,
            monitoredPhase=monitoredPhase,
            ptRatio=ptRatio,
            ctRatio=ctRatio,
            discrete=discrete,
            enabled=enabled,
        )
        graph_write.set_attr(control, RC, "lineDropCompensation", lineDropCompensation)
        graph_write.set_attr(control, RC, "lineDropR", lineDropR)
        graph_write.set_attr(control, RC, "lineDropX", lineDropX)
        graph_write.set_attr(control, RC, "maxLimitVoltage", maxLimitVoltage)
        graph_write.set_attr(control, RC, "minLimitVoltage", minLimitVoltage)
        graph_write.set_attr(control, RC, "reversible", reversible)
        return control
