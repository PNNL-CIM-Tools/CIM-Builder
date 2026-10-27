"""PowerTransformerBuilder: the instance tier (design: Phase 1 of
cimbuilder/development/OBJECT_BUILDER_MIGRATION.md, resolved against real
.cimtbl reference models and Visio modeling reference diagrams - see the
approved implementation plan for the full field-location evidence).

Three coexisting CIM impedance representations exist for a PowerTransformer,
confirmed against cimprofiles.cim18.cim18v17.electrical_balanced (NOT
electrical_unbalanced, which has no scalar impedance fields on
PowerTransformerEnd at all):

1. PI-direct-on-end (2-winding, and 3-winding star-equivalent) - add_electrical
   writes r/x/b/g straight onto a single PowerTransformerEnd. Needed for
   PSS/E import. Any star<->mesh conversion (e.g. a 3-winding star-equivalent's
   mirrored end values) is the caller's job - this builder only ever writes
   already-computed values, never derives them.
2. Mesh-by-end - add_mesh_impedance builds a TransformerMeshImpedance directly
   between two named PowerTransformerEnds, no TransformerWinding layer.
3. Mesh-by-winding (template) - the TransformerTankConfigurationBuilder
   (by_template.py) builds this tier; PowerTransformerBuilder only
   references a template by name via add_tank.

Field locations confirmed directly against the installed cimprofiles package
(do not assume - every part module below was grepped, not guessed):
- endNumber, connectionKind, Terminal, BaseVoltage, grounded, and the
  RatioTapChanger FK all live on connectivity_unbalanced.TransformerEnd/
  PowerTransformerEnd - connectivity.add_connectivity resolves its own part
  module off network.cim, so this file still needs CN directly for the
  fields add_connectivity's TransformerEnd branch doesn't set (connectionKind,
  endNumber itself) and for add_tap_changer's FK write.
- r/x/b/g/ratedS/ratedU (the impedance values) and TransformerMeshImpedance's
  FromTransformerEnd/ToTransformerEnd/r/x live on electrical_balanced - NOT
  electrical_unbalanced, which has no scalar impedance fields on
  PowerTransformerEnd at all.
- TransformerTank's PowerTransformer/TankConfiguration FKs live on
  construction.TransformerTank - electrical_unbalanced.TransformerTank is a
  different shape (ratings only, no FKs at all) and must not be used here.
- RatioTapChanger's own ratings (highStep/lowStep/initialDelay) live on
  regulating_control.TapChanger (RatioTapChanger's base class) - not on
  connectivity_unbalanced's RatioTapChanger, which only has the TransformerEnd
  FK.
"""

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.construction as CONST
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.regulating_control as REG

from cimbuilder.builders.base import ObjectBuilder
from cimtables import connectivity, graph_write


