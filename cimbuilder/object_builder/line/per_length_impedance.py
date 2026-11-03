import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.short_circuit as SC
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class PerLengthSequenceImpedanceBuilder(ObjectBuilder):
    """
    Builder for positive sequence impedances per unit length
    (equivalent to specifying r/x/b on line in OpenDSS)
    """

    cim_class_name = "PerLengthSequenceImpedance"

    def add_electrical(
        self,
        impedance: EL_BAL.PerLengthSequenceImpedance,
        *,
        r: float | Qty | None = None,
        x: float | Qty | None = None,
        bch: float | Qty | None = None,
        gch: float | Qty | None = None,
        isTemplate: bool | None = None,
        calculatedFrequency: float | Qty | None = None,
        calculatedTemperature: float | Qty | None,
    ) -> EL_BAL.PerLengthSequenceImpedance:
        """
        Positive-sequence per-length impedance. Per-unit not supported for these attributes
        * r: positive sequence resistance, float in ohm/m or Qty('ohm/length')
        * x: positive sequence reactance, float in ohm/m or Qty('ohm/length')
        * bch: positive sequence shunt susceptance, float in siemens/m or Qty('siemens/length')
        * gch: positive sequence shunt conductance, float in siemens/m or Qty('siemens/length')
        * isTemplate: denotes if used as part of a LineCode or other template
        * calculatedFrequency: frequency at which r/x/bch/gch were calculated, float or Qty('Hz')
        * calculatedTemperature at which r/x/bch/gch were calculated, float or Qty('degC')
        """
        graph_write.set_attr(impedance, EL_BAL, "r", r)
        graph_write.set_attr(impedance, EL_BAL, "x", x)
        graph_write.set_attr(impedance, EL_BAL, "bch", bch)
        graph_write.set_attr(impedance, EL_BAL, "gch", gch)
        graph_write.set_attr(impedance, EL_BAL, "isTemplate", isTemplate)
        graph_write.set_attr(
            impedance, EL_BAL, "calculatedFrequency", calculatedFrequency
        )
        graph_write.set_attr(
            impedance, EL_BAL, "calculatedTemperature", calculatedTemperature
        )
        return impedance

    def add_short_circuit(
        self,
        impedance: EL_BAL.PerLengthSequenceImpedance,
        *,
        r0: float | Qty | None = None,
        x0: float | Qty | None = None,
        b0ch: float | Qty | None = None,
        g0ch: float | Qty | None = None,
    ) -> EL_BAL.PerLengthSequenceImpedance:
        """
        Adds zero-sequence short-circuit impedances to the line
        * r0: zero sequence resistance, float in ohm/m or Qty('ohm/length')
        * x0: zero sequence reactance, float in ohm/m or Qty('ohm/length')
        * b0ch: zero sequence shunt susceptance, float in siemens/m or Qty('S/length')
        * g0ch: zero sequence shunt conductance, float in siemens/m or Qty('S/length')
        """
        graph_write.set_attr(impedance, SC, "r0", r0)
        graph_write.set_attr(impedance, SC, "x0", x0)
        graph_write.set_attr(impedance, SC, "b0ch", b0ch)
        graph_write.set_attr(impedance, SC, "g0ch", g0ch)
        return impedance

    def add_electrical_earthing(
        self,
        impedance: EL_BAL.PerLengthSequenceImpedance,
        *,
        rg: float | Qty | None = None,
        xg: float | Qty | None = None,
    ) -> EL_BAL.PerLengthSequenceImpedance:
        """
        Add earth resistance and base temperature / frequency
        * rg: earth return resistance, float in ohm or Qty('ohm'|'pu')
        * xg: earth return reactance, float in ohm or Qty('ohm'|'pu')
        """

        graph_write.set_attr(impedance, EL_BAL, "rg", rg)
        graph_write.set_attr(impedance, EL_BAL, "xg", xg)
        return impedance

    def add_wire_configuration(
        self, impedance: EL_BAL.PerLengthSequenceImpedance, *, WireConfiguration: str
    ) -> EL_BAL.PerLengthSequenceImpedance:
        """
        Associates the sequence impedances with an existing WireConfiguration template
        * WireConfiguration: mRID string of the target WireConfiguration
        """
        el_bal: EL_BAL = self.cim  # type: ignore
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=impedance,
            profile_part=EL_BAL,
            association_name="WireConfiguration",
            target_class=el_bal.WireConfiguration,
            target_mRID=WireConfiguration,
        )
        return impedance


