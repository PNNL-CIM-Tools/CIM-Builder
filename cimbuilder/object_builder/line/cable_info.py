from abc import ABC

import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.line.wire_info import WireInfoBuilder


class CableInfoBuilder(WireInfoBuilder, ABC):
    """
    Base builder for underground cables, use ConcentricNeutralCableInfoBuilder.
    Builder functions to be called in the following order:
    * create() - instantiate the cable info, e.g. cable_<name>
    * add_asset_info() - conductor geometry, resistances, ratings and cable diameters
    """

    cim_class_name = "CableInfo"

    def add_asset_info(
        self,
        cable: AI.CableInfo,
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
    ) -> AI.CableInfo:
        """
        Adds the conductor data and cable diameters
        * gmr: geometric mean radius of the phase conductor, float in m or Qty('ft'|'in')
        * radius: outside radius of the phase conductor, float in m or Qty('in')
        * rAC25: AC resistance at 25 degC, float in ohm/m or Qty('ohm/mi')
        * rAC50: AC resistance at 50 degC, float in ohm/m or Qty('ohm/mi')
        * rDC20: DC resistance at 20 degC, float in ohm/m or Qty('ohm/mi')
        * ratedCurrent: normal ampacity, float in A or Qty('A')
        * ratedVoltage: rated voltage, float in V or Qty('kV')
        * insulated: boolean, conductor is insulated if true
        * insulationThickness: thickness of the insulation, float in m or Qty('mm'|'in')
        * diameterOverInsulation: diameter over the insulation, float in m or Qty('in')
        * diameterOverJacket: outside diameter of the cable, float in m or Qty('in')
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
        )
        graph_write.set_attr(cable, AI, "diameterOverInsulation", diameterOverInsulation)
        graph_write.set_attr(cable, AI, "diameterOverJacket", diameterOverJacket)
        return cable
