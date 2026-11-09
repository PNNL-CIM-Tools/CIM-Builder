from abc import ABC

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.construction as CONSTR
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.short_circuit as SC
from cimtables import connectivity, graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.transformer.power_transformer import (
    PowerTransformerBuilder,
)

mRID = str


class TransformerBankBaseBuilder(PowerTransformerBuilder, ABC):
    """
    Shared base for transformer banks, use TransformerBankBuilder (tanks described by lug/core/
    winding/mesh) or TransformerBankFromConfigurationBuilder (tanks from a TransformerTankConfiguration
    template). Builder functions to be called in the following order:
    * create() - instantiate the PowerTransformer
    * add_connectivity() - set the EquipmentContainer
    * add_power_transformer_end() - create each end with its Terminal and phases, no ratings
    * add_transformer_tank() - one per physical tank, shape depends on the subclass
    * add_transformer_phase_end() - one phase end for every conductor the tank lugs land on
    """

    cim_class_name = "PowerTransformer"

    def add_power_transformer_end(
        self,
        xfmr: CN.PowerTransformer,
        *,
        node: mRID,
        endNumber: int,
        phases: str,
        connectionKind: str | None = None,
        grounded: bool | None = None,
        BaseVoltage: mRID,
    ) -> tuple[CN.PowerTransformer, CN.Terminal, CN.PowerTransformerEnd]:
        """
        Adds an end and its Terminal, carrying the phases of the conductors it lands on
        * node: mRID of the ConnectivityNode or TopologicalNode for this end
        * endNumber: highest voltage winding is end #1
        * phases: phase-code string in conductor order (e.g. ABCN, s1s2N)
        * connectionKind: wye/delta connection, Y|Yn|oY|D|Dn|oD|Z|I|A|T
        * grounded: boolean, the neutral of this end is grounded if true
        * BaseVoltage: mRID string of the BaseVoltage
        """
        xfmr, terminal, xfmr_end = super().add_power_transformer_end(
            xfmr,
            node=node,
            endNumber=endNumber,
            connectionKind=connectionKind,
            grounded=grounded,
            BaseVoltage=BaseVoltage,
        )
        # an end's phases live on its Terminal only, no phase children are created
        connectivity.add_phase_children(self.network, xfmr_end, [terminal], phases=phases)  # type:ignore
        return xfmr, terminal, xfmr_end

    def add_transformer_phase_end(
        self,
        xfmr: CN.PowerTransformer,
        *,
        endNumber: int,
        sequenceNumber: int,
        phase: str,
        phaseNeutralU: float | Qty | None = None,
        grounded: bool | None = None,
    ) -> tuple[CN.PowerTransformer, CN.TransformerPhaseEnd]:
        """
        Adds the real phase of one conductor of an end, on the end's Terminal
        * endNumber: integer, must match an existing PowerTransformerEnd of xfmr
        * sequenceNumber: integer, the lug sequenceNumber this conductor lands on
        * phase: single phase kind string, A|B|C|N|s1|s2
        * phaseNeutralU: phase-to-neutral rated voltage, float in V or Qty('kV')
        * grounded: boolean, this conductor is grounded if true (e.g. the neutral)
        """
        cn: CN = self.cim  # type:ignore
        xfmr_ends = [end for end in xfmr.PowerTransformerEnd if end.endNumber == endNumber]
        if len(xfmr_ends) != 1:
            raise ValueError(
                f"{xfmr.mRID!r}: phase end needs exactly one PowerTransformerEnd with "
                f"endNumber {endNumber}, found {len(xfmr_ends)}"
            )
        phase_end = cn.TransformerPhaseEnd(mRID=f"{xfmr.mRID}_{endNumber}_{phase.lower()}")
        graph_write.set_attr(phase_end, CN, "endNumber", endNumber)
        graph_write.set_attr(phase_end, CN, "sequenceNumber", sequenceNumber)
        graph_write.set_attr(phase_end, CN, "phase", cn.SinglePhaseKind(phase))
        graph_write.set_attr(phase_end, CN, "phaseNeutralU", phaseNeutralU)
        graph_write.set_attr(phase_end, CN, "grounded", grounded)
        graph_write.set_assc(phase_end, CN, "Terminal", xfmr_ends[0].Terminal)
        graph_write.add_to_graph(self.network, phase_end)
        return xfmr, phase_end

    def _resolve_tank(self, xfmr: CONSTR.PowerTransformer, TransformerTank: mRID) -> CONSTR.TransformerTank:
        """The tank of xfmr a lug, core or winding belongs to"""
        constr: CONSTR = self.cim  # type:ignore
        tank: CONSTR.TransformerTank | None = graph_write.resolve(
            self.network, constr.TransformerTank, TransformerTank
        )  # type:ignore
        if tank is None or tank.PowerTransformer is not xfmr:
            raise ValueError(f"{xfmr.mRID!r}: {TransformerTank!r} is not a tank of this transformer")
        return tank


