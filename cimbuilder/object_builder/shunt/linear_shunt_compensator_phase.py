import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import graph_write, impedance
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
        Adds base connectivity layer of terminals, base voltage, phasing
        * node: mRID of the ConnectivityNode or TopologicalNode
        * compensatorType: string, capacitor|reactor
        * phases: phase-code string in conductor order (e.g. CABN). None sets no LinearShuntCompensatorPhase objects
        * grounded: boolean, shunt_phase is grounded if true
        * customerCount: the number of metered customers aggregated into the shunt_phase
        * EquipmentContainer: mRID of the VoltageLevel or Feeder containing the shunt_phase.
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore

        graph_write.set_attr(shunt_phs, CN, "phase", phase)
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
        shunt_phase: EL_BAL.LinearShuntCompensator,
        *,
        nomQ: float | Qty | None = None,
        bPerSection: float | Qty | None = None,
        gPerSection: float | Qty | None = None,
        normalSections: float | None = 1,
        maximumSections: float | None = 1,
    ) -> EL_BAL.LinearShuntCompensator:
        """Adds electrical_balanced.LinearShuntCompensator's fixed-shunt_phase parameters.
        * nomU: nominal voltage used to calculate susceptance, within 10% of BaseVoltage.nominalVoltage
        * nomQ: nominal reactive power, float in VAr or Qty('kVA'|'MVA')
        * bPerSection: shunt_phase susceptance, float in siemens or Qty('S'|'pu')
        * gPerSection: shunt_phase conductance, float in siemens or Qty('S'|'pu')
        * normalSections: number of individual caps within bank normally switched in
        * maximumSections: total number of individual caps within the bank
        * 
        """


        graph_write.set_attr(shunt_phase, EL_BAL, "nomQ", nomQ)
        graph_write.set_attr(shunt_phase, EL_BAL, "normalSections", normalSections)
        graph_write.set_attr(shunt_phase, EL_BAL, "maximumSections", maximumSections)

        z_base = impedance.z_base(shunt_phase, [], self.network.base_power)

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
        graph_write.set_attr(shunt_phase, EL_BAL, "bPerSection", bPerSection, z_base=z_base)
        graph_write.set_attr(shunt_phase, EL_BAL, "gPerSection", gPerSection, z_base=z_base)

        return shunt_phase

    def add_ssh(
        self,
        shunt_phase: SSH.LinearShuntCompensator,
        *,
        sections: float,
        inService: bool | None = None,
    ) -> SSH.LinearShuntCompensator:
        """
        Adds real-time values from measurement or basecase.
        * sections: total number of cap bank sections switched in
        * inService: boolean, shunt_phase is de-energized if false
        """
        graph_write.set_attr(shunt_phase, SSH, "sections", sections)
        graph_write.set_attr(shunt_phase, SSH, "inService", inService)
        return shunt_phase

    