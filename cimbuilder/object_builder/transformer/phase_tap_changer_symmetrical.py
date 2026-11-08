from cimbuilder.object_builder.transformer.phase_tap_changer_non_linear import (
    PhaseTapChangerNonLinearBuilder,
)


class PhaseTapChangerSymmetricalBuilder(PhaseTapChangerNonLinearBuilder):
    """
    Builder for phase tap changers whose quadrature winding shifts the phase with no change in
    voltage magnitude. Builder functions to be called in the following order:
    * create() - instantiate the PhaseTapChangerSymmetrical
    * add_connectivity() - attach the tap changer to its transformer end
    * add_electrical() - step range, normal step, voltage change per step and maximum reactance
    * add_regulating_control() - neutral step and voltage, LTC settings and the TapChangerControl
    * add_ssh() - set the tap position
    """

    cim_class_name = "PhaseTapChangerSymmetrical"
