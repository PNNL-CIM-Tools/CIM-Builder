"""Switch builders: SwitchBuilder (base) and its subclass chain -
ProtectedSwitchBuilder(SwitchBuilder), then BreakerBuilder/RecloserBuilder/
LoadBreakSwitchBuilder(ProtectedSwitchBuilder), plus DisconnectorBuilder/
FuseBuilder(SwitchBuilder) directly. See switch.py's module docstring for the
full field-location evidence and why every leaf is a pure cim_class_name
override with no new add_* methods needed (except BreakerBuilder's own
inTransitTime)."""

from cimbuilder.builders.switch.switch import (
    DisconnectorBuilder,
    FuseBuilder,
    SwitchBuilder,
)

__all__ = [
    'BreakerBuilder',
    'DisconnectorBuilder',
    'FuseBuilder',
    'LoadBreakSwitchBuilder',
    'ProtectedSwitchBuilder',
    'RecloserBuilder',
    'SwitchBuilder',
]
