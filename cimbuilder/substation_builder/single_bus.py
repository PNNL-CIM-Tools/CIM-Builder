from dataclasses import dataclass, field

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typing import

import cimbuilder.object_builder as object_builder
import cimbuilder.utils as utils

import logging
_log = logging.getLogger(__name__)

@dataclass
class SingleBusSubstation():
    connection:ConnectionInterface
    network:GraphModel = field(default=None)
    name:str = field(default='new_single_bus_sub')
    base_voltage:int|cim.BaseVoltage = field(default=115000)
    total_sections:int = field(default = 4)

    def __post_init__(self):
        self.total_sections = int(self.total_sections)
        self.cim = utils.get_cim_profile(self.connection) # Import CIM profile

        # Create new substation class
        self.substation = self.cim.Substation(mRID = utils.new_mrid(), name=self.name)
        
        # If no network defined, create substation as a DistributedArea
        if not self.network:
            self.network = DistributedArea(connection=self.connection, container=self.substation, distributed=False)
        self.network.add_to_graph(self.substation)
        
        # If base voltage not defined, create a new BaseVoltage object
        self.base_voltage = utils.get_base_voltage(self.network, self.base_voltage)
        
        # main bus
        self.main_bus = self.cim.ConnectivityNode(name=f'{self.name}_main_bus', mRID=utils.new_mrid())
        self.main_bus.ConnectivityNodeContainer = self.substation
        self.network.add_to_graph(self.main_bus)
        object_builder.new_bus_bar_section(self.network, self.main_bus)
       
        return self.network
    
    def new_branch(self, series_number:int, branch_equipment:cim.ConductingEquipment, branch_terminal:cim.Terminal|int) -> None:

        junction1 = cim.ConnectivityNode(name=f'{self.substation.name}_{series_number}_j1', mRID = utils.new_mrid(), ConnectivityNodeContainer=self.substation)
        
        breaker = object_builder.new_breaker(self.network, self.substation, name = f"{self.substation.name}_{series_number}", node1 = self.main_bus, node2 = junction1)
        
        breaker.BaseVoltage = self.base_voltage

        if type(branch_terminal) == cim.Terminal:
                branch_terminal.ConnectivityNode = junction1
    
        
        self.network.add_to_graph(junction1)

    def new_feeder(self, series_number:int, feeder_network:GraphModel, feeder:cim.Feeder, 
                                sourcebus:cim.ConnectivityNode=None) -> None:
            
        feeder_network.get_all_edges(cim.Feeder)

        # If sourcebus of feeder not specified, look for something named sourcebus
        if not sourcebus: 
            found = False
            feeder_network.get_all_edges(cim.EnergySource)
            feeder_network.get_all_edges(cim.Terminal)
            feeder_network.get_all_edges(cim.ConnectivityNode)
            for source in feeder_network.graph[cim.EnergySource].values():
                if source.Terminals[0].ConnectivityNode.name == 'sourcebus':
                    sourcebus = source.Terminals[0].ConnectivityNode
                    found = True
            if not found:
                _log.error(f'Could not find sourcebus for {feeder.name}')

        junction1 = cim.ConnectivityNode(name=f'{self.substation.name}_{series_number}_j1', mRID = utils.new_mrid(), ConnectivityNodeContainer=self.substation)
        junction2 = cim.ConnectivityNode(name=f'{self.substation.name}_{series_number}_j2', mRID = utils.new_mrid(), ConnectivityNodeContainer=self.substation)
        # junction3 = cim.ConnectivityNode(name=f'{substation.name}_{series_number}_j3', mRID = new_mrid(), ConnectivityNodeContainer=substation)

        breaker = object_builder.new_breaker(self.network, self.substation, name = f'{self.substation.name}_{series_number}', node1 = junction1, node2 = junction2)
        airgap1 = object_builder.new_disconnector(self.network, self.substation, name = f'{self.substation.name}_{series_number+1}', node1 = self.main_bus, node2 = junction1)
        airgap2 = object_builder.new_disconnector(self.network, self.substation, name = f'{self.substation.name}_{series_number+2}', node1 = junction2, node2 = sourcebus)
        
        breaker.BaseVoltage = self.base_voltage
        airgap1.BaseVoltage = self.base_voltage
        airgap2.BaseVoltage = self.base_voltage
        feeder.NormalEnergizingSubstation = self.substation
        sourcebus.AdditionalEquipmentContainer = self.substation
        self.substation.NormalEnergizedFeeder.append(feeder)


        # feeder_network.add_to_graph(self.substation)
        self.network.add_to_graph(junction1)
        self.network.add_to_graph(junction2)
        self.network.add_to_graph(sourcebus)
        self.network.add_to_graph(feeder)
    