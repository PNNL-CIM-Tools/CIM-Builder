import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.transformer.phase_tap_changer import (
    PhaseTapChangerBuilder,
)


class PhaseTapChangerLinearBuilder(PhaseTapChangerBuilder):
    """
    Builder for phase tap changers with a fixed phase shift per step and no change in voltage magnitude.
    Builder functions to be called in the following order:
    * create() - instantiate the PhaseTapChangerLinear
    * add_connectivity() - attach the tap changer to its transformer end
    * add_electrical() - step range, normal step, phase shift per step and maximum reactance
    * add_regulating_control() - neutral step and voltage, LTC settings and the TapChangerControl
    * add_ssh() - set the tap position
    """

    cim_class_name = "PhaseTapChangerLinear"

    def add_electrical(
        self,
        tap_changer: EL_BAL.PhaseTapChangerLinear,
        *,
        highStep: int,
        lowStep: int,
        normalStep: int,
        stepPhaseShiftIncrement: float | Qty,
        xMax: float | Qty | None = None,
    ) -> EL_BAL.PhaseTapChangerLinear:
        """
        Adds the step range and phase shift per step
        * highStep: integer, highest step, e.g. 32
        * lowStep: integer, lowest step, e.g. -32
        * normalStep: integer, step used when no solved tap is available
        * stepPhaseShiftIncrement: phase shift per step, float in degrees or Qty('deg')
        * xMax: reactance at the highest and lowest step, float in ohm or Qty('ohm')
        """
        super().add_electrical(
            tap_changer, highStep=highStep, lowStep=lowStep, normalStep=normalStep
        )
        graph_write.set_attr(
            tap_changer, EL_BAL, "stepPhaseShiftIncrement", stepPhaseShiftIncrement
        )
        graph_write.set_attr(tap_changer, EL_BAL, "xMax", xMax)
        return tap_changer