class TransformerBankBuilder(TransformerBankBaseBuilder):
    """
    Builder for transformer banks whose tanks are described directly (e.g. open-wye open-delta).
    Builder functions to be called in the following order:
    * create() - instantiate the PowerTransformer
    * add_connectivity() - set the EquipmentContainer
    * add_power_transformer_end() - create each end with its Terminal and phases, no ratings
    * add_transformer_tank() - create one tank with %Z, loadloss, etc. for every physical tank
    * add_transformer_phase_end() - one phase end for every conductor the tank lugs land on
    * add_transformer_lug() - create one lug for every physical connection point, including ungrounded floating lugs
    * add_transformer_core() - optional, adds the physical core
    * add_transformer_winding() - create windings across lugs and core, triplex split-phase tanks have 3 windings
    * add_mesh_impedance() - create mesh impedance across pairs of windings
    """

    def add_transformer_tank(
        self,
        xfmr: CONSTR.PowerTransformer,
        *,
        TransformerTank: mRID | None = None,
        loadLoss: float | Qty | None = None,
        noLoadLoss: float | Qty | None = None,
        percentImpedance: float | None = None,
        percentMagnetizingCurrent: float | None = None,
    ) -> tuple[CONSTR.PowerTransformer, CONSTR.TransformerTank]:
        """
        Adds a physical tank with its nameplate data to the PowerTransformer
        * TransformerTank: mRID of the new tank, default <xfmr>_tank. Give one per tank for multi-tank banks (e.g. <xfmr>_tank_l)
        * loadLoss: active power thermal loss at rated power, float in W or Qty('kW')
        * noLoadLoss: active power thermal loss at no load, float in W or Qty('kW')
        * percentImpedance: %Z or %IZ, float in percentage (e.g. 2.7)
        * percentMagnetizingCurrent: magnetizing current as percentage of base current, float
        """
        constr: CONSTR = self.cim  # type:ignore
        if TransformerTank is None:
            TransformerTank = f"{xfmr.mRID}_tank"
        tank = constr.TransformerTank(mRID=TransformerTank)
        graph_write.set_assc(tank, CONSTR, "PowerTransformer", xfmr)
        graph_write.set_assc(tank, CN, "EquipmentContainer", xfmr.EquipmentContainer)
        graph_write.set_attr(tank, EL_UNBAL, "loadLoss", loadLoss)
        graph_write.set_attr(tank, EL_UNBAL, "noLoadLoss", noLoadLoss)
        graph_write.set_attr(tank, EL_UNBAL, "percentImpedance", percentImpedance)
        graph_write.set_attr(
            tank, EL_UNBAL, "percentMagnetizingCurrent", percentMagnetizingCurrent
        )
        graph_write.add_to_graph(self.network, tank)
        return xfmr, tank

    def add_transformer_lug(
        self,
        xfmr: CONSTR.PowerTransformer,
        *,
        TransformerTank: mRID,
        designation: str,
        sequenceNumber: int | None = None,
        TransformerEnd: mRID | None = None,
    ) -> tuple[CONSTR.PowerTransformer, CONSTR.TransformerLug]:
        """
        Add a physical lug / bushing to a tank
        * TransformerTank: mRID of the tank this lug is on
        * designation: string from IEEE c57.12.70 nameplate - high side is H1,H2,H3, low-side is X1,X2,X3 for xfmr over 200kVA and 8660V; smaller transformers use additive polarity X3,X2,X1.
        * sequenceNumber: integer, the conductor this lug lands on, matches the TransformerPhaseEnd sequenceNumber
        * TransformerEnd: mRID of the TransformerPhaseEnd this lug is aggregated into. None for floating lugs
        """
        constr: CONSTR = self.cim  # type:ignore
        tank = self._resolve_tank(xfmr, TransformerTank)
        lug = constr.TransformerLug(mRID=f"{tank.mRID}_lug_{designation.lower()}")
        graph_write.set_attr(lug, CONSTR, "designation", designation)
        graph_write.set_attr(lug, CONSTR, "sequenceNumber", sequenceNumber)
        graph_write.set_assc(lug, CONSTR, "TransformerTank", tank)
        if TransformerEnd is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=lug,
                profile_part=CONSTR,
                association_name="TransformerEnd",
                target_class=constr.TransformerEnd,
                target_mRID=TransformerEnd,
            )
        graph_write.add_to_graph(self.network, lug)
        return xfmr, lug

    def add_transformer_core(
        self,
        xfmr: CONSTR.PowerTransformer,
        *,
        TransformerTank: mRID,
        form: str,
        b: float | Qty | None = None,
        g: float | Qty | None = None,
        b0: float | Qty | None = None,
        g0: float | Qty | None = None,
    ) -> tuple[CONSTR.PowerTransformer, CONSTR.TransformerCore]:
        """
        Adds a transformer core to a tank
        * TransformerTank: mRID of the tank this core is in
        * form: string, coreForm|shellForm
        * b: core shunt susceptance, float in siemens or Qty('S')
        * g: core shunt conductance, float in siemens or Qty('S')
        * b0: zero sequence shunt susceptance, float in siemens or Qty('S')
        * g0: zero sequence shunt conductance, float in siemens or Qty('S')
        """
        constr: CONSTR = self.cim  # type:ignore
        tank = self._resolve_tank(xfmr, TransformerTank)
        core = constr.TransformerCore(mRID=f"{tank.mRID}_core")
        graph_write.set_attr(core, CONSTR, "form", constr.CoreConstructionKind(form))
        graph_write.set_attr(core, EL_UNBAL, "b", b)
        graph_write.set_attr(core, EL_UNBAL, "g", g)
        graph_write.set_attr(core, SC, "b0", b0)
        graph_write.set_attr(core, SC, "g0", g0)
        graph_write.set_assc(core, CONSTR, "TransformerTank", tank)
        graph_write.add_to_graph(self.network, core)
        return xfmr, core

    def add_transformer_winding(
        self,
        xfmr: CONSTR.PowerTransformer,
        *,
        TransformerTank: mRID,
        FromTransformerLug: mRID,
        ToTransformerLug: mRID,
        AutoTransformerLug: mRID | None = None,
        TransformerCore: mRID | None = None,
        connection: str,
        baseS: float | Qty | None = None,
        baseU: float | Qty | None = None,
        ratedS: float | Qty | None = None,
        ratedU: float | Qty | None = None,
        r: float | Qty | None = None,
        rDC: float | Qty | None = None,
    ) -> tuple[CONSTR.PowerTransformer, CONSTR.TransformerWinding]:
        """
        Adds a single coil wound between two lugs of a tank
        * TransformerTank: mRID of the tank this coil is in
        * FromTransformerLug: mRID of the lug at the start of the coil
        * ToTransformerLug: mRID of the lug at the end of the coil
        * AutoTransformerLug: mRID of the common lug, autotransformer windings only
        * TransformerCore: mRID of the core this coil is wound on
        * connection: string, D|G|I|Y|Yn
        * baseS: per-coil base power for pu impedances, float in VA or Qty('kVA')
        * baseU: coil base voltage for pu impedances, float in V or Qty('kV')
        * ratedS: coil apparent power rating, float in VA or Qty('kVA')
        * ratedU: coil rated voltage, float in V or Qty('kV')
        * r: coil resistance, float in ohm or Qty('ohm'|'pu'|'percent') on baseU/baseS
        * rDC: coil DC resistance, float in ohm or Qty('ohm'|'pu'|'percent') on baseU/baseS
        """
        constr: CONSTR = self.cim  # type:ignore
        tank = self._resolve_tank(xfmr, TransformerTank)
        from_lug = graph_write.resolve(self.network, constr.TransformerLug, FromTransformerLug)
        to_lug = graph_write.resolve(self.network, constr.TransformerLug, ToTransformerLug)
        if from_lug is None or to_lug is None:
            raise ValueError(
                f"{tank.mRID!r}: winding references lugs "
                f"{FromTransformerLug!r}/{ToTransformerLug!r}, not both found in graph"
            )
        winding = constr.TransformerWinding(
            mRID=f"{tank.mRID}_wdg_{from_lug.designation.lower()}{to_lug.designation.lower()}"  # type:ignore
        )
        graph_write.set_assc(winding, CONSTR, "FromTransformerLug", from_lug)
        graph_write.set_assc(winding, CONSTR, "ToTransformerLug", to_lug)
        if AutoTransformerLug is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=winding,
                profile_part=CONSTR,
                association_name="AutoTransformerLug",
                target_class=constr.TransformerLug,
                target_mRID=AutoTransformerLug,
            )
        if TransformerCore is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=winding,
                profile_part=CONSTR,
                association_name="TransformerCore",
                target_class=constr.TransformerCore,
                target_mRID=TransformerCore,
            )
        graph_write.set_assc(winding, CONSTR, "TransformerTank", tank)
        graph_write.set_attr(
            winding, CONSTR, "connection", constr.PhaseShuntConnectionKind(connection)
        )
        # ratings first: a pu/percent r or rDC converts against baseU/baseS
        graph_write.set_attr(winding, EL_UNBAL, "baseS", baseS)
        graph_write.set_attr(winding, EL_UNBAL, "baseU", baseU)
        graph_write.set_attr(winding, EL_UNBAL, "ratedS", ratedS)
        graph_write.set_attr(winding, EL_UNBAL, "ratedU", ratedU)
        graph_write.set_attr(winding, EL_UNBAL, "r", r)
        graph_write.set_attr(winding, EL_UNBAL, "rDC", rDC)
        graph_write.add_to_graph(self.network, winding)
        return xfmr, winding

    def add_mesh_impedance(  # type:ignore[override]
        self,
        xfmr: CONSTR.PowerTransformer,
        *,
        FromWinding: mRID,
        ToWinding: mRID,
        r: float | Qty | None = None,
        x: float | Qty | None = None,
    ) -> tuple[CONSTR.PowerTransformer, EL_UNBAL.TransformerMeshImpedance]:
        """
        Mesh impedance between a pair of windings of a tank. b and g are specified on the core
        * FromWinding: mRID of the "from" winding, whose baseU / baseS is the pu base
        * ToWinding: mRID of the "to" winding
        * r: resistance, float in ohm or Qty('ohm'|'pu'|'percent')
        * x: reactance, float in ohm or Qty('ohm'|'pu'|'percent')
        """
        constr: CONSTR = self.cim  # type:ignore
        el_unbal: EL_UNBAL = self.cim  # type:ignore
        from_winding = graph_write.resolve(self.network, constr.TransformerWinding, FromWinding)
        to_winding = graph_write.resolve(self.network, constr.TransformerWinding, ToWinding)
        if from_winding is None or to_winding is None:
            raise ValueError(
                f"{xfmr.mRID!r}: mesh impedance references windings "
                f"{FromWinding!r}/{ToWinding!r}, not both found in graph"
            )
        tank = from_winding.TransformerTank
        from_suffix = FromWinding.removeprefix(f"{tank.mRID}_wdg_")
        to_suffix = ToWinding.removeprefix(f"{tank.mRID}_wdg_")
        mesh = el_unbal.TransformerMeshImpedance(mRID=f"{tank.mRID}_mesh_{from_suffix}{to_suffix}")
        for association_name, target_mRID in (("FromWinding", FromWinding), ("ToWinding", ToWinding)):
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=mesh,
                profile_part=EL_UNBAL,
                association_name=association_name,
                target_class=el_unbal.TransformerWinding,
                target_mRID=target_mRID,
            )
        # associations first: a pu/percent r or x converts against FromWinding's baseU/baseS
        graph_write.set_attr(mesh, EL_UNBAL, "r", r)
        graph_write.set_attr(mesh, EL_UNBAL, "x", x)
        graph_write.add_to_graph(self.network, mesh)
        return xfmr, mesh


