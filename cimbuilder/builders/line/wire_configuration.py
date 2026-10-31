import cimprofiles.cim18.cim18v17.construction as CONST

from cimbuilder.builders.base import ObjectBuilder
from cimtables import graph_write

class WireConfigurationBuilder(ObjectBuilder):
    """LineModel04/05's wire-geometry template container
    (construction.WireConfiguration): numberOfPhases/installationType/usage
    plus the singular WireSpacing FK to a ConductorDistanceSpacing (distance
    pairs) or XYSpacing (x/y coordinates) object, built separately via
    ConductorDistanceSpacingBuilder/XYSpacingBuilder."""

    cim_class_name = 'WireConfiguration'

    def add_config_template(self, config, *, numberOfPhases: int | None = None, installationType=None,
                    usage=None, WireSpacing: str | None = None) -> None:
        """Sets construction.WireConfiguration's own scalars.
        * numberOfPhases: plain int, no unit wrapping.
        * installationType: string value of construction.WireInstallationKind
          (e.g. 'overhead') - converted via
          `self.cim.WireInstallationKind(...)` before set_attr.
        * usage: string value of construction.WireUsageKind (e.g.
          'distribution') - converted via `self.cim.WireUsageKind(...)`.
        * WireSpacing: accepted but unused here - note this is a likely bug:
          the parameter is declared but never passed to set_assc_from_mrid
          in this method; use add_construction (below) to actually set the
          WireSpacing association.
        """
        graph_write.set_attr(config, CONST, 'numberOfPhases', numberOfPhases)
        if installationType is not None:
            graph_write.set_attr(config, CONST, 'installationType', self.cim.WireInstallationKind(installationType))
        if usage is not None:
            graph_write.set_attr(config, CONST, 'usage', self.cim.WireUsageKind(usage))

    def add_construction(self, config, WireSpacing: str | None = None) -> None:
        """Associates `config` with an existing wire-spacing object
        (construction.WireConfiguration's WireSpacing FK).
        * WireSpacing: mRID string of an existing ConductorDistanceSpacing or
          XYSpacing (built earlier). Resolved via set_assc_from_mrid, which
          raises ValueError if that mRID isn't already in the graph. Left
          unset entirely when omitted (no association write at all, not even
          to None).
        """
        if WireSpacing is not None:
            graph_write.set_assc_from_mrid(
                self.network, config, CONST, 'WireSpacing', self.cim.WireSpacing, WireSpacing)

