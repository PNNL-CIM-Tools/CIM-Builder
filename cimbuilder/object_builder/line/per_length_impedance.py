import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.short_circuit as SC

from cimbuilder.object_builder.object_builder import ObjectBuilder
from cimtables import graph_write


class PerLengthSequenceImpedanceBuilder(ObjectBuilder):
    """
    Builder for positive sequence impedances per unit length
    (equivalent to specifying r/x/b on line in OpenDSS)
    """
    
    cim_class_name = 'PerLengthSequenceImpedance'

    def add_electrical(self, impedance, *, r=None, x=None, bch=None, gch=None,
                    calculatedFrequency=None, calculatedTemperature, rg=None, xg=None) -> None:
        """
        Positive-sequence per-length impedance. Per-unit not supported for these attributes
        * r: positive sequence resistance, float in ohm/m or Qty('ohm/length')
        * x: positive sequence reactance, float in ohm/m or Qty('ohm/length')
        * bch: positive sequence shunt susceptance, float in siemens/m or Qty('siemens/length')
        * gch: positive sequence shunt conductance, float in siemens/m or Qty('siemens/length')
        """
        graph_write.set_attr(impedance, EL_BAL, 'r', r)
        graph_write.set_attr(impedance, EL_BAL, 'x', x)
        graph_write.set_attr(impedance, EL_BAL, 'bch', bch)
        graph_write.set_attr(impedance, EL_BAL, 'gch', gch)

        
    def add_short_circuit(self, impedance, *, r0=None, x0=None, b0ch=None, g0ch=None) -> None:
        """
        Adds zero-sequence short-circuit impedances to the line
        * r0: zero sequence resistance, float in ohm/m or Qty('ohm/length')
        * x0: zero sequence reactance, float in ohm/m or Qty('ohm/length')
        * b0ch: zero sequence shunt susceptance, float in siemens/m or Qty('S/length')
        * g0ch: zero sequence shunt conductance, float in siemens/m or Qty('S/length')
        """
        graph_write.set_attr(impedance, SC, 'r0', r0)
        graph_write.set_attr(impedance, SC, 'x0', x0)
        graph_write.set_attr(impedance, SC, 'b0ch', b0ch)
        graph_write.set_attr(impedance, SC, 'g0ch', g0ch)
            
    def add_electrical_earthing(self, impedance, *, calculatedFrequency=None, 
                                calculatedTemperature=None, rg=None, xg=None) -> None:
        """
        Add earth resistance and base temperature / frequency
        * calculatedFrequency: frequency at which r/x/bch/gch were calculated, float or Qty('Hz')
        * calculatedTemperature at which r/x/bch/gch were calculated, float or Qty('degC')
        * rg: earth return resistance, float in ohm or Qty('ohm'|'pu')
        * xg: earth return reactance, float in ohm or Qty('ohm'|'pu')
        """
        graph_write.set_attr(impedance, EL_BAL, 'calculatedFrequency', calculatedFrequency)
        graph_write.set_attr(impedance, EL_BAL, 'calculatedTemperature', calculatedTemperature)
        graph_write.set_attr(impedance, EL_BAL, 'rg', rg)
        graph_write.set_attr(impedance, EL_BAL, 'xg', xg)
        
    def add_wire_configuration(self, impedance, *, WireConfiguration: str) -> object:
            """
            Associates the sequence impedances with an existing WireConfiguration template
            * WireConfiguration: mRID string of the target WireConfiguration
            """
            target = graph_write.set_assc_from_mrid(
                self.network, impedance, EL_BAL, 'WireConfiguration', self.cim.WireConfiguration, WireConfiguration)
            return target

class PerLengthPhaseImpedanceBuilder(ObjectBuilder):
    """
    Builder for lower-triangular line impedance per length matrix
    (equivalent to OpenDSS linecode)
    """
    cim_class_name = 'PerLengthPhaseImpedance'

    def add_phase_impedance_data_row(self, matrix, row, column, r, x, b, g, fromPhase, toPhase):
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

        data = self.cim.PhaseImpedanceData() # no mRID on this class
        data.uuid(mRID=f"{matrix.mRID}_{row}_{column}")
        graph_write.set_attr(data, EL_UNBAL, 'row', row)
        graph_write.set_attr(data, EL_UNBAL, 'column', column)
        graph_write.set_attr(data, EL_UNBAL, 'r', r)
        graph_write.set_attr(data, EL_UNBAL, 'x', x)
        graph_write.set_attr(data, EL_UNBAL, 'b', b)
        graph_write.set_attr(data, EL_UNBAL, 'g', g)
        graph_write.set_attr(data, EL_UNBAL, 'fromPhase', fromPhase)
        graph_write.set_attr(data, EL_UNBAL, 'toPhase', toPhase)
        graph_write.set_assc(data, EL_UNBAL, 'PhaseImpedance', matrix)
        graph_write.add_to_graph(self.network, data)


    def add_electrical_earthing(self, matrix, *, conductorCount: int | None = None,
                    calculatedFrequency=None, rg=None, xg=None) -> None:
        """
        * conductorCount: plain int, no unit wrapping.
        * calculatedFrequency: a Qty resolved to Frequency (Hz, SI base).
        * rg/xg: Qtys resolved to ResistancePerLength/ReactancePerLength
          (ohm/m, SI base) - ground return path values, inherited
          PerLengthImpedance base-class fields.
        A bare number for calculatedFrequency/rg/xg is read as SI base (wrapped in its CIMUnit).
        """
        graph_write.set_attr(matrix, EL_UNBAL, 'conductorCount', conductorCount)
        graph_write.set_attr(matrix, EL_UNBAL, 'calculatedFrequency', calculatedFrequency)
        graph_write.set_attr(matrix, EL_UNBAL, 'rg', rg)
        graph_write.set_attr(matrix, EL_UNBAL, 'xg', xg)
