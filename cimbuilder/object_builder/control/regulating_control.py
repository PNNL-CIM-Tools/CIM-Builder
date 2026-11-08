import cimprofiles.cim18.cim18v17.regulating_control as RC
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class RegulatingControlBuilder(ObjectBuilder):
    """
    Builder for the control of regulating equipment, e.g. a switched capacitor bank.
    Builder functions to be called in the following order:
    * create() - instantiate the RegulatingControl
    * add_regulating_control() - monitored Terminal, mode and target band
    Attach the controlled equipment with e.g. LinearShuntCompensatorBuilder.add_regulating_control(RegulatingControl=...)
    """

    cim_class_name = "RegulatingControl"

    def add_regulating_control(
        self,
        control: RC.RegulatingControl,
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
    ) -> RC.RegulatingControl:
        """
        Adds the monitored Terminal and control settings
        * Terminal: mRID of the monitored Terminal, e.g. the capacitor's own terminal or a line terminal
        * mode: string, voltage|currentFlow|activePower|reactivePower|powerFactor|admittance|temperature|timeScheduled
        * targetValue: band center on the primary side (PT/CT secondary basis x ratio), float in the unit of mode (V, A, W, VAr)
        * targetDeadband: bandwidth on the primary side, float in the unit of mode
        * monitoredPhase: phase-code string of the sensed phase, e.g. A
        * ptRatio: PT ratio, primary to secondary, float (e.g. 60)
        * ctRatio: CT ratio, primary to secondary, float (e.g. 120)
        * discrete: boolean, true for stepped control (e.g. capacitor sections)
        * enabled: boolean, control is in service if true
        """
        rc: RC = self.cim  # type: ignore
        graph_write.set_attr(control, RC, "mode", rc.RegulatingControlModeKind(mode))
        graph_write.set_attr(control, RC, "targetValue", targetValue)
        graph_write.set_attr(control, RC, "targetDeadband", targetDeadband)
        if monitoredPhase is not None:
            graph_write.set_attr(control, RC, "monitoredPhase", rc.PhaseCode(monitoredPhase))
        graph_write.set_attr(control, RC, "ptRatio", ptRatio)
        graph_write.set_attr(control, RC, "ctRatio", ctRatio)
        graph_write.set_attr(control, RC, "discrete", discrete)
        graph_write.set_attr(control, RC, "enabled", enabled)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=control,
            profile_part=RC,
            association_name="Terminal",
            target_class=rc.Terminal,
            target_mRID=Terminal,
        )
        return control
