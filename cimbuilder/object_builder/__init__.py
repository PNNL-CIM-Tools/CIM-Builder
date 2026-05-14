# from cimbuilder.object_builder.new_base_voltage import new_base_voltage as new_base_voltage
from typing import TypeVar
from cimbuilder.object_builder.switch.new_breaker import new_breaker as new_breaker
from cimbuilder.object_builder.switch.new_disconnector import new_disconnector as new_disconnector
from cimbuilder.object_builder.switch.new_fuse import new_fuse as new_fuse
from cimbuilder.object_builder.switch.new_load_break_switch import new_load_break_switch as new_load_break_switch
from cimbuilder.object_builder.topology.new_bus_bar_section import new_bus_bar_section as new_bus_bar_section
from cimbuilder.object_builder.transformer.new_power_transformer import new_power_transformer as new_power_transformer

from cimbuilder.object_builder.generic.new_one_terminal_object import new_one_terminal_object as new_one_terminal_object
from cimbuilder.object_builder.generic.new_two_terminal_object import new_two_terminal_object as new_two_terminal_object

from cimbuilder.object_builder.measurement.new_analog import new_analog as new_analog
from cimbuilder.object_builder.measurement.new_analog import create_all_analog as create_all_analog
from cimbuilder.object_builder.measurement.new_discrete import new_discrete as new_discrete

# from cimbuilder.object_builder.new_capacitor import new_capacitor as new_capacitor 
# from cimbuilder.object_builder.generator.new_synchronous_generator import new_synchronous_generator as new_synchronous_generator
# from cimbuilder.object_builder.new_transmission_line import new_transmission_line as new_transmission_line
# from cimbuilder.object_builder.transformer.new_tap_changer import new_tap_changer as new_tap_changer


# import inspect
# T = TypeVar['T', cimtype]

# class ObjectBuilder:
#     def __init__(self, *, graph: GraphModel):
#         self._graph_model=  graph

#     def create(self, *, type: cim.datatype: T, **kwargs) -> T: 
#         signature = inspect.signature(new_breaker)


# graph = GraphModel()
# obj = ObjectBuilder(graph)
# obj = ObjectBuilder(graph=graph)




