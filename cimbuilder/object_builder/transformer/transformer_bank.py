import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.construction as CONSTR
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.short_circuit as SC
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.transformer.power_transformer import (
    PowerTransformerBuilder,
)

mRID = str


class TransformerBankBuilder(PowerTransformerBuilder):
    """
    Builder for transformer banks composed of one of more tanks. Builder functions to be called in the following order:
    * create() - instantiate the PowerTransformer
    * add_power_transformer_end() - create PowerTransformerEnd, optionally create one phase end for every phase on high side and low side
    * add_transformer_tank() - create one tank with %Z, loadloss, etc. for every physical tank
    * add_transformer_phase_end() - add phaseNeutralU for existing phase ends or create new ones for each phase
    * add_transformer_lug() - create one lug for every physical connection point, including ungrounded floating lugs
    * add_transformer_core() - optional, adds the physical core
    * add_transformer_winding() - create windings across lugs and core, triplex split-phase tanks have 3 windings
    * add_mesh_impedance() - create mesh impedance across pairs of windings
    """

    cim_class_name = "PowerTransformer"

    def add_connectivity(
        self, xfmr: CN.PowerTransformer, *, EquipmentContainer: mRID | None = None
    ) -> CN.PowerTransformer:
        return super().add_connectivity(xfmr, EquipmentContainer=EquipmentContainer)

    def add_power_transformer_end(
        self,
        xfmr: CN.PowerTransformer,
        *,
        node: mRID,
        endNumber: int,
        connectionKind: str | None = None,
        BaseVoltage: mRID,
        phases: str | None,
        TankConfiguration: mRID | None,
    ) -> tuple[CN.PowerTransformer, CN.Terminal, CN.PowerTransformerEnd]:
        xfmr, terminal, xfmr_end = super().add_power_transformer_end(
            xfmr,
            node=node,
            endNumber=endNumber,
            connectionKind=connectionKind,
            BaseVoltage=BaseVoltage,
        )

        if phases is not None:
            graph_write.set_attr(terminal, CN, "phases", phases)

            for sequenceNumber, phase in enumerate(phases):
                self.add_transformer_phase_end(
                    xfmr=xfmr,  # type:ignore
                    endNumber=endNumber,
                    sequenceNumber=sequenceNumber + 1,  # start with 1
                    phase=phase,
                    phaseNeutralU=None,
                    TankConfiguration=TankConfiguration,
                    TransformerPhaseEnd=None,
                )

        return xfmr, terminal, xfmr_end

    def add_transformer_tank(
        self,
        xfmr: CONSTR.PowerTransformer,
        *,
        TransformerTank: mRID,
        loadLoss: float | Qty | None = None,
        noLoadLoss: float | Qty | None = None,
        percentImpdance: float | None = None,
        percentMagnetizingCurrent: float | None = None,
        TankConfiguration: mRID | None = None,
    ) -> tuple[CONSTR.PowerTransformer, CONSTR.TransformerTank]:
        """
        Adds a per-phase TransformerTank to the PowerTransformer
        * TransformerTank: mRID of the tank to be added
        * loadLoss: active power thermal loss at rated power, float in W or Qty('kW')
        * noLoadLoss: active power thermal loss at no load, float in W or Qty('kW')
        * percentImpedance: %Z or %IZ, float in percentage (e.g. 2.7)
        * percentMagnetizingCurrent: Magnetizing current expressed as percentage of base current, float
        * TankConfiguration: mRID of tank configuation template (equivalent to OpenDSS XfmrCode)
        """
        constr: CONSTR = self.cim  # type:ignore
        tank = self.network.find_by_mRID(mRID=TransformerTank)
        if tank is not None and not isinstance(tank, constr.TransformerTank):
            raise ValueError(
                f"{TransformerTank} is another object that is not a TransformerTank"
            )
        if not tank:
            tank = constr.TransformerTank(mRID=TransformerTank)

        graph_write.set_assc(tank, CONSTR, "PowerTransformer", xfmr)
        graph_write.set_assc(
            tank, CONSTR, "EquipmentContainer", xfmr.EquipmentContainer
        )
        graph_write.set_attr(tank, CONSTR, "loadLoss", loadLoss)
        graph_write.set_attr(tank, CONSTR, "noLoadLoss", noLoadLoss)
        graph_write.set_attr(tank, CONSTR, "percentImpedance", percentImpdance)
        graph_write.set_attr(
            tank, CONSTR, "percentMagnetizingCurrent", percentMagnetizingCurrent
        )

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

    def add_transformer_phase_end(
        self,
        xfmr: CONSTR.PowerTransformer | None,
        *,
        endNumber: int,
        sequenceNumber: int,
        phase: str,
        phaseNeutralU: float | Qty | None,
        TankConfiguration: mRID | None,
        TransformerPhaseEnd: mRID | None,
    ) -> tuple[CONSTR.PowerTransformer | None, CONSTR.TransformerPhaseEnd]:
        """
        Adds a single phase end for a transformer or configuration
        * endNumber: integer, must match the PowerTransformerEnd
        * sequenceNumber: integer, incrementing to match PhaseCode
        *
        """

        constr: CONSTR = self.cim  # type:ignore
        if TransformerPhaseEnd is None:
            if TankConfiguration is not None:
                mRID = f"{TankConfiguration}_end_{endNumber}_seq_{sequenceNumber}"
            elif xfmr is not None:
                mRID = f"{xfmr.mRID}_end_{endNumber}_seq_{sequenceNumber}"
            else:
                raise ValueError("Either xfmr or TankConfiguration must be specified")
            phase_end = constr.TransformerPhaseEnd(mRID=mRID)
            graph_write.add_to_graph(self.network, phase_end)
        else:
            phase_end: CONSTR.TransformerPhaseEnd = graph_write.resolve(
                self.network, constr.TransformerPhaseEnd, TransformerPhaseEnd
            )  # type:ignore

        graph_write.set_attr(phase_end, CONSTR, "phase", phase)
        graph_write.set_attr(phase_end, CONSTR, "phaseNeutralU", phaseNeutralU)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=phase_end,
            profile_part=CONSTR,
            association_name="TankConfiguration",
            target_class=constr.TransformerTankConfiguration,
            target_mRID=TankConfiguration,
        )

        return xfmr, phase_end

    def add_transformer_lug(
        self,
        xfmr: CONSTR.PowerTransformer,
        *,
        designation: str,
        TransformerTank: mRID,
        TransformerEnd: mRID,
    ) -> tuple[CONSTR.PowerTransformer, CONSTR.TransformerLug]:
        """
        Add a physical lug / bushing to the transformer
        * designation: string from IEEE c57.12.70 nameplate - high side is H1,H2,H3, low-side is X1,X2,X3 for xfmr over 200kVA and 8660V; smaller transformers use additive polarity X3,X2,X1.
        * TransformerTank: mRID of tank for which this is a lug
        * TransformerEnd: mRID of TransformerPhaseEnd this lug is aggregated into
        """

        constr: CONSTR = self.cim  # type:ignore
        mRID = f"{TransformerTank}_lug_{designation}"
        lug = constr.TransformerLug(mRID=mRID)
        graph_write.set_attr(lug, CONSTR, "designation", designation)

        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=lug,
            profile_part=CONSTR,
            association_name="TransformerTank",
            target_class=constr.TransformerTank,
            target_mRID=TransformerTank,
        )
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
        xfmr: CONSTR.PowerTransformer | None,
        *,
        TransformerTank: mRID,
        form: str,
        b: float | Qty | None = None,
        g: float | Qty | None = None,
        b0: float | Qty | None = None,
        g0: float | Qty | None = None,
    ) -> tuple[CONSTR.PowerTransformer | None, CONSTR.TransformerCore]:
        """
        Adds a transformer core to the transformer tank
        * form: string, coreForm|shellForm
        * b: core shunt susceptance, float in siemens or Qty('S')
        * g: core sequence shunt conductance, float in siemens or Qty('S')
        * b0: zero sequence shunt susceptance, float in siemens or Qty('S')
        * g0: zero sequence shunt conductance, float in siemens or Qty('S')
        """
        constr: CONSTR = self.cim  # type:ignore
        mRID = f"{TransformerTank}_core"
        core = constr.TransformerCore(mRID=mRID)
        graph_write.set_attr(core, EL_UNBAL, "form", form)
        graph_write.set_attr(core, EL_UNBAL, "b", b)
        graph_write.set_attr(core, EL_UNBAL, "g", g)
        graph_write.set_attr(core, SC, "b", b0)
        graph_write.set_attr(core, SC, "g", g0)
        graph_write.add_to_graph(self.network, core)
        return xfmr, core

    def add_transformer_winding(
        self,
        xfmr: CONSTR.PowerTransformer | None,
        *,
        TransformerTank: mRID,
        FromTransformerLug: mRID,
        ToTransformerLug: mRID,
        AutoTransformerLug: mRID | None = None,
        connection: str,
        baseS: float | Qty | None = None,
        baseU: float | Qty | None = None,
        ratedS: float | Qty | None = None,
        ratedU: float | Qty | None = None,
        r: float | Qty | None = None,
        rDC: float | Qty | None = None,
    ) -> tuple[CONSTR.PowerTransformer | None, CONSTR.TransformerWinding]:

        constr: CONSTR = self.cim  # type:ignore
        from_lug: CONSTR.TransformerLug = graph_write.resolve(
            self.network, constr.TransformerLug, FromTransformerLug
        )  # type:ignore
        to_lug: CONSTR.TransformerLug = graph_write.resolve(
            self.network, constr.TransformerLug, ToTransformerLug
        )  # type:ignore

        mRID = f"{TransformerTank}_winding_{from_lug.designation}_{to_lug.designation}"
        winding = constr.TransformerWinding(mRID=mRID)

        graph_write.set_attr(winding, CONSTR, "connection", connection)
        graph_write.set_attr(winding, CONSTR, "baseS", baseS)
        graph_write.set_attr(winding, CONSTR, "baseU", baseU)
        graph_write.set_attr(winding, CONSTR, "ratedS", ratedS)
        graph_write.set_attr(winding, CONSTR, "ratedU", ratedU)
        graph_write.set_attr(winding, CONSTR, "r", r)
        graph_write.set_attr(winding, CONSTR, "rDC", rDC)
        graph_write.add_to_graph(self.network, winding)

        return xfmr, winding

    def add_mesh_impedance(
        self,
        xfmr: EL_BAL.PowerTransformer,
        *,
        FromTransformerEnd: mRID,
        ToTransformerEnd: mRID,
        FromWinding: mRID,
        ToWinding: mRID,
        r: float | Qty | None = None,
        x: float | Qty | None = None,
    ) -> tuple[EL_BAL.PowerTransformer, EL_BAL.TransformerMeshImpedance]:
        """
        Mesh model for transformers with three or more windings. b and g are specified on the end
        * FromTransformerEnd: mRID of the "from" winding that specifies ratedU / ratedS
        * ToTransformerEnd: mRID of the "to" winding
        * r: positive sequence resistance, float in ohm or Qty('ohm'|'pu'|'percent')
        * x: positive sequence reactance, float in ohm or Qty('ohm'|'pu'|'percent')
        """
        constr: CONSTR = self.cim  # type:ignore
        xfmr, mesh = super().add_mesh_impedance(
            xfmr=xfmr,
            FromTransformerEnd=FromTransformerEnd,
            ToTransformerEnd=ToTransformerEnd,
            r=r,
            x=x,
        )
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=mesh,
            profile_part=CONSTR,
            association_name="FromWinding",
            target_class=constr.TransformerWinding,
            target_mRID=FromWinding,
        )
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=mesh,
            profile_part=CONSTR,
            association_name="ToWinding",
            target_class=constr.TransformerWinding,
            target_mRID=ToWinding,
        )
        return xfmr, mesh
