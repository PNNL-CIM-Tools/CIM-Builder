"""Line builders: ACLineSegmentBuilder (the instance tier - base.py) and the
reusable template tier (by_template.py) - PerLengthSequenceImpedanceBuilder /
PerLengthPhaseImpedanceBuilder (per-length impedance templates) and
WireConfigurationBuilder / ConductorDistanceSpacingBuilder / XYSpacingBuilder
(wire geometry templates). See base.py's module docstring for the five
coexisting line-impedance/geometry representations each supports."""

from cimbuilder.builders.line.base import ACLineSegmentBuilder
from cimbuilder.builders.line.by_template import (
    ConductorDistanceSpacingBuilder,
    PerLengthPhaseImpedanceBuilder,
    PerLengthSequenceImpedanceBuilder,
    WireConfigurationBuilder,
    XYSpacingBuilder,
)

__all__ = [
    'ACLineSegmentBuilder',
    'ConductorDistanceSpacingBuilder',
    'PerLengthPhaseImpedanceBuilder',
    'PerLengthSequenceImpedanceBuilder',
    'WireConfigurationBuilder',
    'XYSpacingBuilder',
]
