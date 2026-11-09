from abc import ABC

import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.conducting_asset_info import ConductingAssetInfoBuilder


class WireInfoBuilder(ConductingAssetInfoBuilder, ABC):
    """
    Base builder for conductor catalog data, use OverheadWireInfoBuilder or ConcentricNeutralCableInfoBuilder.
    Builder functions to be called in the following order:
    * create() - instantiate the wire info, e.g. wire_<name> or cable_<name>
    * add_asset_info() - conductor geometry, resistances and ratings
    Reference it from WireConfigurationBuilder.add_wire_sequence_configuration(WireInfo=...)
    """

    cim_class_name = "WireInfo"
    # cim18v17 types WireInfo.constructionKind as WireMaterialKind, CableInfo's as CableConstructionKind
    construction_kind_enum = "WireMaterialKind"

    def add_asset_info(
        self,
        wire: AI.WireInfo,
        *,
        purpose: str | None = None,
        sizeDescription: str | None = None,
        material: str | None = None,
        constructionKind: str | None = None,
        crossSection: float | Qty | None = None,
        gmr: float | Qty | None = None,
        radius: float | Qty | None = None,
        coreRadius: float | Qty | None = None,
        strandCount: int | None = None,
        strandRadius: float | Qty | None = None,
        coreStrandCount: int | None = None,
        coreStrandRadius: float | Qty | None = None,
        rAC25: float | Qty | None = None,
        rAC50: float | Qty | None = None,
        rAC75: float | Qty | None = None,
        rDC20: float | Qty | None = None,
        insulated: bool | None = None,
        insulationMaterial: str | None = None,
        insulationThickness: float | Qty | None = None,
        ratedStrength: float | Qty | None = None,
        **kwargs,
    ) -> AI.WireInfo:
        """
        Adds the conductor data, plus the ConductingAssetInfoBuilder ratings (phaseCount, ratedCurrent, ...)
        * purpose: free text, e.g. 'phase', 'neutral'
        * sizeDescription: free text conductor size, e.g. '556.5 kcmil', '#2'
        * material: string, aaac|acsr|aluminum|aluminumAlloy|aluminumAlloySteel|aluminumSteel|copper|other|steel
        * constructionKind: string, WireMaterialKind for overhead wire, CableConstructionKind for cables
          (compacted|compressed|other|sector|segmental|solid|stranded)
        * crossSection: conductor cross-section area, float in m^2 or Qty('mm^2')
        * gmr: geometric mean radius of the conductor, float in m or Qty('ft'|'in')
        * radius: outside radius of the conductor, float in m or Qty('in')
        * coreRadius: radius of the steel core, float in m or Qty('in')
        * strandCount: integer, number of conductor strands
        * strandRadius: radius of one conductor strand, float in m or Qty('in')
        * coreStrandCount: integer, number of core strands
        * coreStrandRadius: radius of one core strand, float in m or Qty('in')
        * rAC25: AC resistance at 25 degC, float in ohm/m or Qty('ohm/mi')
        * rAC50: AC resistance at 50 degC, float in ohm/m or Qty('ohm/mi')
        * rAC75: AC resistance at 75 degC, float in ohm/m or Qty('ohm/mi')
        * rDC20: DC resistance at 20 degC, float in ohm/m or Qty('ohm/mi')
        * insulated: boolean, conductor is insulated if true
        * insulationMaterial: WireInsulationKind string, e.g. crosslinkedPolyethylene|ethylenePropyleneRubber|oilPaper|other
        * insulationThickness: thickness of the insulation, float in m or Qty('mm'|'in')
        * ratedStrength: breaking strength, float in N or Qty('lbf')
        """
        super().add_asset_info(wire, **kwargs)
        graph_write.set_attr(wire, AI, "purpose", purpose)
        graph_write.set_attr(wire, AI, "sizeDescription", sizeDescription)
        graph_write.set_attr(wire, AI, "material", self._enum("WireMaterialKind", material))
        graph_write.set_attr(
            wire, AI, "constructionKind", self._enum(self.construction_kind_enum, constructionKind)
        )
        graph_write.set_attr(wire, AI, "crossSection", crossSection)
        graph_write.set_attr(wire, AI, "gmr", gmr)
        graph_write.set_attr(wire, AI, "radius", radius)
        graph_write.set_attr(wire, AI, "coreRadius", coreRadius)
        graph_write.set_attr(wire, AI, "strandCount", strandCount)
        graph_write.set_attr(wire, AI, "strandRadius", strandRadius)
        graph_write.set_attr(wire, AI, "coreStrandCount", coreStrandCount)
        graph_write.set_attr(wire, AI, "coreStrandRadius", coreStrandRadius)
        graph_write.set_attr(wire, AI, "rAC25", rAC25)
        graph_write.set_attr(wire, AI, "rAC50", rAC50)
        graph_write.set_attr(wire, AI, "rAC75", rAC75)
        graph_write.set_attr(wire, AI, "rDC20", rDC20)
        graph_write.set_attr(wire, AI, "insulated", insulated)
        graph_write.set_attr(
            wire, AI, "insulationMaterial", self._enum("WireInsulationKind", insulationMaterial)
        )
        graph_write.set_attr(wire, AI, "insulationThickness", insulationThickness)
        graph_write.set_attr(wire, AI, "ratedStrength", ratedStrength)
        return wire
