import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.construction as CONST

from cimbuilder.object_builder.object_builder import ObjectBuilder
from cimtables import graph_write

class WireConfigurationBuilder(ObjectBuilder):
    """LineModel04/05's wire-geometry template container
    (construction.WireConfiguration): numberOfPhases/installationType/usage
    plus the singular WireSpacing FK to a ConductorDistanceSpacing (distance
    pairs) or XYSpacing (x/y coordinates) object, built separately via
    ConductorDistanceSpacingBuilder/XYSpacingBuilder."""

    cim_class_name = 'WireConfiguration'
    
    def add_electrical(self, config, *, PerLengthImpedance=None, EarthResistivity=None) -> None:
        """
        * PerLenghtImpedance: mRID string of a PerLengthSequenceImpedance or PerLengthPhaseImpedance
        * EarthResistivity: mRID string of the EarthResistivity of all lines using this template
        """
        el_bal:EL_UNBAL = self.cim # type: ignore
        
        if PerLengthImpedance is not None:
            graph_write.set_assc_from_mrid(self.network, config, CONST, 'PerLengthImpedance',
                el_bal.PerLengthImpedance, PerLengthImpedance)
        
        if EarthResistivity is not None:
            graph_write.set_assc_from_mrid(self.network, config, CONST, 'PerLengthImpedance',
                el_bal.EarthResistivity, EarthResistivity)
                

    def add_construction(self, config, *, numberOfPhases: int | None = None, 
                    WireSpacing: str | None = None) -> None:
        """
        * numberOfPhases: number of phases within the circuit group
        * WireSpacing: mRID string of an existing wire spacing
        """
        cn:CONST = self.cim # type: ignore
        graph_write.set_attr(config, CONST, 'numberOfPhases', numberOfPhases)
        
        if WireSpacing is not None:
            graph_write.set_assc_from_mrid(
                self.network, config, CONST, 'WireSpacing', cn.WireSpacing, WireSpacing)

