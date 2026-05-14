"""Switch-family primitives: Breaker, Disconnector, LoadBreakSwitch, Fuse."""
from cimbuilder.object_builder.switch.new_breaker import new_breaker
from cimbuilder.object_builder.switch.new_disconnector import new_disconnector
from cimbuilder.object_builder.switch.new_fuse import new_fuse
from cimbuilder.object_builder.switch.new_load_break_switch import new_load_break_switch

__all__ = [
    "new_breaker",
    "new_disconnector",
    "new_fuse",
    "new_load_break_switch",
]
