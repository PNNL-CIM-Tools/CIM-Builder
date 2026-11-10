from abc import ABC

import cimprofiles.cim18.cim18v17.asset_info as AI
from cimtables import Qty, graph_write

from cimbuilder.object_builder.line.wire_info import WireInfoBuilder


class CableInfoBuilder(WireInfoBuilder, ABC):
    """
    Base builder for underground cables, use ConcentricNeutralCableInfoBuilder.
    Builder functions to be called in the following order:
    * create() - instantiate the cable info, e.g. cable_<name>
    * add_asset_info() - conductor geometry, resistances, ratings and cable construction
    """

    cim_class_name = "CableInfo"
    construction_kind_enum = "CableConstructionKind"

    def add_asset_info(
        self,
        cable: AI.CableInfo,
        *,
        diameterOverCore: float | Qty | None = None,
        diameterOverInsulation: float | Qty | None = None,
        diameterOverScreen: float | Qty | None = None,
        diameterOverJacket: float | Qty | None = None,
        isStrandFill: bool | None = None,
        sheathAsNeutral: bool | None = None,
        nominalTemperature: float | Qty | None = None,
        outerJacketKind: str | None = None,
        shieldMaterial: str | None = None,
        **kwargs,
    ) -> AI.CableInfo:
        """
        Adds the cable construction, plus every WireInfoBuilder.add_asset_info field
        * diameterOverCore: diameter over the core, float in m or Qty('in')
        * diameterOverInsulation: diameter over the insulation, float in m or Qty('in')
        * diameterOverScreen: diameter over the screen, float in m or Qty('in')
        * diameterOverJacket: outside diameter of the cable, float in m or Qty('in')
        * isStrandFill: boolean, strand fill (water blocking) if true
        * sheathAsNeutral: boolean, the sheath is used as the neutral if true
        * nominalTemperature: maximum nominal design operating temperature, float in degC or Qty('degC')
        * outerJacketKind: string, insulating|linearLowDensityPolyethylene|none|other|polyethylene|pvc|semiconducting
        * shieldMaterial: string, aluminum|copper|lead|other|steel
        """
        super().add_asset_info(cable, **kwargs)
        graph_write.set_attr(cable, AI, "diameterOverCore", diameterOverCore)
        graph_write.set_attr(cable, AI, "diameterOverInsulation", diameterOverInsulation)
        graph_write.set_attr(cable, AI, "diameterOverScreen", diameterOverScreen)
        graph_write.set_attr(cable, AI, "diameterOverJacket", diameterOverJacket)
        graph_write.set_attr(cable, AI, "isStrandFill", isStrandFill)
        graph_write.set_attr(cable, AI, "sheathAsNeutral", sheathAsNeutral)
        graph_write.set_attr(cable, AI, "nominalTemperature", nominalTemperature)
        graph_write.set_attr(
            cable, AI, "outerJacketKind", self._enum("CableOuterJacketKind", outerJacketKind)
        )
        graph_write.set_attr(
            cable, AI, "shieldMaterial", self._enum("CableShieldMaterialKind", shieldMaterial)
        )
        return cable
