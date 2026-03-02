from __future__ import annotations
from dataclasses import dataclass, field
from typing import Type

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface, get_cim_profile
import cimgraph.data_profile.cimhub_2023 as cim 

from cimbuilder.substation_builder.substation_builder import SubstationBuilder
import cimbuilder.object_builder as object_builder
import cimbuilder.utils as utils
import logging
_log = logging.getLogger(__name__)

@dataclass
class SingleBusSubstation(SubstationBuilder):
    name:str = field(default='new_single_bus_sub')
    base_voltage:int|cim.BaseVoltage = field(default=115000)
    total_sections:int = field(default = 4)

    def __post_init__(self):                                    
        self.total_sections = int(self.total_sections)
        cim_profile, cim_module = get_cim_profile()
        self.cim : cim = cim_module
        # Create new substation class
        self.substation = self.cim.Substation(name=self.name)
        
        # If no network defined, create substation as a DistributedArea
        if not self.network:
            self.network = DistributedArea(connection=self.connection, container=self.substation)
        self.network.add_to_graph(self.substation)
        
        # If base voltage not defined, create a new BaseVoltage object
        self.base_voltage = utils.get_base_voltage(self.network, self.base_voltage)
        
        # main bus
        self.main_bus = self.cim.ConnectivityNode(name=f'{self.name}_main_bus')
        self.main_bus.ConnectivityNodeContainer = self.substation
        self.network.add_to_graph(self.main_bus)
        object_builder.new_bus_bar_section(self.network, self.main_bus)
       
        return self.network
    
    def new_branch(self, breaker_number:int, branch_equipment:cim.ConductingEquipment,
                    branch_terminal:cim.Terminal|int) -> None:

        junction1 = self.cim.ConnectivityNode(name=f'{self.substation.name}_{breaker_number}_j1',
                                            ConnectivityNodeContainer=self.substation)
        
        breaker = object_builder.new_breaker(self.network, self.substation, name = f"{self.substation.name}_{breaker_number}",
                                            node1 = self.main_bus, node2 = junction1)
        
        breaker.BaseVoltage = self.base_voltage

        if type(branch_terminal) == cim.Terminal:
                branch_terminal.ConnectivityNode = junction1
    
        
        self.network.add_to_graph(junction1)

    def new_feeder(self, breaker_number:int, feeder_network:GraphModel, feeder:cim.Feeder, 
                                sourcebus:cim.ConnectivityNode=None) -> None:
            
        feeder_network.get_all_edges(self.cim.Feeder)

        # If sourcebus of feeder not specified, look for something named sourcebus
        if not sourcebus: 
            found = False
            feeder_network.get_all_edges(self.cim.EnergySource)
            feeder_network.get_all_edges(self.cim.Terminal)
            feeder_network.get_all_edges(self.cim.ConnectivityNode)
            source = feeder_network.list_by_class(self.cim.EnergySource)[0]
                # if source.Terminals[0].ConnectivityNode.name == 'sourcebus':
            sourcebus:cim.ConnectivityNode = source.Terminals[0].ConnectivityNode
            # found = True
            # if not found:
            #     _log.error(f'Could not find sourcebus for {feeder.name}')

        junction1 = cim.ConnectivityNode(name=f'{self.substation.name}_{breaker_number}_j1',
                                        ConnectivityNodeContainer=self.substation)
        junction2 = cim.ConnectivityNode(name=f'{self.substation.name}_{breaker_number}_j2',
                                        ConnectivityNodeContainer=self.substation)

        breaker = object_builder.new_breaker(self.network, container=self.substation,
                                            name = f'{self.substation.name}_{breaker_number}',
                                            node1 = junction1, node2 = junction2)
        airgap1 = object_builder.new_disconnector(self.network, container=self.substation,
                                                name = f'{self.substation.name}_{breaker_number+1}',
                                                node1 = self.main_bus, node2 = junction1)
        airgap2 = object_builder.new_disconnector(self.network, container=self.substation,
                                                name = f'{self.substation.name}_{breaker_number+2}',
                                                node1 = junction2, node2 = sourcebus)
        
        breaker.BaseVoltage = self.base_voltage
        airgap1.BaseVoltage = self.base_voltage
        airgap2.BaseVoltage = self.base_voltage
        feeder.NormalEnergizingSubstation = self.substation
        self.substation.NormalEnergizedFeeder.append(feeder)


        # feeder_network.add_to_graph(self.substation)
        self.network.add_to_graph(junction1)
        self.network.add_to_graph(junction2)
        self.network.add_to_graph(sourcebus)
        self.network.add_to_graph(feeder)
    