from abc import ABC

from cimbuilder.object_builder.transformer.tap_changer import TapChangerBuilder


class PhaseTapChangerBuilder(TapChangerBuilder, ABC):
    """
    Base builder for phase tap changers on the PowerTransformerEnd of a phase-shifting transformer,
    use PhaseTapChangerLinearBuilder, PhaseTapChangerSymmetricalBuilder, PhaseTapChangerAsymmetricalBuilder
    or PhaseTapChangerTabularBuilder. Builder functions to be called in the following order:
    * create() - instantiate the phase tap changer
    * add_connectivity() - attach the tap changer to its transformer end
    * add_electrical() - step range, normal step and phase shift per step
    * add_regulating_control() - neutral step and voltage, LTC settings and the TapChangerControl
    * add_ssh() - set the tap position
    """

    cim_class_name = "PhaseTapChanger"
