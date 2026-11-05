"""Generic one/two-terminal object constructors (pre-ObjectBuilder-pattern helpers)."""
from cimbuilder.object_builder.generic.new_one_terminal_obj import new_one_terminal_object
from cimbuilder.object_builder.generic.new_two_terminal_obj import new_two_terminal_object

__all__ = [
    "new_one_terminal_object",
    "new_two_terminal_object",
]
