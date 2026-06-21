from __future__ import annotations
from dataclasses import dataclass, field
from cimgraph.models import GraphModel, DistributedArea
from cimgraph.databases import ConnectionInterface
import cimgraph.data_profile.cimhub_2023 as cim  # TODO: cleaner typing import
from cimbuilder.substation_builder.substation_builder import SubstationBuilder
from cimbuilder import object_builder
import cimbuilder.utils as utils
import logging
_log = logging.getLogger(__name__)


@dataclass
class MainAndTransferSubstation(SubstationBuilder):
    """
    Class for building a main-and-transfer bus substation model in node-breaker representation.
    
    This substation topology features a main bus and a transfer bus connected by a bus tie.
    It allows for equipment maintenance without service interruption by transferring
    loads to the transfer bus during maintenance operations.
    
    Attributes:
        connection (ConnectionInterface): Connection interface to the CIM database
        network (GraphModel): Graph model to which the substation will be added
        name (str): Name of the substation
        base_voltage (int | cim.BaseVoltage): Base voltage in volts or a BaseVoltage object
    """
    connection: ConnectionInterface
    network: GraphModel = field(default=None)
    name: str = field(default='new_main_transfer_sub')
    base_voltage: int | cim.BaseVoltage = field(default=115000)
    
    def __post_init__(self):
        """
        Initialize the substation after the instance has been created.
        
        Creates the substation entity, main bus, transfer bus, and bus tie.
        If network is not provided, creates a new distributed area.
        
        Returns:
            GraphModel: The network containing the substation
        """
        cim_module = self.connection.cim
        self.cim:cim = cim_module
        
        # Create new substation class
        self.substation = self.cim.Substation(name=self.name)
        
        # If no network defined, create substation as a DistributedArea
        if not self.network:
            self.network = DistributedArea(connection=self.connection, container=self.substation, distributed=False)
        self.network.add_to_graph(self.substation)
        
        # If base voltage not defined, create a new BaseVoltage object
        self.base_voltage = utils.get_base_voltage(self.network, self.base_voltage)
        
        # Create main bus
        self.main_bus = self.cim.ConnectivityNode(name=f'{self.name}_main_bus')
        self.main_bus.ConnectivityNodeContainer = self.substation
        self.network.add_to_graph(self.main_bus)
        object_builder.new_bus_bar_section(self.network, self.main_bus)
        
        # Create transfer bus
        self.transfer_bus = self.cim.ConnectivityNode(name=f'{self.name}_transfer_bus')
        self.transfer_bus.ConnectivityNodeContainer = self.substation
        self.network.add_to_graph(self.transfer_bus)
        object_builder.new_bus_bar_section(self.network, self.transfer_bus)
        
        # Create bus tie between main and transfer buses
        self.new_bus_tie()
        
        return self.network
    
    def new_bus_tie(self):
        """
        Create a new bus tie between the main bus and transfer bus.
        
        The bus tie consists of two disconnectors and a breaker,
        connected in series with two junction nodes.
        """
        # Create junction nodes for the bus tie
        junction1 = self.cim.ConnectivityNode(name=f'{self.substation.name}_bt_j1',
                                        ConnectivityNodeContainer=self.substation)
        junction2 = self.cim.ConnectivityNode(name=f'{self.substation.name}_bt_j2',
                                        ConnectivityNodeContainer=self.substation)
        
        # Create disconnector from main bus to junction1
        airgap1 = object_builder.new_disconnector(self.network, self.substation, name=f'{self.substation.name}_bt1',
                                                node1=self.main_bus, node2=junction1)
        airgap1.BaseVoltage = self.base_voltage
        
        # Create breaker between junction1 and junction2
        bus_tie = object_builder.new_breaker(self.network, self.substation, name=f'{self.substation.name}_bus_tie',
                                            node1=junction1, node2=junction2)
        bus_tie.BaseVoltage = self.base_voltage
        
        # Create disconnector from junction2 to transfer bus
        airgap2 = object_builder.new_disconnector(self.network, self.substation, name=f'{self.substation.name}_bt1',
                                                node1=junction2, node2=self.transfer_bus)
        airgap2.BaseVoltage = self.base_voltage
        
        # Add junction nodes to graph
        self.network.add_to_graph(junction1)
        self.network.add_to_graph(junction2)
    
    def new_branch(self, breaker_number: int, branch_equipment: cim.ConductingEquipment,
                  branch_terminal: cim.Terminal | int) -> None:
        """
        Create a new branch connection to the substation with the main-and-transfer bus configuration.
        
        The branch connection consists of a breaker and three disconnectors arranged to allow
        the branch to be connected to either the main bus or the transfer bus.
        
        Args:
            breaker_number (int): Identifier number for the branch breaker
            branch_equipment (cim.ConductingEquipment): Branch equipment to be connected
            branch_terminal (cim.Terminal | int): Terminal or terminal index of the branch equipment
        """
        # Create junction nodes for branch connection
        junction1 = self.cim.ConnectivityNode(name=f'{self.substation.name}_{breaker_number}_j1', 
                                        ConnectivityNodeContainer=self.substation)
        junction2 = self.cim.ConnectivityNode(name=f'{self.substation.name}_{breaker_number}_j2',
                                        ConnectivityNodeContainer=self.substation)
        junction3 = self.cim.ConnectivityNode(name=f'{self.substation.name}_{breaker_number}_j3', 
                                        ConnectivityNodeContainer=self.substation)
        
        # Create breaker between junction1 and junction2
        breaker = object_builder.new_breaker(self.network, self.substation,
                                            name=f'{self.substation.name}_{breaker_number}', node1=junction1,
                                            node2=junction2)
        
        # Create disconnector from main bus to junction1
        airgap1 = object_builder.new_disconnector(self.network, self.substation,
                                                name=f'{self.substation.name}_{10*breaker_number + 1}',
                                                node1=self.main_bus, node2=junction1)
        
        # Create disconnector from junction2 to junction3
        airgap2 = object_builder.new_disconnector(self.network, self.substation,
                                                name=f'{self.substation.name}_{10*breaker_number + 2}', 
                                                node1=junction2, node2=junction3)
        
        # Create disconnector from junction3 to transfer bus
        airgap3 = object_builder.new_disconnector(self.network, self.substation,
                                                name=f'{self.substation.name}_{10*breaker_number + 3}',
                                                node1=junction3, node2=self.transfer_bus)
        
        # Set base voltage for all switching equipment
        breaker.BaseVoltage = self.base_voltage
        airgap1.BaseVoltage = self.base_voltage
        airgap2.BaseVoltage = self.base_voltage
        airgap3.BaseVoltage = self.base_voltage
        
        # Connect branch terminal to junction3
        if type(branch_terminal) == self.cim.Terminal:
            branch_terminal.ConnectivityNode = junction3
        elif type(branch_terminal) == int:
            branch_terminal = branch_equipment.Terminals[branch_terminal]
            branch_terminal.ConnectivityNode = junction3
        
        # Add junction nodes to graph
        self.network.add_to_graph(junction1)
        self.network.add_to_graph(junction2)
        self.network.add_to_graph(junction3)
    
    def new_feeder(self, series_number: int, feeder_network: GraphModel, feeder: cim.Feeder,
                  sourcebus: cim.ConnectivityNode = None) -> None:
        """
        Connect a new feeder to the substation with the main-and-transfer bus configuration.
        
        The feeder connection includes a breaker and disconnectors to allow for
        connection to either the main bus or transfer bus.
        
        Args:
            series_number (int): Identifier number for the feeder connection
            feeder_network (GraphModel): Graph model containing the feeder
            feeder (cim.Feeder): Feeder object to be connected
            sourcebus (cim.ConnectivityNode, optional): Source bus for the feeder. If None,
                                                       attempts to find a node named 'sourcebus'
        """
        feeder_network.get_all_edges(self.cim.Feeder)
        
        # If sourcebus of feeder not specified, look for something named sourcebus
        if not sourcebus:
            found = False
            feeder_network.get_all_edges(self.cim.EnergySource)
            feeder_network.get_all_edges(self.cim.Terminal)
            feeder_network.get_all_edges(self.cim.ConnectivityNode)
            for source in feeder_network.graph[self.cim.EnergySource].values():
                if source.Terminals[0].ConnectivityNode.name == 'sourcebus':
                    sourcebus = source.Terminals[0].ConnectivityNode
                    found = True
            if not found:
                _log.error(f'Could not find sourcebus for {feeder.name}')
        
        # Create junction nodes for feeder connection
        junction1 = self.cim.ConnectivityNode(name=f'{self.substation.name}_{10*series_number}_j1', 
                                        ConnectivityNodeContainer=self.substation)
        junction2 = self.cim.ConnectivityNode(name=f'{self.substation.name}_{10*series_number}_j2', 
                                        ConnectivityNodeContainer=self.substation)

        # Create breaker between junction1 and junction2
        breaker = object_builder.new_breaker(self.network, self.substation,
                                            name=f'{self.substation.name}_{10*series_number}', node1=junction1,
                                            node2=junction2)
        
        # Create disconnector from main bus to junction1
        airgap1 = object_builder.new_disconnector(self.network, self.substation,
                                                name=f'{self.substation.name}_{10*series_number + 1}',
                                                node1=self.main_bus, node2=junction1)
        
        # Create disconnector from junction2 to sourcebus
        airgap2 = object_builder.new_disconnector(self.network, self.substation,
                                                name=f'{self.substation.name}_{10*series_number + 2}',
                                                node1=junction2, node2=sourcebus)
        
        # Create disconnector from sourcebus to transfer bus (normally open)
        airgap3 = object_builder.new_disconnector(self.network, self.substation,
                                                name=f'{self.substation.name}_{10*series_number + 3}', 
                                                node1=sourcebus, node2=self.transfer_bus)
        
        # Set base voltage for all switching equipment
        breaker.BaseVoltage = self.base_voltage
        airgap1.BaseVoltage = self.base_voltage
        airgap2.BaseVoltage = self.base_voltage
        airgap3.BaseVoltage = self.base_voltage
        
        # Configure transfer bus disconnector as normally open
        airgap3.open = True
        airgap3.normalOpen = True
        
        # Set up feeder-substation relationship
        feeder.NormalEnergizingSubstation = self.substation
        self.substation.NormalEnergizedFeeder.append(feeder)
        
        # Add nodes to graph
        self.network.add_to_graph(junction1)
        self.network.add_to_graph(junction2)
        self.network.add_to_graph(sourcebus)
        self.network.add_to_graph(feeder)