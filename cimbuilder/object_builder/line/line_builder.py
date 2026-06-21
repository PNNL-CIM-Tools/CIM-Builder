
from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel
from cimgraph.databases import get_cim_profile

from cimbuilder.object_builder.object_builder import ObjectBuilder

import logging
_log = logging.getLogger(__name__)

if TYPE_CHECKING:
    import cimgraph.data_profile.cim18gmdm.connectivity as CN
    import cimgraph.data_profile.cim18gmdm.electrical as EQ
    import cimgraph.data_profile.cim18gmdm.asset as AST
    # import cimgraph.data_profile.cim18gmdm.dynamics as DN
    # import cimgraph.data_profile.cim18gmdm.short_circuit as SC


@dataclass
class LineBuilder(ObjectBuilder):
    network: GraphModel
    container: "CN.EquipmentContainer"

    def add_connectivity(self,
        name: str,
        node1: "str | CN.ConnectivityNode",
        node2: "str | CN.ConnectivityNode"):
        
        cim: CN = get_cim_profile()
        
        line = cim.ACLineSegment(name=name)
        line.EquipmentContainer = self.container
        self.network.add_to_graph(line)
        
        return line
        
        
    def add_electrical(self,
        r: float,
        x: float,
        bch: float,
        r_unit: str|None,
        x_unit: str|None,
        bch_unit: str|None
    ):
        
        cim: EQ = get_cim_profile()
        
        if r_unit.lower() in ['pu', 'perunit', 'per_unit']:
            convert_to_ohm(r_unit)
        
        line.r = cim.Resistance(r, r_unit or 'ohm')
        line.x = cim.Resistance(x, x_unit or 'ohm')
        
        
        
    def add_short_circuit(self,
        r0,
        x0,
        b0ch,
    ):
        cim: SC = get_cim_profile()
        
        if r_unit.lower() in ['pu', 'perunit', 'per_unit']:
            convert_to_ohm(r_unit)
        
        line.r0 = cim.Resistance(r, r_unit or 'ohm')
        
        line.x0 = cim.Resistance(x, x_unit or 'ohm')

