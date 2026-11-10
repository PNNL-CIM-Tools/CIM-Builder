import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.line.cable_info import CableInfoBuilder


class ConcentricNeutralCableInfoBuilder(CableInfoBuilder):
    """
    Builder for concentric neutral cables (equivalent to OpenDSS CNData). Builder functions to be called in the following order:
    * create() - instantiate the ConcentricNeutralCableInfo, e.g. cable_<name>
    * add_asset_info() - phase conductor, cable construction and neutral strands
    """

    cim_class_name = "ConcentricNeutralCableInfo"

    def add_asset_info(
        self,
        cable: AI.ConcentricNeutralCableInfo,
        *,
        diameterOverNeutral: float | Qty | None = None,
        neutralStrandCount: int | None = None,
        neutralStrandRadius: float | Qty | None = None,
        neutralStrandGmr: float | Qty | None = None,
        neutralStrandRDC20: float | Qty | None = None,
        **kwargs,
    ) -> AI.ConcentricNeutralCableInfo:
        """
        Adds the neutral strands, plus every CableInfoBuilder.add_asset_info field
        * diameterOverNeutral: diameter over the concentric neutral strands, float in m or Qty('in')
        * neutralStrandCount: integer, number of concentric neutral strands
        * neutralStrandRadius: outside radius of one neutral strand, float in m or Qty('in')
        * neutralStrandGmr: geometric mean radius of one neutral strand, float in m or Qty('ft'|'in')
        * neutralStrandRDC20: DC resistance of one neutral strand at 20 degC, float in ohm/m or Qty('ohm/mi')
        """
        super().add_asset_info(cable, **kwargs)
        graph_write.set_attr(cable, AI, "diameterOverNeutral", diameterOverNeutral)
        graph_write.set_attr(cable, AI, "neutralStrandCount", neutralStrandCount)
        graph_write.set_attr(cable, AI, "neutralStrandRadius", neutralStrandRadius)
        graph_write.set_attr(cable, AI, "neutralStrandGmr", neutralStrandGmr)
        graph_write.set_attr(cable, AI, "neutralStrandRDC20", neutralStrandRDC20)
        return cable
