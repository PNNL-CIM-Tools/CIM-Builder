from abc import ABC

import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class WireInfoBuilder(ObjectBuilder, ABC):
    """
    Base builder for conductor catalog data, use OverheadWireInfoBuilder or ConcentricNeutralCableInfoBuilder.
    Builder functions to be called in the following order:
    * create() - instantiate the wire info, e.g. wire_<name> or cable_<name>
    * add_asset_info() - conductor geometry, resistances and ratings
    Reference it from WireConfigurationBuilder.add_wire_sequence_configuration(WireInfo=...)
    """

    cim_class_name = "WireInfo"

    def add_asset_info(
        self,
        wire: AI.WireInfo,
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
    ) -> AI.WireInfo:
        """
        Adds the conductor data
        * gmr: geometric mean radius of the conductor, float in m or Qty('ft'|'in')
        * radius: outside radius of the conductor, float in m or Qty('in')
        * rAC25: AC resistance at 25 degC, float in ohm/m or Qty('ohm/mi')
        * rAC50: AC resistance at 50 degC, float in ohm/m or Qty('ohm/mi')
        * rDC20: DC resistance at 20 degC, float in ohm/m or Qty('ohm/mi')
        * ratedCurrent: normal ampacity, float in A or Qty('A')
        * ratedVoltage: rated voltage, float in V or Qty('kV')
        * insulated: boolean, conductor is insulated if true
        * insulationThickness: thickness of the insulation, float in m or Qty('mm'|'in')
        """
        graph_write.set_attr(wire, AI, "gmr", gmr)
        graph_write.set_attr(wire, AI, "radius", radius)
        graph_write.set_attr(wire, AI, "rAC25", rAC25)
        graph_write.set_attr(wire, AI, "rAC50", rAC50)
        graph_write.set_attr(wire, AI, "rDC20", rDC20)
        graph_write.set_attr(wire, AI, "ratedCurrent", ratedCurrent)
        graph_write.set_attr(wire, AI, "ratedVoltage", ratedVoltage)
        graph_write.set_attr(wire, AI, "insulated", insulated)
        graph_write.set_attr(wire, AI, "insulationThickness", insulationThickness)
        return wire
