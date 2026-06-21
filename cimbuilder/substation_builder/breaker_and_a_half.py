from __future__ import annotations
from dataclasses import dataclass, field

from cimgraph.models import GraphModel, DistributedArea

import cimgraph.data_profile.cimhub_2023 as cim  # TODO: cleaner typing import

from cimbuilder.substation_builder.substation_builder import SubstationBuilder
from cimbuilder import object_builder
import cimbuilder.utils as utils

import logging
_log = logging.getLogger(__name__)


@dataclass()
class BreakerAndHalfSubstation(SubstationBuilder):

    name: str = field(default='new_breaker_and_half_bus_sub')
    base_voltage: int | cim.BaseVoltage = field(default=115000)
    total_bus_ties: int = field(default=2)

    def __post_init__(self):
        """
        Initialize the BreakerAndHalfSubstation instance, creating the substation structure and
        components if not already defined.
        """
        cim_module = self.connection.cim
        self.cim = cim_module

        # Create new substation class
        self.substation = self.cim.Substation(name=self.name)

        # If no network defined, create substation as a DistributedArea
        if not self.network:
            self.network = DistributedArea(connection=self.connection, container=self.substation, distributed=False)
        self.network.add_to_graph(self.substation)
        
        # If base voltage not defined, create a new BaseVoltage object
        self.base_voltage = utils.get_base_voltage(self.network, self.base_voltage)

        # Create the first main bus
        self.main_bus_1 = self.cim.ConnectivityNode(name=f'{self.name}_main_bus_1')
        self.main_bus_1.ConnectivityNodeContainer = self.substation
        self.network.add_to_graph(self.main_bus_1)
        object_builder.new_bus_bar_section(self.network, self.main_bus_1)

        # Create the second main bus
        self.main_bus_2 = self.cim.ConnectivityNode(name=f'{self.name}_main_bus_2')
        self.main_bus_2.ConnectivityNodeContainer = self.substation
        self.network.add_to_graph(self.main_bus_2)
        object_builder.new_bus_bar_section(self.network, self.main_bus_2)

        # Create bus ties
        for tie in range(self.total_bus_ties):
            self.new_bus_tie(tie)

        return self.network

    def new_bus_tie(self, tie_number):

        number_of_junctions = 8
        junctions = []

        # Create connective nodes (junctions) for the bus tie
        for i in range(number_of_junctions):
            junctions.append(self.cim.ConnectivityNode(name=f'{self.substation.name}_{tie_number}_bt_j{i + 1}',
                                                  ConnectivityNodeContainer=self.substation))

        tie_number = 10 * tie_number

        # Create the first bus-tie arrangement
        bus_tie_1 = object_builder.new_breaker(self.network, self.substation, name=f'{self.name}_bt_{tie_number}',
                                               node1=junctions[0], node2=junctions[1])
        airgap1 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{10 + tie_number + 1}', node1=self.main_bus_1,
                                                  node2=junctions[0])
        airgap2 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{10 + tie_number + 2}', node1=junctions[1],
                                                  node2=junctions[2])
        # Create the second bus-tie arrangement
        bus_tie_2 = object_builder.new_breaker(self.network, self.substation,
                                               name=f'{self.name}_bt_{2 * tie_number}',
                                               node1=junctions[3], node2=junctions[4])
        airgap3 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{20 + tie_number + 1}',
                                                  node1=junctions[2], node2=junctions[3])
        airgap4 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{20 + tie_number + 2}',
                                                  node1=junctions[4], node2=junctions[5])
        # Create the third bus-tie arrangement
        bus_tie_3 = object_builder.new_breaker(self.network, self.substation,
                                               name=f'{self.name}_bt_{3 * tie_number}',
                                               node1=junctions[6], node2=junctions[7])
        airgap5 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{30 + tie_number + 1}',
                                                  node1=junctions[5], node2=junctions[6])
        airgap6 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{30 + tie_number + 2}',
                                                  node1=junctions[7], node2=self.main_bus_2)

        # Set the base voltage for all elements
        bus_tie_1.BaseVoltage = self.base_voltage
        bus_tie_2.BaseVoltage = self.base_voltage
        bus_tie_3.BaseVoltage = self.base_voltage

        airgap1.BaseVoltage = self.base_voltage
        airgap2.BaseVoltage = self.base_voltage
        airgap3.BaseVoltage = self.base_voltage
        airgap4.BaseVoltage = self.base_voltage
        airgap5.BaseVoltage = self.base_voltage
        airgap6.BaseVoltage = self.base_voltage

        # Add all junctions to the network graph
        for junction in junctions:
            self.network.add_to_graph(junction)

    def new_branch(self, breaker_number: int, tie_number: int, branch_equipment: cim.ConductingEquipment, branch_terminal: cim.Terminal | int) -> None:

        # Determine the junction connection point based on the branch number
        if breaker_number % 2 == 0:
            jcn_name = f'{self.substation.name}_{tie_number}_bt_j{6}'
            jcn_num = 2
        else:
            jcn_name = f'{self.substation.name}_{tie_number}_bt_j{3}'
            jcn_num = 1

        junction1 = self.cim.ConnectivityNode(name=f'{self.substation.name}_{breaker_number}_j{jcn_num}',
                                         ConnectivityNodeContainer=self.substation)
        
        airgap1 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.substation.name}_{10 * breaker_number}', node1=jcn_name,
                                                  node2=junction1)
        airgap1.BaseVoltage = self.base_voltage

        # Set branch terminal connectivity node
        branch_terminal.ConnectivityNode = junction1

        self.network.add_to_graph(junction1)

    def new_feeder(self, breaker_number: int, tie_number: int, feeder_network: GraphModel, feeder: cim.Feeder,
                   sourcebus: cim.ConnectivityNode = None) -> None:

        # Determine the junction connection point based on the branch number
        if breaker_number % 2 == 0:
            jcn_name = f'{self.substation.name}_{tie_number}_bt_j{6}'
            jcn_num = 2
        else:
            jcn_name = f'{self.substation.name}_{tie_number}_bt_j{3}'
            jcn_num = 1

        feeder_network.get_all_edges(cim.Feeder)

        # If sourcebus of feeder not specified, look for something named sourcebus
        if not sourcebus:
            found = False
            feeder_network.get_all_edges(self.cim.EnergySource)
            feeder_network.get_all_edges(self.cim.Terminal)
            feeder_network.get_all_edges(self.cim.ConnectivityNode)
            # Check if the feeder network has a source bus
            if feeder.NormalHeadTerminal is not None:
                sourcebus = feeder.NormalHeadTerminal.ConnectivityNode
                found = True
            else:
                # Search for a source bus in the feeder network
                for source in feeder_network.graph.get(self.cim.EnergySource,{}).values():
                    if source.Terminals[0].ConnectivityNode.name == 'sourcebus':
                        sourcebus = source.Terminals[0].ConnectivityNode
                        found = True
            if not found:
                _log.error(f'Could not find sourcebus for {feeder.name}')

        airgap1 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.substation.name}_{10 * breaker_number}',
                                                  node1=jcn_name, node2=sourcebus)
        airgap1.BaseVoltage = self.base_voltage

        feeder.NormalEnergizingSubstation = self.substation

        self.network.add_to_graph(sourcebus)
        self.network.add_to_graph(feeder)
        feeder_network.add_to_graph(self.substation)
        self.substation.NormalEnergizedFeeder.append(feeder)