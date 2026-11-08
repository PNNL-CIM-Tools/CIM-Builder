import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
from cimtables import graph_write

from cimbuilder.object_builder.transformer.tap_changer import TapChangerBuilder


class RatioTapChangerBuilder(TapChangerBuilder):
    """
    Builder for ratio tap changers: LTCs on a PowerTransformerEnd and step-voltage regulators
    on an AutoTransformerEnd. Builder functions to be called in the following order:
    * create() - instantiate the RatioTapChanger
    * add_connectivity() - attach the tap changer to its transformer end
    * add_electrical() - step range, normal step and voltage change per step
    * add_regulating_control() - neutral step and voltage, LTC settings and the TapChangerControl
    * add_ssh() - set the tap position
    """

    cim_class_name = "RatioTapChanger"

    def add_electrical(
        self,
        tap_changer: EL_BAL.RatioTapChanger,
        *,
        highStep: int,
        lowStep: int,
        normalStep: int,
        stepVoltageIncrement: float,
    ) -> EL_BAL.RatioTapChanger:
        """
        Adds the step range and voltage change per step
        * highStep: integer, highest boost step, e.g. 16
        * lowStep: integer, lowest buck step, e.g. -16
        * normalStep: integer, step used when no solved tap is available
        * stepVoltageIncrement: voltage change per step, float in percentage (e.g. 0.625)
        """
        super().add_electrical(
            tap_changer, highStep=highStep, lowStep=lowStep, normalStep=normalStep
        )
        graph_write.set_attr(
            tap_changer, EL_BAL, "stepVoltageIncrement", stepVoltageIncrement
        )
        return tap_changer
