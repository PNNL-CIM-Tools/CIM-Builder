"""TransformerTankConfigurationBuilder: the reusable template tier (design:
Phase 1 of cimbuilder/development/OBJECT_BUILDER_MIGRATION.md; see the
approved implementation plan for the full field-location evidence).

Builds the template xfmrcodes.cimtbl shows: TransformerTankConfiguration
(the ratings container) + TransformerPhaseEnd (per-phase end definitions) +
TransformerWinding (the winding layer, shape 3's mesh-by-winding
representation) + TransformerMeshImpedance between two named windings.
PowerTransformerBuilder.add_tank references a built config by name - it
never builds one itself.

Field locations confirmed directly against the installed cimprofiles
package (do not assume):
- percentImpedance/percentMagnetizingCurrent/noLoadLoss/loadLoss, and the
  TankConfiguration FK on both TransformerPhaseEnd and TransformerWinding,
  live on construction - the only part module TransformerTankConfiguration
  itself exists in at all.
- endNumber/sequenceNumber/phase/phaseNeutralU (TransformerPhaseEnd's own
  identity fields) live on connectivity_unbalanced, inherited from the
  shared TransformerEnd/TransformerPhaseEnd base every part module's version
  subclasses - NOT duplicated onto construction's TransformerPhaseEnd, which
  only adds the TankConfiguration FK.
- TransformerWinding's rating/impedance scalars (baseS/baseU/r/ratedS/
  ratedU/rDC) live on electrical_balanced; its connectivity/membership FKs
  (FromTransformerEnd/ToTransformerEnd/TankConfiguration/connection) live on
  construction instead - two different part modules for the same class,
  confirmed by reading both directly.
- TransformerMeshImpedance's FromWinding/ToWinding/r/x live on
  electrical_balanced (the same class also carries FromTransformerEnd/
  ToTransformerEnd there, used by PowerTransformerBuilder.add_mesh_impedance
  for shape 2 instead).
"""

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.construction as CONST
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL

from cimbuilder.builders.base import ObjectBuilder
from cimtables import graph_write


