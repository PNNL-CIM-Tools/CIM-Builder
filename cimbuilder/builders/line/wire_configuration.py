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
            target = graph_write.resolve_any_subclass(self.network, self.cim.WireSpacing, WireSpacing)
            if target is None:
                raise ValueError(
                    f"{config.name!r}: WireSpacing {WireSpacing!r} not found in graph "
                    f"(build the spacing before the WireConfiguration that references it)"
                )
            graph_write.set_assc(config, CONST, 'WireSpacing', target)