class PerLengthPhaseImpedanceBuilder(ObjectBuilder):
    """
    Builder for lower-triangular line impedance per length matrix
    """

    cim_class_name = "PerLengthPhaseImpedance"

    def add_electrical(
        self,
        matrix: EL_UNBAL.PerLengthPhaseImpedance,
        *,
        conductorCount: int | None = None,
        isTemplate: bool | None = None,
        calculatedFrequency: float | Qty | None = None,
        calculatedTemperature: float | Qty | None,
    ) -> EL_UNBAL.PerLengthPhaseImpedance:
        """
        * isTemplate: denotes if used as part of a LineCode or other template
        * calculatedFrequency: frequency at which r/x/bch/gch were calculated, float or Qty('Hz')
        * calculatedTemperature at which r/x/bch/gch were calculated, float or Qty('degC')
        """

        graph_write.set_attr(matrix, EL_UNBAL, "conductorCount", conductorCount)
        graph_write.set_attr(matrix, EL_UNBAL, "isTemplate", isTemplate)
        graph_write.set_attr(
            matrix, EL_UNBAL, "calculatedFrequency", calculatedFrequency
        )
        graph_write.set_attr(
            matrix, EL_UNBAL, "calculatedTemperature", calculatedTemperature
        )
        return matrix

    def add_phase_impedance_data_row(
        self,
        matrix: EL_UNBAL.PerLengthPhaseImpedance,
        *,
        row: int,
        column: int,
        r: float | Qty | None,
        x: float | Qty | None,
        b: float | Qty | None,
        g: float | Qty | None,
        fromPhase: str,
        toPhase: str,
    ) -> tuple[EL_UNBAL.PerLengthPhaseImpedance, EL_UNBAL.PhaseImpedanceData]:
        """
        Adds a single row of lower triangular phase impedance matrix
        * row: integer, matrix row index
        * column: integer, matrix column index
        * r: resistance, float in ohm/m or Qty('ohm/length')
        * x: reactance, float in ohm/m or Qty('ohm/length')
        * bch: shunt susceptance, float in siemens/m or Qty('S/length')
        * gch: shunt conductance, float in siemens/m or Qty('S/length')
        * fromPhase: single phase letter for "from" phase
        * toPhase: single phase letter for "to" phase
        """

        data = self.cim.PhaseImpedanceData()  # no mRID on this class
        data.uuid(mRID=f"{matrix.mRID}_{row}_{column}")
        graph_write.set_attr(data, EL_UNBAL, "row", row)
        graph_write.set_attr(data, EL_UNBAL, "column", column)
        graph_write.set_attr(data, EL_UNBAL, "r", r)
        graph_write.set_attr(data, EL_UNBAL, "x", x)
        graph_write.set_attr(data, EL_UNBAL, "b", b)
        graph_write.set_attr(data, EL_UNBAL, "g", g)
        graph_write.set_attr(data, EL_UNBAL, "fromPhase", fromPhase)
        graph_write.set_attr(data, EL_UNBAL, "toPhase", toPhase)
        graph_write.set_assc(data, EL_UNBAL, "PhaseImpedance", matrix)
        graph_write.add_to_graph(self.network, data)
        return matrix, data

    def add_electrical_earthing(
        self,
        matrix: EL_UNBAL.PerLengthPhaseImpedance,
        *,
        rg: float | Qty | None = None,
        xg: float | Qty | None = None,
    ) -> None:
        """
        Adds eart
        """

        graph_write.set_attr(matrix, EL_UNBAL, "rg", rg)
        graph_write.set_attr(matrix, EL_UNBAL, "xg", xg)
