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

    def add_construction(self, config, *, numberOfPhases: int | None = None, 
                    WireSpacing: str | None = None) -> None:
        """
        * numberOfPhases: plain int, no unit wrapping.

        * WireSpacing: mRID string of an existing wire spacing
        """
        graph_write.set_attr(config, CONST, 'numberOfPhases', numberOfPhases)
        
        if WireSpacing is not None:
            graph_write.set_assc_from_mrid(
                self.network, config, CONST, 'WireSpacing', self.cim.WireSpacing, WireSpacing)

