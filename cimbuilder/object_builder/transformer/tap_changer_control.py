import cimprofiles.cim18.cim18v17.regulating_control as RC
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class TapChangerControlBuilder(ObjectBuilder):
    """
    Builder for the voltage control of one or more tap changers, e.g. three single-phase
    regulators on one controller. Builder functions to be called in the following order:
    * create() - instantiate the TapChangerControl
    * add_regulating_control() - regulated Terminal, target band and line drop compensation
    Attach tap changers with TapChangerBuilder.add_regulating_control(TapChangerControl=...)
    """

    cim_class_name = "TapChangerControl"

    def add_regulating_control(
        self,
        control: RC.TapChangerControl,
        *,
        Terminal: mRID,
        mode: str,
        monitoredPhase: str,
        targetValue: float,
        targetDeadband: float,
        discrete: bool | None = None,
        enabled: bool | None = None,
        lineDropCompensation: bool | None = None,
        lineDropR: float | Qty | None = None,
        lineDropX: float | Qty | None = None,
    ) -> RC.TapChangerControl:
        """
        Adds the regulated Terminal and control settings
        * Terminal: mRID of the regulated Terminal, the L side of a type A regulator or the LV side of an LTC
        * mode: string, voltage|currentFlow|activePower|reactivePower|powerFactor|admittance|temperature|timeScheduled
        * monitoredPhase: phase-code string of the sensed phase, e.g. A
        * targetValue: band center, float in V on the primary side (PT secondary basis x ptRatio)
        * targetDeadband: bandwidth, float in V on the primary side (PT secondary basis x ptRatio)
        * discrete: boolean, true for stepped tap control
        * enabled: boolean, control is in service if true
        * lineDropCompensation: boolean, line drop compensation is used if true
        * lineDropR: line drop compensator resistance, float in ohm or Qty('ohm')
        * lineDropX: line drop compensator reactance, float in ohm or Qty('ohm')
        """
        rc: RC = self.cim  # type: ignore
        graph_write.set_attr(control, RC, "mode", rc.RegulatingControlModeKind(mode))
        graph_write.set_attr(control, RC, "monitoredPhase", rc.PhaseCode(monitoredPhase))
        graph_write.set_attr(control, RC, "targetValue", targetValue)
        graph_write.set_attr(control, RC, "targetDeadband", targetDeadband)
        graph_write.set_attr(control, RC, "discrete", discrete)
        graph_write.set_attr(control, RC, "enabled", enabled)
        graph_write.set_attr(control, RC, "lineDropCompensation", lineDropCompensation)
        graph_write.set_attr(control, RC, "lineDropR", lineDropR)
        graph_write.set_attr(control, RC, "lineDropX", lineDropX)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=control,
            profile_part=RC,
            association_name="Terminal",
            target_class=rc.Terminal,
            target_mRID=Terminal,
        )
        return control
