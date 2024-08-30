import importlib
import json
import logging
import os
from argparse import ArgumentParser

from cimgraph.databases import ConnectionParameters
from cimgraph.databases.blazegraph.blazegraph import BlazegraphConnection
from cimgraph.databases.graphdb.graphdb import GraphDBConnection
from cimgraph.databases.fileparsers.xml_parser import XMLFile
from cimgraph.databases.neo4j.neo4j import Neo4jConnection
from cimgraph.models import FeederModel, BusBranchModel
import cimgraph.utils as cimUtils

logging.basicConfig(format='%(asctime)s::%(levelname)s::%(name)s::%(filename)s::%(lineno)d::%(message)s',
                    filename='cim_measurement_manager.log',
                    filemode='w',
                    level=logging.INFO,
                    encoding='utf-8')
logger = logging.getLogger(__name__)

cim = None

class CimMeasurementManager(object):
    def __init__(self, databaseType: str, databaseUrl: str, cimProfile: str, systemModelType: str, systemModelMrid: str):
            global cim
            self.modelUuids = {}
            self.cimProfile = cimProfile
            self.iec61970301 = 7
            if self.cimProfile == 'cimhub_2023':
                self.iec61970301 = 8
            cim = importlib.import_module(f"cimgraph.data_profile.{self.cimProfile}")
            self.dbConnection = self.databaseConnection(databaseType, databaseUrl)
            self.graphModel = self.createGraphModel(systemModelType, systemModelMrid)
    
    def databaseConnection(self, dbType: str, dbUrl: str) -> object:
        dbConnection = None
        if dbType not in ["Blazegraph", "GraphDB", "Neo4j", "xml"]:
            raise RuntimeError(f"Unsupported database type, {dbType}, specified! Current supported databases are: "
                               "Blazegraph, GraphDB, Neo4j, or xml.")
        if dbType == "Blazegraph":
            params = ConnectionParameters(url=dbUrl, cim_profile=self.cimProfile, iec61970_301=self.iec61970301)
            dbConnection = BlazegraphConnection(params)
        elif dbType == "GraphDB":
            params = ConnectionParameters(url=dbUrl, cim_profile=self.cimProfile, iec61970_301=self.iec61970301)
            dbConnection = GraphDBConnection(params)
        elif dbType == "Neo4j":
            params = ConnectionParameters(url=dbUrl, cim_profile=self.cimProfile, iec61970_301=self.iec61970301)
            dbConnection = Neo4jConnection(params)
        elif dbType == "xml":
            params = ConnectionParameters(filename=dbUrl, cim_profile=self.cimProfile)
            dbConnection = XMLFile(params)
        return dbConnection
    
    def createGraphModel(self, systemModelType: str, containerMrid: str) -> object:
        if systemModelType not in ["feeder", "busBranch"]:
            raise RuntimeError(f"Unsupport system model type, {systemModelType}, specified! Current support system "
                               "model types are: feeder, busBranch, and nodeBreaker.")
        if systemModelType == "feeder":
            feederContainer = cim.Feeder(mRID=containerMrid)
            graphModel = FeederModel(connection=self.dbConnection, container=feederContainer, distributed=False)
        elif systemModelType == "busBranch":
            bus_branch_container = cim.ConnectivityNodeContainer(mRID=containerMrid)
            graphModel = BusBranchModel(connection=self.dbConnection, container=bus_branch_container,
                                             distributed=False)
            cimUtils.get_all_data(graphModel)
        return graphModel
    
    def deleteCurrentMeasurements(self):
        for meas in self.graphModel.graph.get(cim.Analog, {}).values():
            meas.PowerSystemResource.Measurements.remove(meas)
        for meas in self.graphModel.graph.get(cim.Discrete, {}).values():
            meas.PowerSystemResource.Measurements.remove(meas)
        if cim.Analog in self.graphModel.graph.keys():
            del self.graphModel.graph[cim.Analog]
        if cim.Discrete in self.graphModel.graph.keys():
            del self.graphModel.graph[cim.Discrete]

    def addMeasurement(self, measurementObject):
        # check to see if measurementObject already exists before adding to graph.
        measurementIsDuplicate = False
        if isinstance(measurementObject, cim.Analog):
            for measurement in self.graphModel.graph.get(cim.Analog, {}).values():
                if (
                    measurement.measurementType == measurementObject.measurementType and 
                    measurement.phases == measurementObject.phases and 
                    measurement.PowerSystemResource.mRID == measurementObject.PowerSystemResource.mRID and 
                    measurement.Terminal.mRID == measurementObject.Terminal.mRID
                ):
                    measurementIsDuplicate = True
                    break
                if (
                    measurementObject.measurementType == "PNV" and
                    measurement.measurementType == measurementObject.measurementType and
                    measurement.PowerSystemResource.mRID != measurementObject.PowerSystemResource.mRID and
                    measurement.Terminal.ConnectivityNode.mRID == measurementObject.Terminal.ConnectivityNode.mRID
                ):
                    measurementIsDuplicate = True
                    break
        elif isinstance(measurementObject, cim.Discrete):
            for measurement in self.graphModel.graph.get(cim.Discrete, {}).values():
                if (
                    measurement.measurementType == measurementObject.measurementType and 
                    measurement.phases == measurementObject.phases and 
                    measurement.PowerSystemResource.mRID == measurementObject.PowerSystemResource.mRID and 
                    measurement.Terminal.mRID == measurementObject.Terminal.mRID
                ):
                    measurementIsDuplicate = True
                    break
        if not measurementIsDuplicate:
            measurementObject.PowerSystemResource.Measurements.append(measurementObject)
            logger.info(f'Adding {measurementObject.__class__.__name__} for '
                       f'{type(measurementObject.PowerSystemResource).__name__}:'
                       f'{measurementObject.PowerSystemResource.name}')
            self.graphModel.add_to_graph(measurementObject)
        else:
            logger.info(f"Duplicate or Redundant measurement. Type: {measurementObject.measurementType}\nPhases: "
                        f"{measurementObject.phases.value}\nPowerSystemResource class type: "
                        f"{type(measurementObject.PowerSystemResource).__name__}\nPowerSystemResource name: "
                        f"{measurementObject.PowerSystemResource.name}\nConnectivityNode: "
                        f"{measurementObject.Terminal.ConnectivityNode.name}")

    def createAnalogMeasurements(self, cimObject):
        objectInfo = {'PowerSystemResource': json.loads(cimObject.__str__()), 'Terminals': []}
        for terminal in cimObject.Terminals:
            terminalDict = json.loads(terminal.__str__())
            terminalDict['sequenceNumber'] = terminal.sequenceNumber
            objectInfo['Terminals'].append(terminalDict)
        logger.info(f"Adding Analog measurements for {cimObject.__class__.__name__}:{json.dumps(objectInfo, indent=4)}")
        measurementTypes = ["A", "PNV", "VA", "SoC"]
        if isinstance(cimObject, cim.ACLineSegment):
            for acLineSegmentPhase in cimObject.ACLineSegmentPhases:  #don't add current and SoC measurements for lines
                for measurementType in measurementTypes[1:-1]:
                    for terminal in cimObject.Terminals:
                        if measurementType in ["A", "VA"] and int(terminal.sequenceNumber) != 1:
                            continue
                        name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                               f"{terminal.sequenceNumber}_{acLineSegmentPhase.phase.value}"
                        measurement = cim.Analog(name = name,
                                                 measurementType = measurementType,
                                                 phases = cim.PhaseCode(acLineSegmentPhase.phase.value),
                                                 PowerSystemResource = cimObject,
                                                 Terminal = terminal)
                        self.addMeasurement(measurement)
        elif isinstance(cimObject, cim.Switch) and not isinstance(cimObject, cim.Cut):
            if cimObject.SwitchPhase:
                for switchPhase in cimObject.SwitchPhase:
                    for measurementType in measurementTypes[:-2]:  #dont't add power and SoC measurements for Switches
                        for terminal in cimObject.Terminals:
                            if measurementType in ["A", "VA"] and int(terminal.sequenceNumber) != 1:
                                continue
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                   f"{terminal.sequenceNumber}_" \
                                   f"{getattr(switchPhase, 'phaseSide' + str(terminal.sequenceNumber)).value}"
                            measurement = cim.Analog(name = name,
                                                     measurementType = measurementType,
                                                     phases = cim.PhaseCode(
                                                         getattr(switchPhase,
                                                                 f'phaseSide{str(terminal.sequenceNumber)}').value
                                                     ),
                                                     PowerSystemResource = cimObject,
                                                     Terminal = terminal)
                            self.addMeasurement(measurement)
            else:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for measurementType in measurementTypes[:-2]:  #dont't add power and SoC measurements for Switches
                        for terminal in cimObject.Terminals:
                            if measurementType in ["A", "VA"] and int(terminal.sequenceNumber) != 1:
                                continue
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                   f"{terminal.sequenceNumber}_{phase.value}"
                            measurement = cim.Analog(name = name,
                                                     measurementType = measurementType,
                                                     phases = phase,
                                                     PowerSystemResource = cimObject,
                                                     Terminal = terminal)
                            self.addMeasurement(measurement)
        elif isinstance(cimObject, cim.EnergyConsumer):
            if cimObject.EnergyConsumerPhase:
                for energyConsumerPhase in cimObject.EnergyConsumerPhase:
                    for measurementType in measurementTypes[1:-1]:  #don't add current and SoC measurements for EnergyConsumers
                        for terminal in cimObject.Terminals:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                   f"{terminal.sequenceNumber}_{energyConsumerPhase.phase.name}"
                            measurement = cim.Analog(name = name,
                                                     measurementType = measurementType,
                                                     phases = cim.PhaseCode(energyConsumerPhase.phase.value),
                                                     PowerSystemResource = cimObject,
                                                     Terminal = terminal)
                            self.addMeasurement(measurement)
            else:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for measurementType in measurementTypes[1:-1]:  #don't add current and SoC measurements for EnergyConsumers
                        for terminal in cimObject.Terminals:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                   f"{terminal.sequenceNumber}_{phase.value}"
                            measurement = cim.Analog(name = name,
                                                     measurementType = measurementType,
                                                     phases = phase,
                                                     PowerSystemResource = cimObject,
                                                     Terminal = terminal)
                            self.addMeasurement(measurement)
        elif isinstance(cimObject, cim.PowerElectronicsConnection):
            for powerElectronicsUnit in cimObject.PowerElectronicsUnit:
                if isinstance(powerElectronicsUnit, cim.PhotovoltaicUnit):
                    if cimObject.PowerElectronicsConnectionPhases:
                        for powerElectronicsConnectionPhase in cimObject.PowerElectronicsConnectionPhases:
                            for measurementType in measurementTypes[1:-1]:  #don't add current and SoC measurements for solar inverters
                                for terminal in cimObject.Terminals:
                                    name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                           f"{terminal.sequenceNumber}_{powerElectronicsConnectionPhase.phase.value}"
                                    measurement = cim.Analog(name = name,
                                                             measurementType = measurementType,
                                                             phases = cim.PhaseCode(
                                                                 powerElectronicsConnectionPhase.phase.value),
                                                             PowerSystemResource = cimObject,
                                                             Terminal = terminal)
                                    self.addMeasurement(measurement)
                    else:
                        for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                            for measurementType in measurementTypes[1:-1]:  #don't add current and SoC measurements for solar inverters
                                for terminal in cimObject.Terminals:
                                    name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                           f"{terminal.sequenceNumber}_{phase.value}"
                                    measurement = cim.Analog(name = name,
                                                             measurementType = measurementType,
                                                             phases = phase,
                                                             PowerSystemResource = cimObject,
                                                             Terminal = terminal)
                                    self.addMeasurement(measurement)
                elif isinstance(powerElectronicsUnit, cim.BatteryUnit):
                    if cimObject.PowerElectronicsConnectionPhases:
                        for powerElectronicsConnectionPhase in cimObject.PowerElectronicsConnectionPhases:
                            for measurementType in measurementTypes[1:-1]:  #don't add current measurements for battery inverters
                                for terminal in cimObject.Terminals:
                                    name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                           f"{terminal.sequenceNumber}_{powerElectronicsConnectionPhase.phase.name}"
                                    measurement = cim.Analog(name = name,
                                                             measurementType = measurementType,
                                                             phases = cim.PhaseCode(
                                                                 powerElectronicsConnectionPhase.phase.value),
                                                             PowerSystemResource = cimObject,
                                                             Terminal = terminal)
                                    self.addMeasurement(measurement)
                    else:
                        for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                            for measurementType in measurementTypes[1:-1]:  #don't add current measurements for battery inverters
                                for terminal in cimObject.Terminals:
                                    name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                        f"{terminal.sequenceNumber}_{phase.value}"
                                    measurement = cim.Analog(name = name,
                                                             measurementType = measurementType,
                                                             phases = phase,
                                                             PowerSystemResource = cimObject,
                                                             Terminal = terminal)
                                    self.addMeasurement(measurement)
                    for terminal in cimObject.Terminals:
                        name = f"{cimObject.__class__.__name__}_{cimObject.name}_SoC"
                        measurement = cim.Analog(name = name,
                                                 phases = cim.PhaseCode.none,
                                                 PowerSystemResource = cimObject,
                                                 Terminal = terminal)
                        self._addMeasurement(measurement)
        elif isinstance(cimObject, cim.SynchronousMachine):
            for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:  #CIM standard for SynchronousMachines assume transmission level so three phase only at this point.
                for measurementType in measurementTypes[1:-1]:  #don't add current and SoC measurements for SynchronousMachine
                    for terminal in cimObject.Terminals:
                        name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                               f"{terminal.sequenceNumber}_{phase.name}"
                        measurement = cim.Analog(name = name,
                                                 measurementType = measurementType,
                                                 phases = phase,
                                                 PowerSystemResource = cimObject,
                                                 Terminal = terminal)
                        self.addMeasurement(measurement)
        elif isinstance(cimObject, cim.PowerTransformer):
            for transformerTank in cimObject.TransformerTanks:
                for transformerTankEnd in transformerTank.TransformerTankEnds:
                    phases = transformerTankEnd.orderedPhases.value
                    for measurementType in measurementTypes[1:-1]:  #don't add current and SoC measurement for Transformers
                        if (
                            (measurementType in ["A", "VA"] and 
                            int(transformerTankEnd.Terminal.sequenceNumber) == 1) or
                            measurementType == "PNV"
                        ):
                            if "A" in phases:
                                name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                       f"{transformerTankEnd.Terminal.sequenceNumber}_A"
                                measurement = cim.Analog(name = name,
                                                         measurementType = measurementType,
                                                         phases = cim.PhaseCode.A,
                                                         PowerSystemResource = cimObject,
                                                         Terminal= transformerTankEnd.Terminal)
                                self.addMeasurement(measurement)
                            if "B" in phases:
                                name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                       f"{transformerTankEnd.Terminal.sequenceNumber}_B"
                                measurement = cim.Analog(name = name,
                                                         measurementType = measurementType,
                                                         phases = cim.PhaseCode.B,
                                                         PowerSystemResource = cimObject,
                                                         Terminal = transformerTankEnd.Terminal)
                                self.addMeasurement(measurement)
                            if "C" in phases:
                                name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                       f"{transformerTankEnd.Terminal.sequenceNumber}_C"
                                measurement = cim.Analog(name = name,
                                                         measurementType = measurementType,
                                                         phases = cim.PhaseCode.C,
                                                         PowerSystemResource = cimObject,
                                                         Terminal = transformerTankEnd.Terminal)
                                self.addMeasurement(measurement)
            for powerTransformerEnd in cimObject.PowerTransformerEnd:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for measurementType in measurementTypes[1:-1]:
                        if (
                            (measurementType in ["A", "VA"] and 
                            int(powerTransformerEnd.Terminal.sequenceNumber) == 1) or
                            measurementType == "PNV"
                        ):
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                   f"{powerTransformerEnd.Terminal.sequenceNumber}_{phase.value}"
                            measurement = cim.Analog(name = name,
                                                     measurementType = measurementType,
                                                     phases = phase,
                                                     PowerSystemResource = cimObject,
                                                     Terminal = powerTransformerEnd.Terminal)
                            self.addMeasurement(measurement)
        elif isinstance(cimObject, cim.LinearShuntCompensator):
            if cimObject.ShuntCompensatorPhase:
                for shuntCompensatorPhase in cimObject.ShuntCompensatorPhase:
                    phase = cim.PhaseCode(shuntCompensatorPhase.phase.value)
                    for measurementType in measurementTypes[1:-1]:  #don't add current and SoC measurements for SynchronousMachine
                        for terminal in cimObject.Terminals:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                   f"{terminal.sequenceNumber}_{phase.value}"
                            measurement = cim.Analog(name = name,
                                                     measurementType = measurementType,
                                                     phases = phase,
                                                     PowerSystemResource = cimObject,
                                                     Terminal = terminal)
                            self.addMeasurement(measurement)
            else:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for measurementType in measurementTypes[1:-1]:  #don't add current and SoC measurements for SynchronousMachine
                        for terminal in cimObject.Terminals:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" \
                                   f"{terminal.sequenceNumber}_{phase.value}"
                            measurement = cim.Analog(name = name,
                                                     measurementType = measurementType,
                                                     phases = phase,
                                                     PowerSystemResource = cimObject,
                                                     Terminal = terminal)
                            self.addMeasurement(measurement)
        else:
            logger.warn(f'cimObject is of an unhandled cim object type. Type: {type(cimObject).__name__}')

    def createDiscreteMeasurements(self, cimObject):
        if isinstance(cimObject, cim.Switch) and not isinstance(cimObject, cim.Cut):
            if cimObject.SwitchPhase:
                for switchPhase in cimObject.SwitchPhase:
                    for terminal in cimObject.Terminals:
                        if int(terminal.sequenceNumber) == 1:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_Pos_{terminal.sequenceNumber}_" \
                                   f"{getattr(switchPhase,'phaseSide'+str(terminal.sequenceNumber)).value}"
                            measurement = cim.Discrete(name = name,
                                                       measurementType = 'Pos',
                                                       phases = cim.PhaseCode(
                                                           getattr(switchPhase,
                                                           f'phaseSide{str(terminal.sequenceNumber)}').value),
                                                       PowerSystemResource = cimObject,
                                                       Terminal = terminal)
                            self.addMeasurement(measurement)
            else:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for terminal in cimObject.Terminals:
                        if int(terminal.sequenceNumber) == 1:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_Pos_{terminal.sequenceNumber}_" \
                                   f"{phase.value}"
                            measurement = cim.Discrete(name = name,
                                                       measurementType = 'Pos',
                                                       phases = phase,
                                                       PowerSystemResource = cimObject,
                                                       Terminal = terminal)
                            self.addMeasurement(measurement)
        elif isinstance(cimObject, cim.LinearShuntCompensator):
            if cimObject.ShuntCompensatorPhase:
                for shuntCompensatorPhase in cimObject.ShuntCompensatorPhase:
                    phase = cim.PhaseCode(shuntCompensatorPhase.phase.value)
                    for terminal in cimObject.Terminals:
                        name = f"{cimObject.__class__.__name__}_{cimObject.name}_Pos_{terminal.sequenceNumber}_" \
                               f"{phase.value}"
                        measurement = cim.Discrete(name = name,
                                                   measurementType = 'Pos',
                                                   phases = phase,
                                                   PowerSystemResource = cimObject,
                                                   Terminal = terminal)
                        self.addMeasurement(measurement)
            else:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for terminal in cimObject.Terminals:
                        name = f"{cimObject.__class__.__name__}_{cimObject.name}_Pos_{terminal.sequenceNumber}_" \
                               f"{phase.value}"
                        measurement = cim.Discrete(name = name,
                                                   measurementType = 'Pos',
                                                   phases = phase,
                                                   PowerSystemResource = cimObject,
                                                   Terminal = terminal)
                        self.addMeasurement(measurement)
        elif isinstance(cimObject, cim.PowerTransformer):
            isRegulator = False
            for powerTransformerEnd in cimObject.PowerTransformerEnd:
                if powerTransformerEnd.RatioTapChanger is not None:
                    isRegulator = True
                    break
            if isRegulator:
                for powerTransformerEnd in cimObject.PowerTransformerEnd:
                    if int(powerTransformerEnd.Terminal.sequenceNumber) == 1:
                        phases = ['A','B','C']
                        for phase in phases:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_Pos_1_{phase}"
                            measurement = cim.Discrete(name=name,
                                                       measurementType='Pos',
                                                       phases=cim.PhaseCode(phase),
                                                       PowerSystemResource=cimObject,
                                                       Terminal=powerTransformerEnd.Terminal)
                            self.addMeasurement(measurement)
                for transformerTank in cimObject.TransformerTanks:
                    for transformerTankEnd in transformerTank.TransformerTankEnds:
                        if int(transformerTankEnd.Terminal.sequenceNumber) == 1:
                            phases = transformerTankEnd.orderedPhases.value.replace("N","")
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_Pos_1_{phases}"
                            measurement = cim.Discrete(name=name,
                                                       measurementType='Pos',
                                                       phases=cim.PhaseCode(phases),
                                                       PowerSystemResource=cimObject,
                                                       Terminal=transformerTankEnd.Terminal)
                            self.addMeasurement(measurement)
    
    def cleanErroneousMeasurements(self, measurementDict):
        logger.info("Cleaning up duplicate and erroneous measurements.")
        erroneousMeasurements = {'count': 0, 'measurements': []}
        cleanMeasurements = []
        # Flag erroneous measurements first.
        for i in measurementDict.keys():
            measurement = measurementDict[i]
            if (
                isinstance(measurement.PowerSystemResource, cim.PowerTransformer) and
                measurement.measurementType in ["A", "VA"] and
                (measurement.phases in [cim.PhaseCode.s1, cim.PhaseCode.s12, cim.PhaseCode.s12N, 
                                        cim.PhaseCode.s1N, cim.PhaseCode.s2, cim.PhaseCode.s2N] or
                int(measurement.Terminal.sequenceNumber) != 1)
            ):
                logger.info(f"Erroneous measurement found!\nEquipment: {measurement.PowerSystemResource.name}\n"
                            f"Equipment Type: {type(measurement.PowerSystemResource).__name__}\nPhase: "
                            f"{measurement.phases.value}\nMeasurement Type: {measurement.measurementType}\n"
                            f"Terminal: {measurement.Terminal.name}")
                xfmrDict = {'name': measurement.PowerSystemResource.name,
                            'mrid': measurement.PowerSystemResource.mRID,
                            'ends': {}}
                for powerTransformerEnd in measurement.PowerSystemResource.PowerTransformerEnd:
                    xfmrDict['ends'][powerTransformerEnd.mRID] = {'name': powerTransformerEnd.name,
                                                                  'connectivity_node': powerTransformerEnd.Terminal.ConnectivityNode.name,
                                                                  'end_number': int(powerTransformerEnd.endNumber),
                                                                  'terminal_sequence_number': int(powerTransformerEnd.Terminal.sequenceNumber),
                                                                  'terminal_name': powerTransformerEnd.Terminal.name,
                                                                  'phases': 'ABC',
                                                                  'measurement_mrid': measurement.mRID}
                for tank in measurement.PowerSystemResource.TransformerTanks:
                    for transformerEnd in tank.TransformerTankEnds:
                        xfmrDict['ends'][transformerEnd.mRID] = {'name': transformerEnd.name,
                                                                  'connectivity_node': transformerEnd.Terminal.ConnectivityNode.name,
                                                                  'end_number': int(transformerEnd.endNumber),
                                                                  'sequence_number': int(transformerEnd.Terminal.sequenceNumber),
                                                                  'terminal_name': transformerEnd.Terminal.name,
                                                                  'phases': transformerEnd.orderedPhases.value,
                                                                  'measurement_mrid': measurement.mRID}
                logger.info(f'Equipment Details: {json.dumps(xfmrDict, indent=4)}')
                erroneousMeasurements['count'] += 1
                if measurement not in erroneousMeasurements['measurements']:
                    erroneousMeasurements['measurements'].append(measurement)
            else:
                isDuplicateMeasurement = False
                for cleanMeasurement in cleanMeasurements:
                    if (
                        measurement.measurementType in ["A", "VA"] and
                        measurement.measurementType == cleanMeasurement.measurementType and
                        measurement.phases == cleanMeasurement.phases and
                        measurement.PowerSystemResource.mRID == cleanMeasurement.PowerSystemResource.mRID
                    ):
                        isDuplicateMeasurement = True
                        erroneousMeasurements['count'] += 1
                        if measurement not in erroneousMeasurements['measurements']:
                            erroneousMeasurements['measurements'].append(measurement)
                        break
                if not isDuplicateMeasurement and measurement not in cleanMeasurements:
                    cleanMeasurements.append(measurement)
                else:
                    logger.info(f"Duplicate measurement found!\nEquipment: {measurement.PowerSystemResource.name}\n"
                                f"Equipment Type: {type(measurement.PowerSystemResource).__name__}\nPhase: "
                                f"{measurement.phases.value}\nMeasurement Type: {measurement.measurementType}")
        if erroneousMeasurements['count'] > 0:
            logger.info(f'{erroneousMeasurements["count"]} erroneous measurements were found in the model. Removing them.')
        for measurement in erroneousMeasurements['measurements']:
            graphMeasurement = None
            if isinstance(measurement, cim.Analog):
                graphMeasurement = self.graphModel.graph.get(cim.Analog, {}).get(measurement.mRID)
            elif isinstance(measurement, cim.Discrete):
                graphMeasurement = self.graphModel.graph.get(cim.Discrete, {}).get(measurement.mRID)
            if graphMeasurement is not None:
                if len(graphMeasurement.PowerSystemResource.Measurements) > 0:
                    graphMeasurement.PowerSystemResource.Measurements.clear()
                try:
                    del self.graphModel.graph[cim.Analog][measurement.mRID]
                except KeyError:
                    del self.graphModel.graph[cim.Discrete][measurement.mRID]
    
    def populateModelWithMeasurements(self):
        self.deleteCurrentMeasurements()
        for cimClass in [cim.LinearShuntCompensator, cim.EnergyConsumer, cim.SynchronousMachine,
                         cim.PowerElectronicsConnection, cim.PowerTransformer, cim.ACLineSegment, cim.LoadBreakSwitch,
                         cim.Breaker, cim.Recloser]:
            for cimObject in self.graphModel.graph.get(cimClass, {}).values():
                if len(cimObject.Measurements) == 0:
                    self.createAnalogMeasurements(cimObject)
                    if cimClass in [cim.LinearShuntCompensator, cim.PowerTransformer, cim.LoadBreakSwitch,
                                    cim.Breaker, cim.Recloser]:
                        self.createDiscreteMeasurements(cimObject)  

