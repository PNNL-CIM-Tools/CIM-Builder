import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.construction as CONSTR
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
from cimtables import connectivity, graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class VoltageRegulatorBuilder(ObjectBuilder):
    """
    Builder for step-voltage regulators, modeled as an AutoTransformer with one series winding
    and two AutoTransformerEnds. Builder functions to be called in the following order:
    * create() - instantiate the VoltageRegulator
    * add_connectivity() - set the EquipmentContainer and ANSI construction type
    * add_auto_transformer_end() - create each end and its Terminal, end 1 is S (source), end 2 is L (load)
    * add_electrical() - add baseU / ratedS to each end
    * add_transformer_lug() - create the S, L and SL lugs
    * add_transformer_winding() - create the series winding across the lugs
    Build the RatioTapChanger on the regulated end and its TapChangerControl with
    RatioTapChangerBuilder and TapChangerControlBuilder
    """

    cim_class_name = "VoltageRegulator"

    def add_connectivity(
        self,
        regulator: CN.VoltageRegulator,
        *,
        construction: str | None = None,
        EquipmentContainer: mRID | None = None,
    ) -> CN.VoltageRegulator:
        """
        Adds base connectivity layer of equipment containment. Add nodes using add_auto_transformer_end
        * construction: ANSI C57.15 regulator type, typeA|typeB
        * EquipmentContainer: mRID of the Substation or Feeder containing the regulator.
        Note: do NOT set BaseVoltage for VoltageRegulator. It is set for each end individually
        """
        cn: CN = self.cim  # type: ignore
        if construction is not None:
            graph_write.set_attr(
                regulator, CN, "construction", cn.RegulatorConstructionKind(construction)
            )
        if EquipmentContainer is None:
            EquipmentContainer = self.container.mRID
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=regulator,
            profile_part=CN,
            association_name="EquipmentContainer",
            target_class=cn.EquipmentContainer,
            target_mRID=EquipmentContainer,
        )
        return regulator

    def add_auto_transformer_end(
        self,
        regulator: CN.VoltageRegulator,
        *,
        node: mRID,
        endNumber: int,
        phase: str,
        BaseVoltage: mRID,
    ) -> tuple[CN.VoltageRegulator, CN.Terminal, CN.AutoTransformerEnd]:
        """
        Adds one end with its Terminal on the regulator (sequenceNumber = endNumber)
        * node: mRID of the ConnectivityNode or TopologicalNode for this end
        * endNumber: integer, 1 for the S (source) side, 2 for the L (load) side
        * phase: phase-code string of the end, also set on its Terminal (e.g. AN)
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore
        end = cn.AutoTransformerEnd(mRID=f"{regulator.mRID}_end{endNumber}")
        graph_write.set_attr(end, CN, "endNumber", endNumber)
        graph_write.set_attr(end, CN, "phase", cn.PhaseCode(phase))
        graph_write.set_assc(end, CN, "AutoTransformer", regulator)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=end,
            profile_part=CN,
            association_name="BaseVoltage",
            target_class=cn.BaseVoltage,
            target_mRID=BaseVoltage,
        )
        graph_write.add_to_graph(self.network, end)
        # needs the end's AutoTransformer, endNumber and phase set first
        terminals = connectivity.add_connectivity(
            network=self.network,
            equipment=end,
            node_cols={"node": node},
        )
        return regulator, terminals[0], end

    def add_electrical(
        self,
        end: EL_UNBAL.AutoTransformerEnd,
        *,
        baseU: float | Qty,
        ratedS: float | Qty,
        rground: float | Qty | None = None,
        xground: float | Qty | None = None,
    ) -> EL_UNBAL.AutoTransformerEnd:
        """
        Adds the ratings of one end
        * baseU: coil voltage, float in V or Qty('kV')
        * ratedS: through rating of the regulator, float in VA or Qty('kVA')
        * rground: grounding resistance, float in ohm or Qty('ohm')
        * xground: grounding reactance, float in ohm or Qty('ohm')
        """
        graph_write.set_attr(end, EL_UNBAL, "baseU", baseU)
        graph_write.set_attr(end, EL_UNBAL, "ratedS", ratedS)
        graph_write.set_attr(end, EL_UNBAL, "rground", rground)
        graph_write.set_attr(end, EL_UNBAL, "xground", xground)
        return end

    def add_transformer_lug(
        self,
        regulator: CN.VoltageRegulator,
        *,
        designation: str,
        sequenceNumber: int,
        TransformerEnd: mRID | None = None,
    ) -> tuple[CN.VoltageRegulator, CONSTR.TransformerLug]:
        """
        Add a physical lug / bushing to the regulator
        * designation: string from ANSI C57.15 - S source, L load, SL source-load
        * sequenceNumber: integer, order of the lug on the regulator
        * TransformerEnd: mRID of AutoTransformerEnd this lug is aggregated into. None for the SL lug
        """
        constr: CONSTR = self.cim  # type:ignore
        lug = constr.TransformerLug(mRID=f"{regulator.mRID}_lug_{designation.lower()}")
        graph_write.set_attr(lug, CONSTR, "designation", designation)
        graph_write.set_attr(lug, CONSTR, "sequenceNumber", sequenceNumber)
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
        return regulator, lug

    def add_transformer_winding(
        self,
        regulator: CN.VoltageRegulator,
        *,
        FromTransformerEnd: mRID,
        ToTransformerEnd: mRID,
        FromTransformerLug: mRID,
        ToTransformerLug: mRID,
        AutoTransformerLug: mRID,
        baseS: float | Qty | None = None,
        baseU: float | Qty | None = None,
        ratedS: float | Qty | None = None,
        ratedU: float | Qty | None = None,
        r: float | Qty | None = None,
        rDC: float | Qty | None = None,
    ) -> tuple[CN.VoltageRegulator, CONSTR.TransformerWinding]:
        """
        Adds the series winding. A regulator owns exactly one winding
        * FromTransformerEnd: mRID of the AutoTransformerEnd on the S side
        * ToTransformerEnd: mRID of the AutoTransformerEnd on the L side
        * FromTransformerLug: mRID of the S lug
        * ToTransformerLug: mRID of the SL lug
        * AutoTransformerLug: mRID of the L lug, the tap
        * baseS: base power for pu impedances, float in VA or Qty('kVA')
        * baseU: coil voltage S to SL, float in V or Qty('kV')
        * ratedS: buck/boost rating (nameplate kVA), float in VA or Qty('kVA')
        * ratedU: coil rated voltage, float in V or Qty('kV')
        * r: coil resistance, float in ohm or Qty('ohm'|'pu'|'percent') on baseU/baseS
        * rDC: coil DC resistance, float in ohm or Qty('ohm'|'pu'|'percent') on baseU/baseS
        """
        constr: CONSTR = self.cim  # type:ignore
        winding = constr.TransformerWinding(mRID=f"{regulator.mRID}_wdg")
        associations = {
            "FromTransformerEnd": (constr.TransformerEnd, FromTransformerEnd),
            "ToTransformerEnd": (constr.TransformerEnd, ToTransformerEnd),
            "FromTransformerLug": (constr.TransformerLug, FromTransformerLug),
            "ToTransformerLug": (constr.TransformerLug, ToTransformerLug),
            "AutoTransformerLug": (constr.TransformerLug, AutoTransformerLug),
        }
        for association_name, (target_class, target_mRID) in associations.items():
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=winding,
                profile_part=CONSTR,
                association_name=association_name,
                target_class=target_class,
                target_mRID=target_mRID,
            )
        graph_write.set_assc(regulator, CN, "AutoTransformerWinding", winding)
        # ratings first: a pu/percent r or rDC converts against baseU/baseS
        graph_write.set_attr(winding, EL_UNBAL, "baseS", baseS)
        graph_write.set_attr(winding, EL_UNBAL, "baseU", baseU)
        graph_write.set_attr(winding, EL_UNBAL, "ratedS", ratedS)
        graph_write.set_attr(winding, EL_UNBAL, "ratedU", ratedU)
        graph_write.set_attr(winding, EL_UNBAL, "r", r)
        graph_write.set_attr(winding, EL_UNBAL, "rDC", rDC)
        graph_write.add_to_graph(self.network, winding)
        return regulator, winding