class PowerTransformerBuilder(ObjectBuilder):
    cim_class_name = 'PowerTransformer'

    def add_connectivity(self, xfmr, *, ends: list[dict], container: object = None) -> list[object]:
        """ends = [{'node': 'busA', 'endNumber': 1, 'connectionKind': 'Y'}, ...],
        one dict per winding end. Builds one PowerTransformerEnd + Terminal per
        entry: the end's PowerTransformer/endNumber are set first (required by
        connectivity.add_connectivity's TransformerEnd branch), then the node
        wiring is delegated to that same generic function - no terminal/node
        logic is reimplemented here. Returns the created PowerTransformerEnds,
        in the given order, for a caller to pass into add_electrical/
        add_mesh_impedance/add_tap_changer."""
        resolved_container = container if container is not None else self.container
        if resolved_container is None:
            resolved_container = self.network.container
        if isinstance(resolved_container, self.cim.EquipmentContainer):
            graph_write.set_assc(xfmr, CN, 'EquipmentContainer', resolved_container)

        created_ends = []
        for entry in ends:
            end = self.cim.PowerTransformerEnd(name=f"{xfmr.name}_end{entry['endNumber']}")
            graph_write.set_assc(end, CN, 'PowerTransformer', xfmr)
            graph_write.set_attr(end, CN, 'endNumber', entry['endNumber'])
            connection_kind = entry.get('connectionKind')
            if connection_kind is not None:
                graph_write.set_attr(end, CN, 'connectionKind', self.cim.WindingConnection(connection_kind))
            graph_write.add_to_graph(self.network, end)
            connectivity.add_connectivity(self.network, end, node_cols={'node': entry['node']})
            created_ends.append(end)
        return created_ends

    def add_electrical(self, end, *, r=None, x=None, b=None, g=None,
                        ratedS=None, ratedU=None) -> None:
        """Shape 1 (PI-direct-on-end): writes directly onto a single
        PowerTransformerEnd - `end` is one of add_connectivity's returned
        ends, not the transformer itself. r/x/b/g are whatever
        already-computed values the caller has; this method performs no
        star<->mesh conversion (that stays in cimhub_core.transformations,
        or a future standalone conversion utility - never here)."""
        graph_write.set_attr(end, EL_BAL, 'r', r)
        graph_write.set_attr(end, EL_BAL, 'x', x)
        graph_write.set_attr(end, EL_BAL, 'b', b)
        graph_write.set_attr(end, EL_BAL, 'g', g)
        graph_write.set_attr(end, EL_BAL, 'ratedS', ratedS)
        graph_write.set_attr(end, EL_BAL, 'ratedU', ratedU)

    def add_mesh_impedance(self, xfmr, *, FromTransformerEnd: str, ToTransformerEnd: str,
                            r=None, x=None) -> object:
        """Shape 2 (mesh-by-end): builds+returns a TransformerMeshImpedance
        directly between two named PowerTransformerEnds (resolved by name),
        no TransformerWinding layer."""
        from_end = graph_write.resolve(self.network, self.cim.PowerTransformerEnd, FromTransformerEnd)
        to_end = graph_write.resolve(self.network, self.cim.PowerTransformerEnd, ToTransformerEnd)
        if from_end is None or to_end is None:
            raise ValueError(
                f"{xfmr.name!r}: mesh impedance references "
                f"{FromTransformerEnd!r}/{ToTransformerEnd!r}, not both found in graph"
            )
        mesh = self.cim.TransformerMeshImpedance(name=f'{xfmr.name}_mesh_{FromTransformerEnd}_{ToTransformerEnd}')
        graph_write.set_assc(mesh, EL_BAL, 'FromTransformerEnd', from_end)
        graph_write.set_assc(mesh, EL_BAL, 'ToTransformerEnd', to_end)
        graph_write.set_attr(mesh, EL_BAL, 'r', r)
        graph_write.set_attr(mesh, EL_BAL, 'x', x)
        graph_write.add_to_graph(self.network, mesh)
        return mesh

    def add_tank(self, xfmr, *, name: str, TankConfiguration: str) -> object:
        """Builds+returns a TransformerTank(name=name, PowerTransformer=xfmr),
        referencing a TransformerTankConfiguration template by name - build
        the template first (via TransformerTankConfigurationBuilder) or this
        raises, same ordering rule CIMTBL_DESIGN.md §12.3 documents for
        EquipmentContainer/FK resolution generally."""
        config = graph_write.resolve(self.network, self.cim.TransformerTankConfiguration, TankConfiguration)
        if config is None:
            raise ValueError(
                f"{xfmr.name!r}: TankConfiguration {TankConfiguration!r} not found in graph "
                f"(build the template before the instance that references it)"
            )
        tank = self.cim.TransformerTank(name=name)
        graph_write.set_assc(tank, CONST, 'PowerTransformer', xfmr)
        graph_write.set_assc(tank, CONST, 'TankConfiguration', config)
        graph_write.add_to_graph(self.network, tank)
        return tank

    def add_tap_changer(self, end, *, highStep: float = 0, lowStep: float = 0,
                         initialDelay: float = 0) -> object:
        """Ports object_builder/transformer/new_tap_changer.py: builds+returns
        a RatioTapChanger on `end` (a PowerTransformerEnd, not the
        transformer - a tap changer is per-end). The tap changer's own
        ratings (highStep/lowStep/initialDelay) are regulating_control
        fields; the FK back onto `end` is a connectivity_unbalanced field -
        two different part modules for the same object, confirmed by reading
        both classes directly rather than assuming one part module covers
        the whole class."""
        tap_changer = self.cim.RatioTapChanger(name=f'{end.name}_tap')
        graph_write.set_attr(tap_changer, REG, 'highStep', highStep)
        graph_write.set_attr(tap_changer, REG, 'lowStep', lowStep)
        graph_write.set_attr(tap_changer, REG, 'initialDelay', initialDelay)
        graph_write.set_assc(end, CN, 'RatioTapChanger', tap_changer)
        graph_write.add_to_graph(self.network, tap_changer)
        return tap_changer
