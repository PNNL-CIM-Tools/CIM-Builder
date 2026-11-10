from abc import ABC

import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.transformer.phase_tap_changer import (
    PhaseTapChangerBuilder,
)


class PhaseTapChangerNonLinearBuilder(PhaseTapChangerBuilder, ABC):
    """
    Base builder for phase tap changers whose phase shift follows from a voltage step on a
    quadrature winding, use PhaseTapChangerSymmetricalBuilder or PhaseTapChangerAsymmetricalBuilder.
    Builder functions to be called in the following order:
    * create() - instantiate the phase tap changer
    * add_connectivity() - attach the tap changer to its transformer end
    * add_electrical() - step range, normal step, voltage change per step and maximum reactance
    * add_regulating_control() - neutral step and voltage, LTC settings and the TapChangerControl
    * add_ssh() - set the tap position
    """

    cim_class_name = "PhaseTapChangerNonLinear"

    def add_electrical(
        self,
        tap_changer: EL_BAL.PhaseTapChangerNonLinear,
        *,
        highStep: int,
        lowStep: int,
        normalStep: int,
        voltageStepIncrement: float,
        xMax: float | Qty | None = None,
    ) -> EL_BAL.PhaseTapChangerNonLinear:
        """
        Adds the step range and voltage change per step
        * highStep: integer, highest step, e.g. 32
        * lowStep: integer, lowest step, e.g. -32
        * normalStep: integer, step used when no solved tap is available
        * voltageStepIncrement: voltage change per step of the quadrature winding, float in percentage (e.g. 1.25)
        * xMax: reactance at the highest and lowest step, float in ohm or Qty('ohm')
        """
        super().add_electrical(
            tap_changer, highStep=highStep, lowStep=lowStep, normalStep=normalStep
        )
        graph_write.set_attr(tap_changer, EL_BAL, "voltageStepIncrement", voltageStepIncrement)
        graph_write.set_attr(tap_changer, EL_BAL, "xMax", xMax)
        return tap_changer