class TransformerBankFromConfigurationBuilder(TransformerBankBaseBuilder):
    """
    Builder for transformer instances built from TransformerTankConfiguration templates
    (e.g. padmount_example.cimtbl). Builder functions to be called in the following order:
    * create() - instantiate the PowerTransformer
    * add_connectivity() - set the EquipmentContainer
    * add_power_transformer_end() - create each end with its Terminal and phases, no ratings
    * add_transformer_tank() - create one tank for every physical tank, pointing at its template
    * add_transformer_phase_end() - one phase end for every conductor the template's lugs land on
    Build the template first with TransformerTankConfigurationBuilder. Ratings, impedances, lugs and
    windings live on the template
    """

    def add_transformer_tank(
        self,
        xfmr: CONSTR.PowerTransformer,
        *,
        TankConfiguration: mRID,
        TransformerTank: mRID | None = None,
    ) -> tuple[CONSTR.PowerTransformer, CONSTR.TransformerTank]:
        """
        Adds a physical tank built from a TransformerTankConfiguration template
        * TankConfiguration: mRID of the TransformerTankConfiguration template
        * TransformerTank: mRID of the new tank, default <xfmr>_tank. Give one per tank for multi-tank banks (e.g. <xfmr>_tank_l)
        """
        constr: CONSTR = self.cim  # type:ignore
        if TransformerTank is None:
            TransformerTank = f"{xfmr.mRID}_tank"
        tank = constr.TransformerTank(mRID=TransformerTank)
        graph_write.set_assc(tank, CONSTR, "PowerTransformer", xfmr)
        graph_write.set_assc(tank, CN, "EquipmentContainer", xfmr.EquipmentContainer)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=tank,
            profile_part=CONSTR,
            association_name="TankConfiguration",
            target_class=constr.TransformerTankConfiguration,
            target_mRID=TankConfiguration,
        )
        graph_write.add_to_graph(self.network, tank)
        return xfmr, tank
