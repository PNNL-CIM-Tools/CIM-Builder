from dataclasses import dataclass, field

from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface
import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typing import

import cimbuilder.object_builder as object_builder
import cimbuilder.utils as utils

import logging
_log = logging.getLogger(__name__)

@dataclass()
class BreakerAndHalfSubstation:
    connection:ConnectionInterface
    network:GraphModel = field(default=None)
    name:str = field(default='new_breaker_and_half_bus_sub')
    base_voltage:int|cim.BaseVoltage = field(default=115000)
    total_bus_ties:int = field(default=2)

    def __post_init__(self):
        self.cim = utils.get_cim_profile(self.connection)  # Import CIM profile

        # Create new substation class
        self.substation = self.cim.Substation(mRID=utils.new_mrid(), name=self.name)

        # If no network defined, create substation as a DistributedArea
        if not self.network:
            self.network = DistributedArea(connection=self.connection, container=self.substation, distributed=False)
        self.network.add_to_graph(self.substation)
        # If base voltage not defined, create a new BaseVoltage object
        self.base_voltage = utils.get_base_voltage(self.network, self.base_voltage)

        # first main bus
        self.main_bus_1 = self.cim.ConnectivityNode(name=f'{self.name}_main_bus_1', mRID=utils.new_mrid())
        self.main_bus_1.ConnectivityNodeContainer = self.substation
        self.network.add_to_graph(self.main_bus_1)
        object_builder.new_bus_bar_section(self.network, self.main_bus_1)

        # second main bus
        self.main_bus_2 = self.cim.ConnectivityNode(name=f'{self.name}_main_bus_2', mRID=utils.new_mrid())
        self.main_bus_2.ConnectivityNodeContainer = self.substation
        self.network.add_to_graph(self.main_bus_2)
        object_builder.new_bus_bar_section(self.network, self.main_bus_2)

        # Create bus ties
        for tie in range(self.total_bus_ties):
            # if tie == 0:
            #     tie_number = 0
            # else:
            #     tie_number = 3*tie + 1
            self.new_bus_tie(tie)#_number)

        return self.network

    def new_bus_tie(self, tie_number):
        number_of_junctions = 8
        junctions = []

        for i in range(number_of_junctions):
            junctions.append(cim.ConnectivityNode(name=f'{self.substation.name}_{tie_number}_bt_j{i + 1}',
                                                mRID=utils.new_mrid(), ConnectivityNodeContainer=self.substation))

        tie_number = 10*tie_number

        # There are three bus tie arrangements
        # Each bus tie arrangement consists of 3 bus-tie breakers
        # and two air gap switches on each side of each bus-tie breaker

        # first bus-tie arrangement
        bus_tie_1 = object_builder.new_breaker(self.network, self.substation, name=f'{self.name}_bt_{tie_number}',
                                               node1=junctions[0], node2=junctions[1])
        airgap1 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{10+tie_number + 1}', node1=self.main_bus_1,
                                                  node2=junctions[0])
        airgap2 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{10+tie_number + 2}', node1=junctions[1],
                                                  node2=junctions[2])
        # second bus-tie arrangement
        bus_tie_2 = object_builder.new_breaker(self.network, self.substation, name=f'{self.name}_bt_{2*tie_number}',
                                               node1=junctions[3], node2=junctions[4])
        airgap3 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{20+tie_number + 1}', node1=junctions[2],
                                                  node2=junctions[3])
        airgap4 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{20+tie_number + 2}', node1=junctions[4],
                                                  node2=junctions[5])
        # third bus-tie arrangement
        bus_tie_3 = object_builder.new_breaker(self.network, self.substation, name=f'{self.name}_bt_{3*tie_number}',
                                               node1=junctions[6], node2=junctions[7])
        airgap5 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{30+tie_number + 1}', node1=junctions[5],
                                                  node2=junctions[6])
        airgap6 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.name}_bt_{30+tie_number + 2}', node1=junctions[7],
                                                  node2=self.main_bus_2)

        bus_tie_1.BaseVoltage = self.base_voltage
        bus_tie_2.BaseVoltage = self.base_voltage
        bus_tie_3.BaseVoltage = self.base_voltage

        airgap1.BaseVoltage = self.base_voltage
        airgap2.BaseVoltage = self.base_voltage
        airgap3.BaseVoltage = self.base_voltage
        airgap4.BaseVoltage = self.base_voltage
        airgap5.BaseVoltage = self.base_voltage
        airgap6.BaseVoltage = self.base_voltage

        for junction in junctions:
            self.network.add_to_graph(junction)

    def new_branch(self, branch_number:int, tie_number:int, branch_equipment:cim.ConductingEquipment, branch_terminal:cim.Terminal|int) -> None:
        # Odd numbered-branches will connect to junction 3 on the
        # specified tie number while even numbers on junction 6

        if branch_number % 2 == 0:
            jcn_name = f'{self.substation.name}_{tie_number}_bt_j{6}'
            jcn_num = 2
        else:
            jcn_name = f'{self.substation.name}_{tie_number}_bt_j{3}'
            jcn_num = 1

        junction1 = cim.ConnectivityNode(name=f'{self.substation.name}_{branch_number}_j{jcn_num}',
                                         mRID=utils.new_mrid(),
                                         ConnectivityNodeContainer=self.substation)
        airgap1 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.substation.name}_{10 * branch_number}', node1=jcn_name,
                                                  node2=junction1)
        airgap1.BaseVoltage = self.base_voltage

        branch_terminal.ConnectivityNode = junction1

        self.network.add_to_graph(junction1)

    def new_feeder(self, branch_number: int, tie_number: int, feeder_network: GraphModel, feeder: cim.Feeder,
                   sourcebus: cim.ConnectivityNode = None) -> None:

        # if feeder_number % 2 == 0:
        #     node_name = f'{self.substation.name}_{branch_number}_j2'
        # else:
        #     node_name = f'{self.substation.name}_{branch_number}_j1'


        if branch_number % 2 == 0:
            jcn_name = f'{self.substation.name}_{tie_number}_bt_j{6}'
            jcn_num = 2
        else:
            jcn_name = f'{self.substation.name}_{tie_number}_bt_j{3}'
            jcn_num = 1

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

        airgap1 = object_builder.new_disconnector(self.network, self.substation,
                                                  name=f'{self.substation.name}_{10 * branch_number}',
                                                  node1=jcn_name, node2=sourcebus)
        airgap1.BaseVoltage = self.base_voltage

        feeder.NormalEnergizingSubstation = self.substation
        sourcebus.AdditionalEquipmentContainer = self.substation

        self.network.add_to_graph(sourcebus)
        self.network.add_to_graph(feeder)
        feeder_network.add_to_graph(self.substation)
        self.substation.NormalEnergizedFeeder.append(feeder)