def main(database: str, databaseUrl: str, cimProfile: str, systemModelType: str, systemModelMrid: str,
         exportModelName: str):
    cimMeasurementManager = CimMeasurementManager(database, databaseUrl, cimProfile, systemModelType, systemModelMrid)
    cimMeasurementManager.populateModelWithMeasurements()
    if database == "xml":
        if exportModelName:
            cimUtils.write_xml(cimMeasurementManager.graphModel, exportModelName)
        else:
            raise ValueError("the database selected was xml but no model name was supplied with optional argument "
                             "--export_model_name")
    else:
        if not exportModelName:
            cimMeasurementManager.graphModel.upload()
        else:
            cimUtils.write_xml(cimMeasurementManager.graphModel, exportModelName)
    logger.info(f"Successfully added measurements for model {systemModelMrid}!")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("database", help="The database type to connect to: Blazegraph, GraphDB, or Neo4j.")
    parser.add_argument("database_url", 
                        help="The url of the database to connect to or the full file path of the xml file to use.")
    parser.add_argument("cim_profile", help="The cim profile to use.")
    parser.add_argument("system_model_type", help="The electrical domain model type: feeder, busBranch, nodeBreaker")
    parser.add_argument("system_model_mrid", help="The system model to edit.")
    parser.add_argument("--export_model_name", help="Optional filename to export system_model_mrid to xml file.")
    args = parser.parse_args()
    main(args.database, args.database_url, args.cim_profile, args.system_model_type, args.system_model_mrid,
         args.export_model_name)    