class TransformerTankConfigurationBuilder(ObjectBuilder):
    cim_class_name = 'TransformerTankConfiguration'

    def add_rating(self, config, *, percentImpedance=None, percentMagnetizingCurrent=None,
                    noLoadLoss=None, loadLoss=None) -> None:
        """construction.TransformerTankConfiguration's own scalars."""
        graph_write.set_attr(config, CONST, 'percentImpedance', percentImpedance)
        graph_write.set_attr(config, CONST, 'percentMagnetizingCurrent', percentMagnetizingCurrent)
        graph_write.set_attr(config, CONST, 'noLoadLoss', noLoadLoss)
        graph_write.set_attr(config, CONST, 'loadLoss', loadLoss)

    def add_phase_end(self, config, *, name: str, endNumber: int, sequenceNumber: int,
                       phase: str, phaseNeutralU=None) -> object:
        """Builds+returns a TransformerPhaseEnd, FK'd to `config`. endNumber/
        sequenceNumber/phase/phaseNeutralU are connectivity_unbalanced fields
        (the shared TransformerEnd/TransformerPhaseEnd identity, not a
        template-specific concept); the TankConfiguration FK itself is
        construction's own field."""
        end = self.cim.TransformerPhaseEnd(name=name)
        graph_write.set_attr(end, CN, 'endNumber', endNumber)
        graph_write.set_attr(end, CN, 'sequenceNumber', sequenceNumber)
        graph_write.set_attr(end, CN, 'phase', self.cim.SinglePhaseKind(phase))
        graph_write.set_attr(end, CN, 'phaseNeutralU', phaseNeutralU)
        graph_write.set_assc(end, CONST, 'TankConfiguration', config)
        graph_write.add_to_graph(self.network, end)
        return end

    def add_winding(self, config, *, name: str, ratedS=None, ratedU=None, baseS=None, baseU=None,
                     r=None, FromTransformerEnd: str | None = None, ToTransformerEnd: str | None = None) -> object:
        """Shape 3's winding layer: builds+returns a TransformerWinding.
        ratedS/ratedU/baseS/baseU/r (a relative Qty, percent) are
        electrical_balanced scalars, with z_base resolved from THIS
        winding's own baseU/baseS - the same rule cimtables/binder.py's
        _winding_z_base already applies for .cimtbl loading, invoked
        directly here for the manual API. FromTransformerEnd/
        ToTransformerEnd/TankConfiguration are construction FKs, resolved by
        name against the TransformerPhaseEnds built by add_phase_end."""
        winding = self.cim.TransformerWinding(name=name)
        graph_write.set_assc(winding, CONST, 'TankConfiguration', config)
        if FromTransformerEnd is not None:
            from_end = graph_write.resolve(self.network, self.cim.TransformerPhaseEnd, FromTransformerEnd)
            if from_end is None:
                raise ValueError(f"{name!r}: FromTransformerEnd {FromTransformerEnd!r} not found in graph")
            graph_write.set_assc(winding, CONST, 'FromTransformerEnd', from_end)
        if ToTransformerEnd is not None:
            to_end = graph_write.resolve(self.network, self.cim.TransformerPhaseEnd, ToTransformerEnd)
            if to_end is None:
                raise ValueError(f"{name!r}: ToTransformerEnd {ToTransformerEnd!r} not found in graph")
            graph_write.set_assc(winding, CONST, 'ToTransformerEnd', to_end)

        graph_write.set_attr(winding, EL_BAL, 'baseS', baseS)
        graph_write.set_attr(winding, EL_BAL, 'baseU', baseU)
        graph_write.set_attr(winding, EL_BAL, 'ratedS', ratedS)
        graph_write.set_attr(winding, EL_BAL, 'ratedU', ratedU)
        if r is not None:
            z_base = _winding_z_base(winding)
            graph_write.set_attr(winding, EL_BAL, 'r', r, z_base=z_base)
        graph_write.add_to_graph(self.network, winding)
        return winding

    def add_mesh_impedance(self, *, FromWinding: str, ToWinding: str, x) -> object:
        """Shape 3's mesh layer: builds+returns a TransformerMeshImpedance
        between two named TransformerWindings. No `config`/`TankConfiguration`
        parameter - TransformerMeshImpedance has no FK to the template
        container itself (confirmed: electrical_balanced.TransformerMeshImpedance
        only has FromWinding/ToWinding/FromTransformerEnd/ToTransformerEnd/r/x),
        only to the two windings, which already carry their own
        TankConfiguration FK. `x` (a relative Qty, percent) is resolved
        against FromWinding's own baseU/baseS, same rule as add_winding's
        `r`."""
        from_winding = graph_write.resolve(self.network, self.cim.TransformerWinding, FromWinding)
        to_winding = graph_write.resolve(self.network, self.cim.TransformerWinding, ToWinding)
        if from_winding is None or to_winding is None:
            raise ValueError(
                f"mesh impedance references {FromWinding!r}/{ToWinding!r}, not both found in graph"
            )
        mesh = self.cim.TransformerMeshImpedance(name=f'{FromWinding}_{ToWinding}_mesh')
        graph_write.set_assc(mesh, EL_BAL, 'FromWinding', from_winding)
        graph_write.set_assc(mesh, EL_BAL, 'ToWinding', to_winding)
        if x is not None:
            graph_write.set_attr(mesh, EL_BAL, 'x', x, z_base=_winding_z_base(from_winding))
        graph_write.add_to_graph(self.network, mesh)
        return mesh


def _winding_z_base(winding: object) -> float | None:
    """z_base in ohms (U**2 / S) from a winding's own baseU/baseS - mirrors
    cimtables/binder.py's _winding_z_base for the single-winding case this
    builder always has (no From*-reference fallback needed here, since the
    winding being written is always the one carrying the relative value).
    Uses getattr, not direct attribute access, since TransformerWinding is a
    runtime-only class resolved off network.cim, not a static import - same
    convention binder.py's own _rating helper uses."""
    base_u = getattr(winding, 'baseU', None)
    base_s = getattr(winding, 'baseS', None)
    if base_u is None or base_s is None:
        return None
    u = base_u.to('V')
    s = base_s.to('VA')
    return (u ** 2 / s) if u and s else None
