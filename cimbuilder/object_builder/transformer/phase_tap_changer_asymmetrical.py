import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.transformer.phase_tap_changer_non_linear import (
    PhaseTapChangerNonLinearBuilder,
)


class PhaseTapChangerAsymmetricalBuilder(PhaseTapChangerNonLinearBuilder):
    """
    Builder for phase tap changers whose quadrature winding is at an angle other than 90 degrees,
    changing both phase and voltage magnitude. Builder functions to be called in the following order:
    * create() - instantiate the PhaseTapChangerAsymmetrical
    * add_connectivity() - attach the tap changer to its transformer end
    * add_electrical() - step range, normal step, voltage change per step, maximum reactance and winding angle
    * add_regulating_control() - neutral step and voltage, LTC settings and the TapChangerControl
    * add_ssh() - set the tap position
    """

    cim_class_name = "PhaseTapChangerAsymmetrical"

    def add_electrical(
        self,
        tap_changer: EL_BAL.PhaseTapChangerAsymmetrical,
        *,
        highStep: int,
        lowStep: int,
        normalStep: int,
        voltageStepIncrement: float,
        windingConnectionAngle: float | Qty,
        xMax: float | Qty | None = None,
    ) -> EL_BAL.PhaseTapChangerAsymmetrical:
        """
        Adds the step range, voltage change per step and winding angle
        * highStep: integer, highest step, e.g. 32
        * lowStep: integer, lowest step, e.g. -32
        * normalStep: integer, step used when no solved tap is available
        * voltageStepIncrement: voltage change per step of the quadrature winding, float in percentage (e.g. 1.25)
        * windingConnectionAngle: angle of the quadrature winding to the in-phase winding, float in degrees or Qty('deg')
        * xMax: reactance at the highest and lowest step, float in ohm or Qty('ohm')
        """
        super().add_electrical(
            tap_changer,
            highStep=highStep,
            lowStep=lowStep,
            normalStep=normalStep,
            voltageStepIncrement=voltageStepIncrement,
            xMax=xMax,
        )
        graph_write.set_attr(
            tap_changer, EL_BAL, "windingConnectionAngle", windingConnectionAngle
        )
        return tap_changer
