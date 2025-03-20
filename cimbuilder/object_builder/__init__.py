# from cimbuilder.object_builder.new_base_voltage import new_base_voltage as new_base_voltage
from typing import TypeVar
from cimbuilder.object_builder.breaker import new_breaker as new_breaker
from cimbuilder.object_builder.disconnector import new_disconnector as new_disconnector
from cimbuilder.object_builder.bus_bar_section import new_bus_bar_section as new_bus_bar_section
from cimbuilder.object_builder.power_transformer import new_power_transformer as new_power_transformer

from cimbuilder.object_builder.one_terminal_obj import new_one_terminal_object as new_one_terminal_object
from cimbuilder.object_builder.two_terminal_obj import new_two_terminal_object as new_two_terminal_object

from cimbuilder.object_builder.analog import new_analog as new_analog
from cimbuilder.object_builder.analog import create_all_analog as create_all_analog
from cimbuilder.object_builder.discrete import new_discrete as new_discrete

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




