import cimprofiles.cim18.cim18v17.construction as CONSTR
import cimprofiles.cim18.cim18v17.short_circuit as SC
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class TransformerTankConfigurationBuilder(ObjectBuilder):
    """
    Builder for transformer banks composed of one of more configs. Builder functions to be called in the following order:
    * create() - instantiate the TransformerTankConfiguration
    * add_power_transformer_end() - create TransformerTankConfigurationEnd, optionally create one phase end for every phase on high side and low side
    * add_transformer_config() - create one config with %Z, loadloss, etc. for every physical config
    * add_transformer_phase_end() - add phaseNeutralU for existing phase ends or create new ones for each phase
    * add_transformer_lug() - create one lug for every physical connection point, including ungrounded floating lugs
    * add_transformer_core() - optional, adds the physical core
    * add_transformer_winding() - create windings across lugs and core, triplex split-phase configs have 3 windings
    * add_mesh_impedance() - create mesh impedance across pairs of windings
    """

    cim_class_name = "TransformerTankConfiguration"

    def add_electrical(
        self,
        config: CONSTR.TransformerTankConfiguration,
        *,
        loadLoss: float | Qty | None = None,
        noLoadLoss: float | Qty | None = None,
        percentImpdance: float | None = None,
        percentMagnetizingCurrent: float | None = None,
    ) -> CONSTR.TransformerTankConfiguration:
        """
        Adds a per-phase TransformerTank to the TransformerTankConfiguration
        * loadLoss: active power thermal loss at rated power, float in W or Qty('kW')
        * noLoadLoss: active power thermal loss at no load, float in W or Qty('kW')
        * percentImpedance: %Z or %IZ, float in percentage (e.g. 2.7)
        * percentMagnetizingCurrent: Magnetizing current expressed as percentage of base current, float
        """
        graph_write.set_attr(config, CONSTR, "loadLoss", loadLoss)
        graph_write.set_attr(config, CONSTR, "noLoadLoss", noLoadLoss)
        graph_write.set_attr(config, CONSTR, "percentImpedance", percentImpdance)
        graph_write.set_attr(
            config, CONSTR, "percentMagnetizingCurrent", percentMagnetizingCurrent
        )

        return config

    def add_transformer_phase_end(
        self,
        config: CONSTR.TransformerTankConfiguration,
        *,
        endNumber: int,
        sequenceNumber: int,
        phase: str,
        phaseNeutralU: float | Qty | None,
        TransformerPhaseEnd: mRID | None,
    ) -> tuple[CONSTR.TransformerTankConfiguration | None, CONSTR.TransformerPhaseEnd]:
        """
        Adds a single phase end for a transformer or configuration
        * endNumber: integer, must match the TransformerTankConfigurationEnd
        * sequenceNumber: integer, incrementing to match PhaseCode
        *
        """

        constr: CONSTR = self.cim  # type:ignore
        if TransformerPhaseEnd is None:
            mRID = f"{config.mRID}_end_{endNumber}_seq_{sequenceNumber}"
            phase_end = constr.TransformerPhaseEnd(mRID=mRID)
            graph_write.add_to_graph(self.network, phase_end)
        else:
            phase_end: CONSTR.TransformerPhaseEnd = graph_write.resolve(
                self.network, constr.TransformerPhaseEnd, TransformerPhaseEnd
            )  # type:ignore

        graph_write.set_attr(phase_end, CONSTR, "phase", constr.SinglePhaseKind(phase))
        graph_write.set_attr(phase_end, CONSTR, "phaseNeutralU", phaseNeutralU)
        graph_write.set_assc(phase_end, CONSTR, "TankConfiguration", config)

        return config, phase_end

    def add_transformer_lug(
        self,
        config: CONSTR.TransformerTankConfiguration,
        *,
        designation: str,
        sequenceNumber: int,
    ) -> tuple[CONSTR.TransformerTankConfiguration, CONSTR.TransformerLug]:
        """
        Add a physical lug / bushing to the transformer
        * designation: string from IEEE c57.12.70 nameplate - high side is H1,H2,H3, low-side is X1,X2,X3 for config over 200kVA and 8660V; smaller transformers use additive polarity X3,X2,X1.
        * TransformerTank: mRID of config for which this is a lug
        * TransformerEnd: mRID of TransformerPhaseEnd this lug is aggregated into
        """

        constr: CONSTR = self.cim  # type:ignore
        mRID = f"{config.mRID}_lug_{designation}_seq_{sequenceNumber}"
        lug = constr.TransformerLug(mRID=mRID)
        graph_write.set_attr(lug, CONSTR, "designation", designation)
        graph_write.set_attr(lug, CONSTR, "sequenceNumber", sequenceNumber)
        graph_write.set_assc(lug, CONSTR, "TankConfiguration", config)
        graph_write.add_to_graph(self.network, lug)
        return config, lug

    def add_transformer_core(
        self,
        config: CONSTR.TransformerTankConfiguration,
        *,
        form: str,
        b: float | Qty | None = None,
        g: float | Qty | None = None,
        b0: float | Qty | None = None,
        g0: float | Qty | None = None,
    ) -> tuple[CONSTR.TransformerTankConfiguration, CONSTR.TransformerCore]:
        """
        Adds a transformer core to the transformer config
        * form: string, coreForm|shellForm
        * b: core shunt susceptance, float in siemens or Qty('S')
        * g: core sequence shunt conductance, float in siemens or Qty('S')
        * b0: zero sequence shunt susceptance, float in siemens or Qty('S')
        * g0: zero sequence shunt conductance, float in siemens or Qty('S')
        """
        constr: CONSTR = self.cim  # type:ignore
        mRID = f"{config.mRID}_core"
        core = constr.TransformerCore(mRID=mRID)
        graph_write.set_attr(core, CONSTR, "form", constr.CoreConstructionKind(form))
        graph_write.set_attr(core, CONSTR, "b", b)
        graph_write.set_attr(core, CONSTR, "g", g)
        graph_write.set_attr(core, SC, "b0", b0)
        graph_write.set_attr(core, SC, "g0", g0)
        graph_write.add_to_graph(self.network, core)
        return config, core

    def add_transformer_winding(
        self,
        config: CONSTR.TransformerTankConfiguration | None,
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
    ) -> tuple[CONSTR.TransformerTankConfiguration | None, CONSTR.TransformerWinding]:

        constr: CONSTR = self.cim  # type:ignore
        from_lug: CONSTR.TransformerLug = graph_write.resolve(
            self.network, constr.TransformerLug, FromTransformerLug
        )  # type:ignore
        to_lug: CONSTR.TransformerLug = graph_write.resolve(
            self.network, constr.TransformerLug, ToTransformerLug
        )  # type:ignore

        mRID = f"{TransformerTank}_winding_{from_lug.designation}_{to_lug.designation}"
        winding = constr.TransformerWinding(mRID=mRID)

        graph_write.set_attr(
            winding, CONSTR, "connection", constr.PhaseShuntConnectionKind(connection)
        )
        graph_write.set_attr(winding, CONSTR, "baseS", baseS)
        graph_write.set_attr(winding, CONSTR, "baseU", baseU)
        graph_write.set_attr(winding, CONSTR, "ratedS", ratedS)
        graph_write.set_attr(winding, CONSTR, "ratedU", ratedU)
        graph_write.set_attr(winding, CONSTR, "r", r)
        graph_write.set_attr(winding, CONSTR, "rDC", rDC)
        graph_write.add_to_graph(self.network, winding)

        return config, winding

    def add_mesh_impedance(
        self,
        config: CONSTR.TransformerTankConfiguration,
        *,
        FromTransformerEnd: mRID,
        ToTransformerEnd: mRID,
        FromWinding: mRID,
        ToWinding: mRID,
        r: float | Qty | None = None,
        x: float | Qty | None = None,
    ) -> tuple[CONSTR.TransformerTankConfiguration, CONSTR.TransformerMeshImpedance]:
        """
        Mesh model for transformers with three or more windings. b and g are specified on the end
        * FromTransformerEnd: mRID of the "from" winding that specifies ratedU / ratedS
        * ToTransformerEnd: mRID of the "to" winding
        * r: positive sequence resistance, float in ohm or Qty('ohm'|'pu'|'percent')
        * x: positive sequence reactance, float in ohm or Qty('ohm'|'pu'|'percent')
        """
        el_bal: CONSTR = self.cim  # type:ignore
        config, mesh = super().add_mesh_impedance(
            config=config,
            FromTransformerEnd=FromTransformerEnd,
            ToTransformerEnd=ToTransformerEnd,
            r=r,
            x=x,
        )
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=mesh,
            profile_part=EL_BAL,
            association_name="FromWinding",
            target_class=el_bal.TransformerWinding,
            target_mRID=FromWinding,
        )
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=mesh,
            profile_part=EL_BAL,
            association_name="ToWinding",
            target_class=el_bal.TransformerWinding,
            target_mRID=ToWinding,
        )
        return config, mesh
