from abc import ABC

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.regulating_control as RC
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class TapChangerBuilder(ObjectBuilder, ABC):
    """
    Base builder for tap changers on a PowerTransformerEnd or AutoTransformerEnd, use
    RatioTapChangerBuilder or PhaseTapChangerBuilder. Builder functions to be called in the following order:
    * create() - instantiate the tap changer
    * add_connectivity() - attach the tap changer to its transformer end
    * add_electrical() - step range and normal step
    * add_regulating_control() - neutral step and voltage, LTC settings and the TapChangerControl
    * add_ssh() - set the tap position
    """

    cim_class_name = "TapChanger"

    def add_connectivity(
        self,
        tap_changer: CN.TapChanger,
        *,
        TransformerEnd: mRID,
    ) -> CN.TapChanger:
        """
        Attaches the tap changer to its transformer end
        * TransformerEnd: mRID of the PowerTransformerEnd or AutoTransformerEnd with the tap changer
        """
        cn: CN = self.cim  # type: ignore
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=tap_changer,
            profile_part=CN,
            association_name="TransformerEnd",
            target_class=cn.TransformerEnd,
            target_mRID=TransformerEnd,
        )
        return tap_changer

    def add_electrical(
        self,
        tap_changer: EL_BAL.TapChanger,
        *,
        highStep: int,
        lowStep: int,
        normalStep: int,
    ) -> EL_BAL.TapChanger:
        """
        Adds the step range of the tap changer
        * highStep: integer, highest step, e.g. 16
        * lowStep: integer, lowest step, e.g. -16
        * normalStep: integer, step used when no solved tap is available
        """
        graph_write.set_attr(tap_changer, EL_BAL, "highStep", highStep)
        graph_write.set_attr(tap_changer, EL_BAL, "lowStep", lowStep)
        graph_write.set_attr(tap_changer, EL_BAL, "normalStep", normalStep)
        return tap_changer

    def add_regulating_control(
        self,
        tap_changer: RC.TapChanger,
        *,
        neutralStep: int,
        neutralU: float | Qty,
        TapChangerControl: mRID | None = None,
        ltcFlag: bool | None = None,
        controlEnabled: bool | None = None,
        ptRatio: float | None = None,
        ptPhase: str | None = None,
        ctRatio: float | None = None,
        ctRating: float | None = None,
        initialDelay: float | Qty | None = None,
        subsequentDelay: float | Qty | None = None,
    ) -> RC.TapChanger:
        """
        Adds the neutral step and LTC settings
        * neutralStep: integer, step with no voltage or phase change, e.g. 0
        * neutralU: voltage at the neutral step, float in V or Qty('kV')
        * TapChangerControl: mRID of the TapChangerControl. None for a manual tap changer
        * ltcFlag: boolean, tap can change under load if true
        * controlEnabled: boolean, regulating control is active if true
        * ptRatio: potential transformer ratio, float (e.g. 7620/120 = 63.5)
        * ptPhase: phase-code string of the potential transformer, e.g. A
        * ctRatio: current transformer ratio, float
        * ctRating: current transformer primary rating, float in A
        * initialDelay: time delay before the first tap change, float in s or Qty('s')
        * subsequentDelay: time delay between later tap changes, float in s or Qty('s')
        """
        rc: RC = self.cim  # type: ignore
        graph_write.set_attr(tap_changer, RC, "neutralStep", neutralStep)
        graph_write.set_attr(tap_changer, RC, "neutralU", neutralU)
        graph_write.set_attr(tap_changer, RC, "ltcFlag", ltcFlag)
        graph_write.set_attr(tap_changer, RC, "controlEnabled", controlEnabled)
        graph_write.set_attr(tap_changer, RC, "ptRatio", ptRatio)
        if ptPhase is not None:
            graph_write.set_attr(tap_changer, RC, "ptPhase", rc.PhaseCode(ptPhase))
        graph_write.set_attr(tap_changer, RC, "ctRatio", ctRatio)
        graph_write.set_attr(tap_changer, RC, "ctRating", ctRating)
        graph_write.set_attr(tap_changer, RC, "initialDelay", initialDelay)
        graph_write.set_attr(tap_changer, RC, "subsequentDelay", subsequentDelay)
        if TapChangerControl is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=tap_changer,
                profile_part=RC,
                association_name="TapChangerControl",
                target_class=rc.TapChangerControl,
                target_mRID=TapChangerControl,
            )
        return tap_changer

    def add_ssh(
        self,
        tap_changer: SSH.TapChanger,
        *,
        step: float,
    ) -> SSH.TapChanger:
        """
        Adds real-time values from measurement or basecase.
        * step: tap position, float between lowStep and highStep
        """
        graph_write.set_attr(tap_changer, SSH, "step", step)
        return tap_changer
