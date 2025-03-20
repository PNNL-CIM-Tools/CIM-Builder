from dataclasses import dataclass, field

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typing import

import cimbuilder.object_builder as object_builder
import cimbuilder.utils as utils

import logging
_log = logging.getLogger(__name__)

@dataclass()
class SectionalizedBusSubstation:
    connection:ConnectionInterface
    network:GraphModel = field(default=None)
    name:str = field(default='new_sectionalized_bus_sub')
    base_voltage:int|cim.BaseVoltage = field(default=115000)
    total_sections: int = field(default=2)

    def __post_init__(self):
        self.total_sections = int(self.total_sections)
        self.cim = utils.get_cim_profile(self.connection)  # Import CIM profile

        # Create new substation class
        self.substation = self.cim.Substation(mRID=utils.new_mrid(), name=self.name)
       
        # If no network defined, create substation as a DistributedArea
        if not self.network:
            self.network = DistributedArea(connection=self.connection, container=self.substation, distributed=False)
        self.network.add_to_graph(self.substation)
        # If base voltage not defined, create a new BaseVoltage object
        self.base_voltage = utils.get_base_voltage(self.network, self.base_voltage)

        # Create bus sections
        for section in range(self.total_sections):
            bus = self.cim.ConnectivityNode(name=f'{self.name}_bus_{section + 1}', mRID=utils.new_mrid())
            bus.ConnectivityNodeContainer = self.substation
            self.network.add_to_graph(bus)
            object_builder.new_bus_bar_section(self.network, bus)

        for section in range(self.total_sections - 1):
            from_bus = f'{self.name}_bus_{section + 1}'
            to_bus = f'{self.name}_bus_{section + 2}'
            series_number = (section+1)*10
            self.new_bus_tie(from_bus, to_bus, series_number)

        return self.network

    def new_bus_tie(self, from_bus, to_bus, series_number):
        junction1 = cim.ConnectivityNode(name=f'{self.substation.name}_{series_number}_bt_j1', mRID=utils.new_mrid(), ConnectivityNodeContainer=self.substation)
        junction2 = cim.ConnectivityNode(name=f'{self.substation.name}_{series_number}_bt_j2', mRID=utils.new_mrid(), ConnectivityNodeContainer=self.substation)

        bus_tie = object_builder.new_breaker(self.network, self.substation, name=f'{self.name}_bt_{series_number}', node1=junction1, node2=junction2)
        airgap1 = object_builder.new_disconnector(self.network, self.substation, name=f'{self.name}_bt_{series_number + 1}', node1=from_bus, node2=junction1)
        airgap2 = object_builder.new_disconnector(self.network, self.substation, name=f'{self.name}_bt_{series_number + 2}', node1=junction2, node2=to_bus)

        bus_tie.BaseVoltage = self.base_voltage
        airgap1.BaseVoltage = self.base_voltage
        airgap2.BaseVoltage = self.base_voltage

        self.network.add_to_graph(junction1)
        self.network.add_to_graph(junction2)

    def new_branch(self, section_number:int, branch_equipment:cim.ConductingEquipment, branch_terminal:cim.Terminal|int) -> None:
        section_name = f'{self.name}_bus_{section_number}'

        junction1 = cim.ConnectivityNode(name=f'{self.substation.name}_{section_number}_j1', mRID=utils.new_mrid(),
                                         ConnectivityNodeContainer=self.substation)
        junction2 = cim.ConnectivityNode(name=f'{self.substation.name}_{section_number}_j2', mRID=utils.new_mrid(),
                                         ConnectivityNodeContainer=self.substation)
        junction3 = cim.ConnectivityNode(name=f'{self.substation.name}_{section_number}_j3', mRID=utils.new_mrid(),
                                         ConnectivityNodeContainer=self.substation)

        breaker = object_builder.new_breaker(self.network, self.substation, name=f'{self.substation.name}_{10*section_number}', node1=junction1, node2=junction2)
        airgap1 = object_builder.new_disconnector(self.network, self.substation, name=f'{self.substation.name}_{10*section_number+1}', node1=section_name, node2=junction1)
        airgap2 = object_builder.new_disconnector(self.network, self.substation, name=f'{self.substation.name}_{10*section_number+2}', node1=junction2, node2=junction3)

        breaker.BaseVoltage = self.base_voltage
        airgap1.BaseVoltage = self.base_voltage
        airgap2.BaseVoltage = self.base_voltage

        if type(branch_terminal) == cim.Terminal:
            branch_terminal.ConnectivityNode = junction3

        self.network.add_to_graph(junction1)
        self.network.add_to_graph(junction2)
        self.network.add_to_graph(junction3)

    def new_feeder(self, section_number: int, feeder_network: GraphModel, feeder: cim.Feeder,
                   sourcebus: cim.ConnectivityNode = None) -> None:

        feeder_network.get_all_edges(cim.Feeder)
        section_name = f'{self.name}_bus_{section_number}'
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

        junction1 = cim.ConnectivityNode(name=f'{self.substation.name}_{section_number}_j1', mRID=utils.new_mrid(),
                                         ConnectivityNodeContainer=self.substation)
        junction2 = cim.ConnectivityNode(name=f'{self.substation.name}_{section_number}_j2', mRID=utils.new_mrid(),
                                         ConnectivityNodeContainer=self.substation)
        #junction3 = cim.ConnectivityNode(name=f'{self.substation.name}_{section_number}_j3', mRID=utils.new_mrid(),
        #                                 ConnectivityNodeContainer=self.substation)

        breaker = object_builder.new_breaker(self.network, self.substation, name=f'{self.substation.name}_{10*section_number}', node1=junction1, node2=junction2)
        airgap1 = object_builder.new_disconnector(self.network, self.substation, name=f'{self.substation.name}_{10*section_number+1}', node1=section_name, node2=junction1)
        airgap2 = object_builder.new_disconnector(self.network, self.substation, name=f'{self.substation.name}_{10*section_number+2}', node1=junction2, node2=sourcebus)

        breaker.BaseVoltage = self.base_voltage
        airgap1.BaseVoltage = self.base_voltage
        airgap2.BaseVoltage = self.base_voltage

        feeder.NormalEnergizingSubstation = self.substation
        sourcebus.AdditionalEquipmentContainer = self.substation
        self.substation.NormalEnergizedFeeder.append(feeder)

        self.network.add_to_graph(junction1)
        self.network.add_to_graph(junction2)
        self.network.add_to_graph(sourcebus)
        self.network.add_to_graph(feeder)
        
        # feeder_network.add_to_graph(self.substation)