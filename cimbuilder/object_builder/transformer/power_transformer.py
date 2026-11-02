import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.short_circuit as SC
from cimtables import connectivity, graph_write, impedance
from cimtables.units import Qty

from cimbuilder.object_builder.object_builder import ObjectBuilder


class PowerTransformerBuilder(ObjectBuilder):
    cim_class_name = "PowerTransformer"

    def add_connectivity(
        self, xfmr: CN.PowerTransformer, *, EquipmentContainer: str | None = None
    ) -> CN.PowerTransformer:
        """
        Adds base connectivity layer of equipment containment. Add nodes using add_power_transformer_end
        * EquipmentContainer: mRID of the Substation or Feeder containing the line.
        note: do NOT set BaseVoltage. It is set for each end individually
        """
        cn: CN = self.cim  # type: ignore
        if EquipmentContainer is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=xfmr,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=EquipmentContainer,
            )
        else:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=xfmr,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=self.container.mRID,
            )
        return xfmr

    def add_power_transformer_end(
        self,
        xfmr: CN.PowerTransformer,
        *,
        node: str,
        endNumber: int,
        connectionKind: str | None = None,
        BaseVoltage: str,
    ) -> tuple[CN.PowerTransformer, CN.Terminal, CN.PowerTransformerEnd]:
        """
        Adds base connectivity layer of terminals, base voltage, etc
        * node: mRID of the ConnectivityNode or TopologicalNode for this end
        * endNumber: highest voltage winding is end #1
        * connectionKind: wye/delta connection, Y|Yn|oY|D|Dn|oD|Z|I|A|T
        * BaseVoltage: mRID string of the BaseVoltage
        """

        cn: CN = self.cim  # type:ignore

        xfmr_end = cn.PowerTransformerEnd(name=f"{xfmr.mRID}_end_{endNumber}")

        terminals = connectivity.add_connectivity(
            network=self.network,
            equipment=xfmr_end,
            node_cols={"node": node},
            equipment_container=None,
        )
        graph_write.set_attr(xfmr_end, CN, "endNumber", endNumber)
        graph_write.set_attr(xfmr_end, CN, "connectionKind", connectionKind)
        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=xfmr_end,
                profile_part=CN,
                association_name="BaseVoltage",
                target_class=cn.BaseVoltage,
                target_mRID=BaseVoltage,
            )

        return xfmr, terminals[0], xfmr_end

    def add_electrical(
        self,
        xfmr_end: EL_BAL.PowerTransformerEnd,
        *,
        r: float | Qty | None = None,
        x: float | Qty | None = None,
        b: float | Qty | None = None,
        g: float | Qty | None = None,
        ratedS: float | Qty,
        ratedU: float | Qty,
        base_code_key: int = 3,
    ) -> None:
        """
        Adds star model positive sequence balanced impedance.
        For 2-winding transformer, all impedance on end with endNumber=1, no impedance on endNumber=2
        For 3-winding transformer, star impedance on each end, b and g preferred on end with endNumber=1
        For transformers with more than 3 ends, r and x should be pairwise mesh, with b and g specfied per end
        * r: positive sequence resistance, float in ohm or Qty('ohm'|'pu'|'percent')
        * x: positive sequence reactance, float in ohm or Qty('ohm'|'pu'|'percent')
        * b: positive sequence shunt susceptance, float in siemens or Qty('S'|'pu'|'percent')
        * g: positive sequence shunt conductance, float in siemens or Qty('S'|'pu'|'percent')
        * ratedS: normal apparent power rating of this winding, float in VA or Qty('kVA'|'MVA')
        * ratedU: phase-to-phase rated voltage at no load, float in V or Qty('kV')
        * base_code_key: 1 = winding MVA base, 2 = system MVA base, 3 = ohms, matches PSSE RAW CW
        """

        relative = any(isinstance(v, Qty) and v.is_relative() for v in (r, x, b, g))
        if base_code_key == 1:
            z_base = impedance.z_base(xfmr_end, [], ratedS)
        elif base_code_key == 2:
            z_base = impedance.z_base(xfmr_end, [], self.network.base_power)
        elif base_code_key == 3 and relative:
            raise ValueError("base_code_key of 3 for ohms but r,x,b,g were in per-unit")
        else:
            raise ValueError(
                "base_code_key must be one of: 1 = winding MVA base, 2 = system MVA base, 3 = ohms"
            )

        graph_write.set_attr(xfmr_end, EL_BAL, "r", r, z_base=z_base)
        graph_write.set_attr(xfmr_end, EL_BAL, "x", x, z_base=z_base)
        graph_write.set_attr(xfmr_end, EL_BAL, "b", b, z_base=z_base)
        graph_write.set_attr(xfmr_end, EL_BAL, "g", g, z_base=z_base)
        graph_write.set_attr(xfmr_end, EL_BAL, "ratedS", ratedS)
        graph_write.set_attr(xfmr_end, EL_BAL, "ratedU", ratedU)

    def add_mesh_impedance(
        self,
        xfmr,
        *,
        FromTransformerEnd: str,
        ToTransformerEnd: str,
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
        el_bal: EL_BAL = self.cim  # type:ignore
        from_end: EL_BAL.PowerTransformerEnd = graph_write.resolve(
            self.network, el_bal.PowerTransformerEnd, FromTransformerEnd
        )  # type:ignore
        to_end: EL_BAL.PowerTransformerEnd = graph_write.resolve(
            self.network, el_bal.PowerTransformerEnd, ToTransformerEnd
        )  # type:ignore
        if from_end is None or to_end is None:
            raise ValueError(
                f"{xfmr.mRID!r}: mesh impedance references "
                f"{FromTransformerEnd!r}/{ToTransformerEnd!r}, not both found in graph"
            )
        mesh = el_bal.TransformerMeshImpedance(
            mRID=f"{xfmr.mRID}_mesh_end_{from_end.endNumber}_{from_end.endNumber}" #type:ignore
        )
        graph_write.set_assc(mesh, EL_BAL, "FromTransformerEnd", from_end)
        graph_write.set_assc(mesh, EL_BAL, "ToTransformerEnd", to_end)

        relative = any(isinstance(v, Qty) and v.is_relative() for v in (r, x))
        z_base = (
            impedance.z_base(mesh, [from_end], from_end.ratedS) if relative else None
        )
        graph_write.set_attr(mesh, EL_BAL, "r", r, z_base=z_base)
        graph_write.set_attr(mesh, EL_BAL, "x", x, z_base=z_base)
        graph_write.add_to_graph(self.network, mesh)
        return xfmr, mesh

    def add_short_circuit(
        self,
        xfmr_end: SC.PowerTransformerEnd,
        *,
        r0: float | Qty | None = None,
        x0: float | Qty | None = None,
        b0: float | Qty | None = None,
        g0: float | Qty | None = None,
        base_code_key: int = 3,
    ) -> None:
        """
        Adds star model positive sequence balanced impedance.
        For 2-winding transformer, all impedance on end with endNumber=1, no impedance on endNumber=2
        For 3-winding transformer, star impedance on each end, b and g preferred on end with endNumber=1
        For transformers with more than 3 ends, r and x should be pairwise mesh, with b and g specfied per end
        * r0: zero sequence resistance, float in ohm or Qty('ohm'|'pu'|'percent')
        * x0: zero sequence reactance, float in ohm or Qty('ohm'|'pu'|'percent')
        * b0: zero sequence shunt susceptance, float in siemens or Qty('S'|'pu'|'percent')
        * g0: zero sequence shunt conductance, float in siemens or Qty('S'|'pu'|'percent')
        * base_code_key: 1 = winding MVA base, 2 = system MVA base, 3 = ohms, matches PSSE RAW CW
        """

        relative = any(isinstance(v, Qty) and v.is_relative() for v in (r0, x0, b0, g0))
        if base_code_key == 1:
            z_base = impedance.z_base(xfmr_end, [], xfmr_end.ratedS)  # type:ignore
        elif base_code_key == 2:
            z_base = impedance.z_base(xfmr_end, [], self.network.base_power)
        elif base_code_key == 3 and relative:
            raise ValueError("base_code_key of 3 for ohms but r,x,b,g were in per-unit")
        else:
            raise ValueError(
                "base_code_key must be one of: 1 = winding MVA base, 2 = system MVA base, 3 = ohms"
            )

        graph_write.set_attr(xfmr_end, EL_BAL, "r", r0, z_base=z_base)
        graph_write.set_attr(xfmr_end, EL_BAL, "x", x0, z_base=z_base)
        graph_write.set_attr(xfmr_end, EL_BAL, "b", b0, z_base=z_base)
        graph_write.set_attr(xfmr_end, EL_BAL, "g", g0, z_base=z_base)
