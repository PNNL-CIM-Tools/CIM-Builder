import cimprofiles.cim18.cim18v17.construction as CONST

from cimbuilder.builders.base import ObjectBuilder
from cimtables import graph_write

class WireConfigurationBuilder(ObjectBuilder):
    """
    """

    cim_class_name = 'WireConfiguration'

    def add_config_template(self, config, *, numberOfPhases: int | None = None, installationType=None,
                    usage=None, WireSpacing: str | None = None) -> None:
        graph_write.set_attr(config, CONST, 'numberOfPhases', numberOfPhases)
        if installationType is not None:
            graph_write.set_attr(config, CONST, 'installationType', self.cim.WireInstallationKind(installationType))
        if usage is not None:
            graph_write.set_attr(config, CONST, 'usage', self.cim.WireUsageKind(usage))
        
    def add_construction(self, config, WireSpacing: str | None = None) -> None:
        if WireSpacing is not None:
            graph_write.set_assc_from_mrid(
                self.network, config, CONST, 'WireSpacing', self.cim.WireSpacing, WireSpacing)

