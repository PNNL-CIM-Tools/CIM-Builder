import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.line.cable_info import CableInfoBuilder


class ConcentricNeutralCableInfoBuilder(CableInfoBuilder):
    """
    Builder for concentric neutral cables (equivalent to OpenDSS CNData). Builder functions to be called in the following order:
    * create() - instantiate the ConcentricNeutralCableInfo, e.g. cable_<name>
    * add_asset_info() - phase conductor, cable diameters and neutral strands
    """

    cim_class_name = "ConcentricNeutralCableInfo"

    def add_asset_info(
        self,
        cable: AI.ConcentricNeutralCableInfo,
        *,
        gmr: float | Qty | None = None,
        radius: float | Qty | None = None,
        rAC25: float | Qty | None = None,
        rAC50: float | Qty | None = None,
        rDC20: float | Qty | None = None,
        ratedCurrent: float | Qty | None = None,
        ratedVoltage: float | Qty | None = None,
        insulated: bool | None = None,
        insulationThickness: float | Qty | None = None,
        diameterOverInsulation: float | Qty | None = None,
        diameterOverJacket: float | Qty | None = None,
        neutralStrandCount: int | None = None,
        neutralStrandRadius: float | Qty | None = None,
        neutralStrandGmr: float | Qty | None = None,
        neutralStrandRDC20: float | Qty | None = None,
    ) -> AI.ConcentricNeutralCableInfo:
        """
        Adds the phase conductor, cable diameters and neutral strands
        * gmr: geometric mean radius of the phase conductor, float in m or Qty('ft'|'in')
        * radius: outside radius of the phase conductor, float in m or Qty('in')
        * rAC25: AC resistance of the phase conductor at 25 degC, float in ohm/m or Qty('ohm/mi')
        * rAC50: AC resistance of the phase conductor at 50 degC, float in ohm/m or Qty('ohm/mi')
        * rDC20: DC resistance of the phase conductor at 20 degC, float in ohm/m or Qty('ohm/mi')
        * ratedCurrent: normal ampacity, float in A or Qty('A')
        * ratedVoltage: rated voltage, float in V or Qty('kV')
        * insulated: boolean, conductor is insulated if true
        * insulationThickness: thickness of the insulation, float in m or Qty('mm'|'in')
        * diameterOverInsulation: diameter over the insulation, float in m or Qty('in')
        * diameterOverJacket: outside diameter of the cable, float in m or Qty('in')
        * neutralStrandCount: integer, number of concentric neutral strands
        * neutralStrandRadius: outside radius of one neutral strand, float in m or Qty('in')
        * neutralStrandGmr: geometric mean radius of one neutral strand, float in m or Qty('ft'|'in')
        * neutralStrandRDC20: DC resistance of one neutral strand at 20 degC, float in ohm/m or Qty('ohm/mi')
        """
        super().add_asset_info(
            cable,
            gmr=gmr,
            radius=radius,
            rAC25=rAC25,
            rAC50=rAC50,
            rDC20=rDC20,
            ratedCurrent=ratedCurrent,
            ratedVoltage=ratedVoltage,
            insulated=insulated,
            insulationThickness=insulationThickness,
            diameterOverInsulation=diameterOverInsulation,
            diameterOverJacket=diameterOverJacket,
        )
        graph_write.set_attr(cable, AI, "neutralStrandCount", neutralStrandCount)
        graph_write.set_attr(cable, AI, "neutralStrandRadius", neutralStrandRadius)
        graph_write.set_attr(cable, AI, "neutralStrandGmr", neutralStrandGmr)
        graph_write.set_attr(cable, AI, "neutralStrandRDC20", neutralStrandRDC20)
        return cable
