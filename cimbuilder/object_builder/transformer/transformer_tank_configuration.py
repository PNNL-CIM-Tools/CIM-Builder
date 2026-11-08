import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.construction as CONSTR
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.short_circuit as SC
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class TransformerTankConfigurationBuilder(ObjectBuilder):
    """
    Builder for a TransformerTankConfiguration: the reusable nameplate template (losses, %Z,
    phase ends, lugs, core, windings, mesh impedances) shared by every TransformerTank that
    references it. Builder functions to be called in the following order:
    * create() - instantiate the TransformerTankConfiguration
    * add_electrical() - %Z, load loss, no-load loss, %magnetizing current of the tank
    * add_transformer_phase_end() - create one phase end for every phase on high side and low side
    * add_transformer_lug() - create one lug for every physical connection point, including ungrounded floating lugs
    * add_transformer_core() - optional, adds the physical core
    * add_transformer_winding() - create windings across lugs and core, triplex split-phase configs have 3 windings
    * add_mesh_impedance() - create mesh impedance across pairs of windings
    """

    cim_class_name = "TransformerTankConfiguration"

    def add_electrical(
        self,
        config: EL_UNBAL.TransformerTankConfiguration,
        *,
        loadLoss: float | Qty | None = None,
        noLoadLoss: float | Qty | None = None,
        percentImpedance: float | None = None,
        percentMagnetizingCurrent: float | None = None,
    ) -> EL_UNBAL.TransformerTankConfiguration:
        """
        Adds the tank nameplate test data
        * loadLoss: active power thermal loss at rated power, float in W or Qty('kW')
        * noLoadLoss: active power thermal loss at no load, float in W or Qty('kW')
        * percentImpedance: %Z or %IZ, float in percentage (e.g. 2.7)
        * percentMagnetizingCurrent: Magnetizing current expressed as percentage of base current, float
        """
        graph_write.set_attr(config, EL_UNBAL, "loadLoss", loadLoss)
        graph_write.set_attr(config, EL_UNBAL, "noLoadLoss", noLoadLoss)
        graph_write.set_attr(config, EL_UNBAL, "percentImpedance", percentImpedance)
        graph_write.set_attr(
            config, EL_UNBAL, "percentMagnetizingCurrent", percentMagnetizingCurrent
        )
        return config

    def add_transformer_phase_end(
        self,
        config: CONSTR.TransformerTankConfiguration,
        *,
        endNumber: int,
        sequenceNumber: int,
        phase: str,
        phaseNeutralU: float | Qty | None = None,
    ) -> tuple[CONSTR.TransformerTankConfiguration, CN.TransformerPhaseEnd]:
        """
        Adds a single phase end to the configuration
        * endNumber: integer, highest voltage side is end #1
        * sequenceNumber: integer, incrementing to match PhaseCode
        * phase: single phase kind string, A|B|C|N|s1|s2|X|Y
        * phaseNeutralU: phase-to-neutral rated voltage, float in V or Qty('kV')
        """
        cn: CN = self.cim  # type:ignore
        phase_end = cn.TransformerPhaseEnd(
            mRID=f"{config.mRID}_end_{endNumber}_seq_{sequenceNumber}"
        )
        graph_write.set_attr(phase_end, CN, "endNumber", endNumber)
        graph_write.set_attr(phase_end, CN, "sequenceNumber", sequenceNumber)
        graph_write.set_attr(phase_end, CN, "phase", cn.SinglePhaseKind(phase))
        graph_write.set_attr(phase_end, CN, "phaseNeutralU", phaseNeutralU)
        graph_write.set_assc(phase_end, CONSTR, "TankConfiguration", config)
        graph_write.add_to_graph(self.network, phase_end)
        return config, phase_end

    def add_transformer_lug(
        self,
        config: CONSTR.TransformerTankConfiguration,
        *,
        designation: str,
        sequenceNumber: int,
        TransformerEnd: mRID | None = None,
    ) -> tuple[CONSTR.TransformerTankConfiguration, CONSTR.TransformerLug]:
        """
        Add a physical lug / bushing to the configuration
        * designation: string from IEEE c57.12.70 nameplate - high side is H1,H2,H3, low-side is X1,X2,X3 for config over 200kVA and 8660V; smaller transformers use additive polarity X3,X2,X1.
        * sequenceNumber: integer, order of the lug on the tank
        * TransformerEnd: mRID of TransformerPhaseEnd this lug is aggregated into. None for floating lugs
        """
        constr: CONSTR = self.cim  # type:ignore
        lug = constr.TransformerLug(
            mRID=f"{config.mRID}_lug_{designation}_seq_{sequenceNumber}"
        )
        graph_write.set_attr(lug, CONSTR, "designation", designation)
        graph_write.set_attr(lug, CONSTR, "sequenceNumber", sequenceNumber)
        graph_write.set_assc(lug, CONSTR, "TankConfiguration", config)
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
        * g: core shunt conductance, float in siemens or Qty('S')
        * b0: zero sequence shunt susceptance, float in siemens or Qty('S')
        * g0: zero sequence shunt conductance, float in siemens or Qty('S')
        """
        constr: CONSTR = self.cim  # type:ignore
        core = constr.TransformerCore(mRID=f"{config.mRID}_core")
        graph_write.set_attr(core, CONSTR, "form", constr.CoreConstructionKind(form))
        graph_write.set_attr(core, EL_UNBAL, "b", b)
        graph_write.set_attr(core, EL_UNBAL, "g", g)
        graph_write.set_attr(core, SC, "b0", b0)
        graph_write.set_attr(core, SC, "g0", g0)
        graph_write.set_assc(core, CONSTR, "TankConfiguration", config)
        graph_write.add_to_graph(self.network, core)
        return config, core

    def add_transformer_winding(
        self,
        config: CONSTR.TransformerTankConfiguration,
        *,
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
    ) -> tuple[CONSTR.TransformerTankConfiguration, CONSTR.TransformerWinding]:
        """
        Adds a single coil wound between two lugs
        * FromTransformerLug: mRID of the lug at the start of the coil
        * ToTransformerLug: mRID of the lug at the end of the coil
        * AutoTransformerLug: mRID of the common lug, autotransformer windings only
        * TransformerCore: mRID of the core this coil is wound on
        * connection: string, D|G|I|Y|Yn
        * baseS: per-coil base power for pu impedances (e.g. ratedS/3 on a 3-phase coil), float in VA or Qty('kVA')
        * baseU: coil base voltage for pu impedances, float in V or Qty('kV')
        * ratedS: coil apparent power rating, float in VA or Qty('kVA')
        * ratedU: coil rated voltage, float in V or Qty('kV')
        * r: coil resistance, float in ohm or Qty('ohm'|'pu'|'percent') on baseU/baseS
        * rDC: coil DC resistance, float in ohm or Qty('ohm'|'pu'|'percent') on baseU/baseS
        """
        constr: CONSTR = self.cim  # type:ignore
        from_lug = graph_write.resolve(self.network, constr.TransformerLug, FromTransformerLug)
        to_lug = graph_write.resolve(self.network, constr.TransformerLug, ToTransformerLug)
        if from_lug is None or to_lug is None:
            raise ValueError(
                f"{config.mRID!r}: winding references lugs "
                f"{FromTransformerLug!r}/{ToTransformerLug!r}, not both found in graph"
            )
        winding = constr.TransformerWinding(
            mRID=f"{config.mRID}_winding_{from_lug.designation}_{to_lug.designation}"  # type:ignore
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
        graph_write.set_assc(winding, CONSTR, "TankConfiguration", config)
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
        return config, winding

    def add_mesh_impedance(
        self,
        config: EL_UNBAL.TransformerTankConfiguration,
        *,
        FromTransformerEnd: mRID,
        ToTransformerEnd: mRID,
        FromWinding: mRID,
        ToWinding: mRID,
        r: float | Qty | None = None,
        x: float | Qty | None = None,
    ) -> tuple[EL_UNBAL.TransformerTankConfiguration, EL_UNBAL.TransformerMeshImpedance]:
        """
        Mesh impedance between a pair of windings. b and g are specified on the core
        * FromTransformerEnd: mRID of the TransformerPhaseEnd on the "from" side
        * ToTransformerEnd: mRID of the TransformerPhaseEnd on the "to" side
        * FromWinding: mRID of the "from" winding, whose baseU / baseS is the pu base
        * ToWinding: mRID of the "to" winding
        * r: resistance, float in ohm or Qty('ohm'|'pu'|'percent')
        * x: reactance, float in ohm or Qty('ohm'|'pu'|'percent')
        """
        el_unbal: EL_UNBAL = self.cim  # type:ignore
        mesh = el_unbal.TransformerMeshImpedance(mRID=f"{FromWinding}_mesh_{ToWinding}")
        associations = {
            "FromTransformerEnd": (el_unbal.TransformerEnd, FromTransformerEnd),
            "ToTransformerEnd": (el_unbal.TransformerEnd, ToTransformerEnd),
            "FromWinding": (el_unbal.TransformerWinding, FromWinding),
            "ToWinding": (el_unbal.TransformerWinding, ToWinding),
        }
        for association_name, (target_class, target_mRID) in associations.items():
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=mesh,
                profile_part=EL_UNBAL,
                association_name=association_name,
                target_class=target_class,
                target_mRID=target_mRID,
            )
        # associations first: a pu/percent r or x converts against FromWinding's baseU/baseS
        graph_write.set_attr(mesh, EL_UNBAL, "r", r)
        graph_write.set_attr(mesh, EL_UNBAL, "x", x)
        graph_write.add_to_graph(self.network, mesh)
        return config, mesh
