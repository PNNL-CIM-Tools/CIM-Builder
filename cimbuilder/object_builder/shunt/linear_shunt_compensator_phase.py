import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.object_builder import ObjectBuilder


class LinearShuntCompensatorPhaseBuilder(ObjectBuilder):
    cim_class_name = "LinearShuntCompensatorPhase"

    def add_connectivity(
        self,
        shunt_phs: CN.LinearShuntCompensatorPhase,
        *,
        phase: str,
        ShuntCompensator: str
    ) -> CN.LinearShuntCompensatorPhase:
        """
        Adds the phase and links it to its parent shunt
        * phase: string, single phase kind A|B|C|N|s1|s2
        * ShuntCompensator: mRID of the parent LinearShuntCompensator
        """
        cn: CN = self.cim  # type: ignore

        graph_write.set_attr(shunt_phs, CN, "phase", cn.SinglePhaseKind(phase))
        if ShuntCompensator is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=shunt_phs,
                profile_part=CN,
                association_name="ShuntCompensator",
                target_class=cn.ShuntCompensator,
                target_mRID=ShuntCompensator,
            )
        return shunt_phs


    def add_electrical(
        self,
        shunt_phase: EL_UNBAL.LinearShuntCompensatorPhase,
        *,
        nomQ: float | Qty | None = None,
        bPerSection: float | Qty | None = None,
        gPerSection: float | Qty | None = None,
        normalSections: int | None = 1,
        maximumSections: int | None = 1,
    ) -> EL_UNBAL.LinearShuntCompensatorPhase:
        """Adds the per-phase section values. bPerSection is derived from nomQ and the parent's nomU if not given
        * nomQ: nominal reactive power of this phase, float in VAr or Qty('kVAr'|'MVAr')
        * bPerSection: shunt_phase susceptance, float in siemens or Qty('S'|'pu')
        * gPerSection: shunt_phase conductance, float in siemens or Qty('S'|'pu')
        * normalSections: number of individual caps within bank normally switched in
        * maximumSections: total number of individual caps within the bank
        * 
        """

        graph_write.set_attr(shunt_phase, EL_UNBAL, "nomQ", nomQ)
        graph_write.set_attr(shunt_phase, EL_UNBAL, "normalSections", normalSections)
        graph_write.set_attr(shunt_phase, EL_UNBAL, "maximumSections", maximumSections)

        if bPerSection is None:
            if shunt_phase.nomQ is None or not shunt_phase.maximumSections:
                raise ValueError(
                    f"LinearShuntCompensator {shunt_phase.mRID!r}: bPerSection needs nomU, nomQ "
                    f"and a nonzero maximumSections set"
                )
            # nomQ is the whole bank: B per section = Q / (U² * maximumSections), in siemens
            bPerSection = shunt_phase.nomQ.to("VAr") / (
                shunt_phase.ShuntCompensator.nomU.to("V") ** 2 * shunt_phase.maximumSections #type:ignore
            )  
        graph_write.set_attr(shunt_phase, EL_UNBAL, "bPerSection", bPerSection, system_base=self.network.base_power)
        graph_write.set_attr(shunt_phase, EL_UNBAL, "gPerSection", gPerSection, system_base=self.network.base_power)

        return shunt_phase

    def add_ssh(
        self,
        shunt_phase: SSH.LinearShuntCompensatorPhase,
        *,
        sections: float,
    ) -> SSH.LinearShuntCompensatorPhase:
        """
        Adds real-time values from measurement or basecase.
        * sections: number of sections of this phase switched in
        """
        graph_write.set_attr(shunt_phase, SSH, "sections", sections)
        return shunt_phase
