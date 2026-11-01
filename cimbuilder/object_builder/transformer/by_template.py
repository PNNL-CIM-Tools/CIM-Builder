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
from cimtables import graph_write, impedance
from cimtables.units import Qty


class TransformerTankConfigurationBuilder(ObjectBuilder):
    cim_class_name = 'TransformerTankConfiguration'

    def add_nameplate(self, config, *, percentImpedance=None, percentMagnetizingCurrent=None,
                    noLoadLoss=None, loadLoss=None) -> None:
        """construction.TransformerTankConfiguration's own scalars.
        * percentImpedance: a Qty resolved to PerCent (dimensionless, SI
          base) - e.g. Qty(2.5, 'percent'). Note: despite the name, this
          field is itself a plain PerCent value, NOT the kind of
          pu/percent-on-an-ohm-field Qty that set_attr special-cases for
          z_base conversion (that only applies to ohm-typed attrs like r/x);
          percentImpedance is simply stored as-is in PerCent.
        * percentMagnetizingCurrent: a Qty resolved to PerCent.
        * noLoadLoss/loadLoss: Qtys resolved to ActivePower (W, SI base).
        A bare number for any of these is read as SI base (wrapped in its CIMUnit).
        """
        graph_write.set_attr(config, CONST, 'percentImpedance', percentImpedance)
        graph_write.set_attr(config, CONST, 'percentMagnetizingCurrent', percentMagnetizingCurrent)
        graph_write.set_attr(config, CONST, 'noLoadLoss', noLoadLoss)
        graph_write.set_attr(config, CONST, 'loadLoss', loadLoss)

    def add_phase_end(self, config, *, mRID: str, endNumber: int, sequenceNumber: int,
                       phase: str, phaseNeutralU=None) -> object:
        """
        Builds+returns a TransformerPhaseEnd on `config` (the
        TransformerTankConfiguration template), one of shape 3's per-phase
        end definitions.
        * mRID: plain string, used verbatim as the new TransformerPhaseEnd's
          identity key.
        * endNumber: plain int, no unit wrapping - matches the
          PowerTransformerEnd side (1=high, 2=low, 3=tertiary by convention,
          not enforced here).
        * sequenceNumber: plain int, no unit wrapping - this end's row/column
          index into a matched PhaseImpedanceData matrix (same convention
          per_length_impedance.py's add_phase_impedance_data documents).
        * phase: string value of connectivity_unbalanced.SinglePhaseKind
          (e.g. 'A', 's1') - converted via `self.cim.SinglePhaseKind(...)`
          before set_attr.
        * phaseNeutralU: a Qty resolved to Voltage (V, SI base) - phase-to-
          neutral voltage for this end. A bare number is read as SI base (wrapped in its CIMUnit).

        Returns the built, graph-added TransformerPhaseEnd.
        """
        end = self.cim.TransformerPhaseEnd(mRID=mRID)
        graph_write.set_attr(end, CN, 'endNumber', endNumber)
        graph_write.set_attr(end, CN, 'sequenceNumber', sequenceNumber)
        graph_write.set_attr(end, CN, 'phase', self.cim.SinglePhaseKind(phase))
        graph_write.set_attr(end, CN, 'phaseNeutralU', phaseNeutralU)
        graph_write.set_assc(end, CONST, 'TankConfiguration', config)
        graph_write.add_to_graph(self.network, end)
        return end

    def add_winding(self, config, *, mRID: str, ratedS=None, ratedU=None, baseS=None, baseU=None,
                     r=None, FromTransformerEnd: str | None = None, ToTransformerEnd: str | None = None) -> object:
        """
        Builds+returns a TransformerWinding on `config` (shape 3's
        mesh-by-winding layer).
        * mRID: plain string, used verbatim as the new TransformerWinding's
          identity key.
        * ratedS: a Qty resolved to ApparentPower (VA, SI base) - normal
          apparent power rating of the winding.
        * ratedU: a Qty resolved to Voltage (V, SI base) - phase-to-phase
          (12470/240) voltage at no load.
        * baseS: a Qty resolved to ApparentPower (VA, SI base) - used for
          calculation of percent impedance; for a split-phase center-tap
          transformer, the rating of the primary winding is used as the
          basis for both secondary windings. Also consumed by
          cimtables.impedance.z_base (via `r`'s z_base,
          below) and by add_mesh_impedance's `x` z_base - so set this
          BEFORE passing a relative (pu/percent) `r` or calling
          add_mesh_impedance with a relative `x`, or the z_base resolves to
          None.
        * baseU: a Qty resolved to Voltage (V, SI base) - phase-to-neutral
          voltage for wye, phase-to-phase voltage for delta. Same
          before-r/before-add_mesh_impedance ordering requirement as baseS.
        * FromTransformerEnd/ToTransformerEnd: mRID strings of existing
          TransformerPhaseEnds (built via add_phase_end). Resolved via
          set_assc_from_mrid, which raises ValueError if not already in the
          graph; omitted entirely (no association write) when None.
        * r: a Qty resolved to Resistance (ohm, SI base) if absolute, or
          converted to ohms against a z_base computed from this winding's
          OWN baseU/baseS (via cimtables.impedance.z_base)
          if relative (pu/percent) - e.g. Qty(2, 'percent'). Raises ValueError
          if relative and baseU/baseS aren't both already set on `winding`
          (z_base resolves to None, which set_attr then rejects). A bare
          number is read as SI base (wrapped in its CIMUnit).

        Returns the built, graph-added TransformerWinding.
        """
        winding = self.cim.TransformerWinding(mRID=mRID)
        graph_write.set_assc(winding, CONST, 'TankConfiguration', config)
        if FromTransformerEnd is not None:
            graph_write.set_assc_from_mrid(
                self.network, winding, CONST, 'FromTransformerEnd', self.cim.TransformerPhaseEnd, FromTransformerEnd)
        if ToTransformerEnd is not None:
            graph_write.set_assc_from_mrid(
                self.network, winding, CONST, 'ToTransformerEnd', self.cim.TransformerPhaseEnd, ToTransformerEnd)

        graph_write.set_attr(winding, EL_BAL, 'baseS', baseS)
        graph_write.set_attr(winding, EL_BAL, 'baseU', baseU)
        graph_write.set_attr(winding, EL_BAL, 'ratedS', ratedS)
        graph_write.set_attr(winding, EL_BAL, 'ratedU', ratedU)
        if isinstance(r, Qty) and r.is_relative():
            graph_write.set_attr(winding, EL_BAL, 'r', r, z_base=impedance.z_base(winding, [], self.network.base_power))
        else:
            graph_write.set_attr(winding, EL_BAL, 'r', r)
        graph_write.add_to_graph(self.network, winding)
        return winding

    def add_mesh_impedance(self, *, FromWinding: str, ToWinding: str, x) -> object:
        """Shape 3's mesh layer: builds+returns a TransformerMeshImpedance
        between two named TransformerWindings. No `config`/`TankConfiguration`
        parameter - TransformerMeshImpedance has no FK to the template
        container itself (confirmed: electrical_balanced.TransformerMeshImpedance
        only has FromWinding/ToWinding/FromTransformerEnd/ToTransformerEnd/r/x),
        only to the two windings, which already carry their own
        TankConfiguration FK.
        * FromWinding/ToWinding: mRID strings of existing TransformerWindings
          (built via add_winding). Resolved via graph_write.resolve (not
          set_assc_from_mrid); if either is not found, this raises
          ValueError itself rather than delegating to resolve/set_assc's own
          error.
        * x: a Qty resolved to Reactance (ohm, SI base) if absolute, or
          converted to ohms against a z_base computed from FromWinding's OWN
          baseU/baseS (via cimtables.impedance.z_base) if
          relative (pu/percent) - same rule as add_winding's `r`. Raises
          ValueError if relative and FromWinding's baseU/baseS aren't both
          already set. A bare number is read as SI base (wrapped in its CIMUnit).

        Returns the built, graph-added TransformerMeshImpedance.
        """
        from_winding = graph_write.resolve(self.network, self.cim.TransformerWinding, FromWinding)
        to_winding = graph_write.resolve(self.network, self.cim.TransformerWinding, ToWinding)
        if from_winding is None or to_winding is None:
            raise ValueError(
                f"mesh impedance references {FromWinding!r}/{ToWinding!r}, not both found in graph"
            )
        mesh = self.cim.TransformerMeshImpedance(mRID=f'{FromWinding}_{ToWinding}_mesh')
        graph_write.set_assc(mesh, EL_BAL, 'FromWinding', from_winding)
        graph_write.set_assc(mesh, EL_BAL, 'ToWinding', to_winding)
        if isinstance(x, Qty) and x.is_relative():
            graph_write.set_attr(mesh, EL_BAL, 'x', x, z_base=impedance.z_base(mesh, [from_winding], self.network.base_power))
        else:
            graph_write.set_attr(mesh, EL_BAL, 'x', x)
        graph_write.add_to_graph(self.network, mesh)
        return mesh
