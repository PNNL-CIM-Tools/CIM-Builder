import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
from cimtables import graph_write

from cimbuilder.object_builder.transformer.phase_tap_changer import (
    PhaseTapChangerBuilder,
)

mRID = str


class PhaseTapChangerTabularBuilder(PhaseTapChangerBuilder):
    """
    Builder for phase tap changers whose angle, ratio and impedance per step come from a
    PhaseTapChangerTable. Builder functions to be called in the following order:
    * create() - instantiate the PhaseTapChangerTabular
    * add_connectivity() - attach the tap changer to its transformer end
    * add_electrical() - step range, normal step and the PhaseTapChangerTable
    * add_regulating_control() - neutral step and voltage, LTC settings and the TapChangerControl
    * add_ssh() - set the tap position
    Build the table first with PhaseTapChangerTableBuilder
    """

    cim_class_name = "PhaseTapChangerTabular"

    def add_electrical(
        self,
        tap_changer: EL_BAL.PhaseTapChangerTabular,
        *,
        highStep: int,
        lowStep: int,
        normalStep: int,
        PhaseTapChangerTable: mRID,
    ) -> EL_BAL.PhaseTapChangerTabular:
        """
        Adds the step range and the table of values per step
        * highStep: integer, highest step, e.g. 32
        * lowStep: integer, lowest step, e.g. -32
        * normalStep: integer, step used when no solved tap is available
        * PhaseTapChangerTable: mRID of the PhaseTapChangerTable, may be shared by several tap changers
        """
        el_bal: EL_BAL = self.cim  # type: ignore
        super().add_electrical(
            tap_changer, highStep=highStep, lowStep=lowStep, normalStep=normalStep
        )
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=tap_changer,
            profile_part=EL_BAL,
            association_name="PhaseTapChangerTable",
            target_class=el_bal.PhaseTapChangerTable,
            target_mRID=PhaseTapChangerTable,
        )
        return tap_changer
