import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.regulating_control as RC
import cimprofiles.cim18.cim18v17.short_circuit as SC
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import connectivity, graph_write
from cimtables.units import Qty

from cimbuilder.core.sort_terminals import sort_terminals_by_sequence
from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class LinearShuntCompensatorBuilder(ObjectBuilder):
    """
    Builder for capacitor and reactor banks. Builder functions to be called in the following order:
    * create() - instantiate the LinearShuntCompensator
    * add_connectivity() - Terminal, phases, connection and BaseVoltage
    * add_electrical() - nominal ratings and susceptance per section
    * add_short_circuit() - zero sequence susceptance per section
    * add_regulating_control() - optional, the RegulatingControl that switches the bank
    * add_ssh() - sections switched in
    """

    cim_class_name = "LinearShuntCompensator"

    def add_connectivity(
        self,
        shunt: CN.LinearShuntCompensator,
        *,
        node: mRID,
        compensatorType: str,
        phaseConnection: str | None = None,
        phases: str | None = None,
        grounded: bool | None = None,
        EquipmentContainer: mRID | None = None,
        BaseVoltage: mRID,
    ) -> tuple[
        CN.LinearShuntCompensator, CN.Terminal, list[CN.LinearShuntCompensatorPhase]
    ]:
        """
        Adds base connectivity layer of terminals, base voltage, phasing
        * node: mRID of the ConnectivityNode or TopologicalNode
        * compensatorType: string, capacitor|reactor
        * phaseConnection: string for whether wye or delta connected, D|Y|Yn|I
        * phases: phase-code string in conductor order (e.g. CABN). None sets no LinearShuntCompensatorPhase objects
        * grounded: boolean, shunt is grounded if true
        * customerCount: the number of metered customers aggregated into the shunt
        * EquipmentContainer: mRID of the VoltageLevel or Feeder containing the shunt.
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore

        graph_write.set_attr(
            shunt, CN, "compensatorType", cn.CompensatorKind(compensatorType)
        )
        graph_write.set_attr(shunt, CN, "grounded", grounded)
        if phaseConnection is not None:
            graph_write.set_attr(
                shunt, CN, "phaseConnection", cn.PhaseShuntConnectionKind(phaseConnection)
            )

        if EquipmentContainer is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=shunt,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=EquipmentContainer,
            )
        else:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=shunt,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=self.container.mRID,
            )
        if len(shunt.Terminals) != 1:
            terminals = connectivity.add_connectivity(
                network=self.network,
                equipment=shunt,
                node_cols={"node": node},
                equipment_container=shunt.EquipmentContainer,
            )
        else:
            terminals = sort_terminals_by_sequence(shunt)

        if phases is not None:
            shunt_phs: list[CN.LinearShuntCompensatorPhase] = (
                connectivity.add_phase_children(
                    self.network, shunt, terminals, phases=phases
                )
            )  # type:ignore
        else:
            shunt_phs = []

        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=shunt,
                profile_part=CN,
                association_name="BaseVoltage",
                target_class=cn.BaseVoltage,
                target_mRID=BaseVoltage,
            )
        return shunt, terminals[0], shunt_phs

    def add_electrical(
        self,
        shunt: EL_BAL.LinearShuntCompensator,
        *,
        nomU: float | Qty,
        nomQ: float | Qty | None = None,
        bPerSection: float | Qty | None = None,
        gPerSection: float | Qty | None = None,
        normalSections: int | None = 1,
        maximumSections: int | None = 1,
    ) -> EL_BAL.LinearShuntCompensator:
        """Adds electrical_balanced.LinearShuntCompensator's fixed-shunt parameters.
        * nomU: nominal voltage used to calculate susceptance, within 10% of BaseVoltage.nominalVoltage
        * nomQ: nominal reactive power, float in VAr or Qty('kVA'|'MVA')
        * bPerSection: shunt susceptance, float in siemens or Qty('S'|'pu')
        * gPerSection: shunt conductance, float in siemens or Qty('S'|'pu')
        * normalSections: number of individual caps within bank normally switched in
        * maximumSections: total number of individual caps within the bank
        *
        """

        graph_write.set_attr(shunt, EL_BAL, "nomU", nomU)
        graph_write.set_attr(shunt, EL_BAL, "nomQ", nomQ)
        graph_write.set_attr(shunt, EL_BAL, "normalSections", normalSections)
        graph_write.set_attr(shunt, EL_BAL, "maximumSections", maximumSections)

        if bPerSection is None:
            if shunt.nomQ is None or not shunt.maximumSections:
                raise ValueError(
                    f"LinearShuntCompensator {shunt.mRID!r}: bPerSection needs nomU, nomQ "
                    f"and a nonzero maximumSections set"
                )
            # nomQ is the whole bank: B per section = Q / (U² * maximumSections), in siemens
            bPerSection = shunt.nomQ.to("VAr") / (
                shunt.nomU.to("V") ** 2 * shunt.maximumSections  # pyright: ignore[reportOptionalMemberAccess]
            )
        graph_write.set_attr(shunt, EL_BAL, "bPerSection", bPerSection, system_base=self.network.base_power)
        graph_write.set_attr(shunt, EL_BAL, "gPerSection", gPerSection, system_base=self.network.base_power)

        return shunt

    def add_short_circuit(
            self,
            shunt: SC.LinearShuntCompensator,
            *,
            b0PerSection: float | Qty | None = None,
            g0PerSection: float | Qty | None = None,
        ) -> SC.LinearShuntCompensator:
            """Adds electrical_balanced.LinearShuntCompensator's fixed-shunt parameters.
            * bPerSection: zero sequence shunt susceptance, float in siemens or Qty('S'|'pu')
            * gPerSection: zero sequence shunt conductance, float in siemens or Qty('S'|'pu')
            """
            graph_write.set_attr(shunt, SC, "b0PerSection", b0PerSection, system_base=self.network.base_power)
            graph_write.set_attr(shunt, SC, "g0PerSection", g0PerSection, system_base=self.network.base_power)
    
            return shunt

    def add_ssh(
        self,
        shunt: SSH.LinearShuntCompensator,
        *,
        sections: float,
        inService: bool | None = None,
    ) -> SSH.LinearShuntCompensator:
        """
        Adds real-time values from measurement or basecase.
        * sections: total number of cap bank sections switched in
        * inService: boolean, shunt is de-energized if false
        """
        graph_write.set_attr(shunt, SSH, "sections", sections)
        graph_write.set_attr(shunt, SSH, "inService", inService)
        return shunt

    def add_regulating_control(
        self,
        shunt: RC.LinearShuntCompensator,
        *,
        RegulatingControl: mRID | None = None,
        controlEnabled: bool | None = None,
        aVRDelay: float | Qty | None = None,
    ) -> RC.LinearShuntCompensator:
        """
        Attaches the shunt to the RegulatingControl that switches it. Build the control first with RegulatingControlBuilder
        * RegulatingControl: mRID of the RegulatingControl, None for a fixed shunt
        * controlEnabled: boolean, the control may switch the shunt if true
        * aVRDelay: time delay before switching, float in s or Qty('s')
        """
        rc: RC = self.cim  # type: ignore
        graph_write.set_attr(shunt, RC, "controlEnabled", controlEnabled)
        graph_write.set_attr(shunt, RC, "aVRDelay", aVRDelay)
        if RegulatingControl is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=shunt,
                profile_part=RC,
                association_name="RegulatingControl",
                target_class=rc.RegulatingControl,
                target_mRID=RegulatingControl,
            )
        return shunt
