import importlib
import json
import logging
import time

from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
from random import Random
from typing import Union
from uuid import UUID

from cimgraph.databases import ConnectionInterface, ConnectionParameters
from cimgraph.databases.blazegraph.blazegraph import BlazegraphConnection
from cimgraph.databases.graphdb.graphdb import GraphDBConnection
from cimgraph.databases.fileparsers.xml_parser import XMLFile
from cimgraph.databases.neo4j.neo4j import Neo4jConnection
from cimgraph.models import BusBranchModel, GraphModel, FeederModel 
import cimgraph.utils as cimUtils

logging.basicConfig(format='%(asctime)s::%(levelname)s::%(name)s::%(filename)s::%(lineno)d::%(message)s',
                    filename='cim_measurement_manager.log',
                    filemode='w',
                    level=logging.INFO,
                    encoding='utf-8')
logger = logging.getLogger(__name__)

cim = None
feederModelmRIDs = {
    "IEEE123.xml": "C1C3E687-6FFD-C753-582B-632A27E28507",
    "IEEE123_PV.xml": "E407CBB6-8C8D-9BC9-589C-AB83FBF0826D",
    "IEEE13.xml": "49AD8E07-3BF9-A4E2-CB8F-C3722F837B62",
    "IEEE13_Assets.xml": "5B816B93-7A5F-B64C-8460-47C17D6E4B0F",
    "IEEE13_OCHRE.xml": "13AD8E07-3BF9-A4E2-CB8F-C3722F837B62",
    "IEEE9500bal.xml": "EE71F6C9-56F0-4167-A14E-7F4C71F10EAA",
    "IEEE8500.xml": "4F76A5F9-271D-9EB8-5E31-AA362D86F2C3",
    "ieee123apps.xml": "F49D1288-9EC6-47DB-8769-57E2B6EDB124",
    # "IEEE37.xml": "49003F52-A359-C2EA-10C4-F4ED3FD368CC", # Fails to load in cimgraph.
    "R2_12_47_2.xml": "9CE150A8-8CC5-A0F9-B67E-BBD8C79D3095",
    "Transactive.xml": "503D6E20-F499-4CC7-8051-971E23D0BF79",
    "ACEP_PSIL.xml": "77966920-E1EC-EE8A-23EE-4EFD23B205BD",
    # "EPRI_DPV_J1.xml": "67AB291F-DCCD-31B7-B499-338206B9828F", # Fails to load in cimgraph.
}

class UuidEncoder(json.JSONEncoder):
    def default(self, obj: object):
        if isinstance(obj, UUID):
            return f"{obj}"
        return json.JSONEncoder.default(self, obj)

class CimMeasurementManager(object):
    def __init__(self, databaseType: str, databaseUrl: str, cimProfile: str, systemModelType: str, 
                 powergridModelsXmlDirectory: Path, uuidFile: Path):
        if not isinstance(databaseType, str):
            raise TypeError("Argument databaseType must be a str type. The provided value is of type "
                            f"{type(databaseType)}")
        if not isinstance(databaseUrl, str):
            raise TypeError("Argument databaseUrl must be a str type. The provided value is of type "
                            f"{type(databaseUrl)}")
        if not isinstance(cimProfile, str):
            raise TypeError(f"Argument cimProfile must be a str type. The provided value is of type {type(cimProfile)}")
        if not isinstance(systemModelType, str):
            raise TypeError("Argument systemModelType must be a str type. The provided value is of type "
                            f"{type(systemModelType)}")
        if not isinstance(powergridModelsXmlDirectory, Path):
            raise TypeError("Argument powergridModelsXmlDirectory must be a Path type. The provided value is of type "
                            f"{type(powergridModelsXmlDirectory)}")
        if not isinstance(uuidFile, Path):
            raise TypeError("Argument uuidFile must be a Path type. The provided value is of type "
                            f"{type(uuidFile)}")
        if databaseType not in ["Blazegraph", "GraphDB", "Neo4j", "xml"]:
            raise ValueError(f"Unsupported database type, {databaseType}, specified! Current supported databases "
                             "are: Blazegraph, GraphDB, Neo4j, or xml.")
        if cimProfile not in ["rc4_2021", "cimhub_2023"]:
            raise ValueError(f"Unsupported cim profile, {cimProfile}, specified! Current supported cim profiles are: "
                             "rc4_2021, or cimhub_2023.")
        if systemModelType not in ["feeder", "busBranch"]:
            raise ValueError(f"Unsupported model type, {systemModelType}, specified! Current supported model types "
                             "are: feeder, or busBranch.")
        global cim
        self.databaseUuids = {}
        self.persistentUuids = []
        self.persistentUuidFile = None
        self.cimProfile = cimProfile
        self.iec61970301 = 7
        if self.cimProfile == 'cimhub_2023':
            self.iec61970301 = 8
        cim = importlib.import_module(f"cimgraph.data_profile.{self.cimProfile}")
        self.dbConnection = self.databaseConnection(databaseType, databaseUrl)
        self.baseXmls = self.loadPowerGridFeederXmlFiles(systemModelType, powergridModelsXmlDirectory)
        self.loadUuidFile(uuidFile)
    
    def databaseConnection(self, dbType: str, dbUrl: str) -> ConnectionInterface:
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
            params = ConnectionParameters(filename=dbUrl, cim_profile="cimhub_2023", iec61970_301=8)
            dbConnection = XMLFile(params)
        return dbConnection
    
    def createGraphModel(self, systemModelType: str, databaseConnection: ConnectionInterface, 
                         containerMrid: str = None) -> GraphModel:
        if not isinstance(systemModelType, str):
            raise TypeError("Argument systemModelType must be a str type. The provided value is of type "
                            f"{type(systemModelType)}")
        if not isinstance(databaseConnection, ConnectionInterface):
            raise TypeError("Argument databaseConnection must be a databaseConnection type. The provided value is of "
                            f"type {type(databaseConnection)}")
        if systemModelType not in ["feeder", "busBranch"]:
            raise ValueError(f"Unsupport system model type, {systemModelType}, specified! Current support system "
                             "model types are: feeder, busBranch, and nodeBreaker.")
        if systemModelType == "feeder":
            feederContainer = cim.Feeder(mRID=containerMrid)
            graphModel = FeederModel(connection=databaseConnection, container=feederContainer, distributed=False)
        elif systemModelType == "busBranch":
            bus_branch_container = cim.ConnectivityNodeContainer(mRID=containerMrid)
            graphModel = BusBranchModel(connection=databaseConnection, container=bus_branch_container,
                                        distributed=False)
        return graphModel
    
    def loadPowerGridFeederXmlFiles(self, modelType: str, xmlDir: Path) -> dict:
        if not isinstance(modelType, str):
            raise TypeError(f"Argument modelType must be a str type. The provided value is of type {type(modelType)}")
        if not isinstance(xmlDir, (str, Path)):
            raise TypeError(f"Argument xmlDir must be a str or Path type. Provided value is {type(xmlDir)}.")
        if modelType not in ["feeder", "busBranch"]:
            raise ValueError(f"Unsupported model type, {modelType}, specified! Current supported model types are: "
                             "feeder, or busBranch.")
        xmlPath = xmlDir.resolve()
        if not xmlPath.is_dir():
            raise ValueError(f"The xml directory provided is not a valid directory! No such directory, {xmlDir}, "
                             "exists.")
        rv = {}
        for child in xmlPath.iterdir():
            if child.is_file() and child.name in feederModelmRIDs.keys():
                rv[child.stem] = {}
                rv[child.stem]["outputDir"] = xmlPath / child.stem
                modelXml = rv[child.stem]["outputDir"] / f"{child.name}"
                if rv[child.stem]["outputDir"].is_dir():
                    for x in rv[child.stem]["outputDir"].iterdir():
                        x.unlink()
                    modelXml.write_text(child.read_text(encoding='utf-8'), encoding='utf-8')
                else:
                    rv[child.stem]["outputDir"].mkdir()
                    modelXml = rv[child.stem]["outputDir"] / f"{child.name}"
                    modelXml.write_text(child.read_text(encoding='utf-8'), encoding='utf-8')
                rv[child.stem]["databaseConnection"] = self.databaseConnection('xml', f"{modelXml}")
                rv[child.stem]["graphModel"] = self.createGraphModel(modelType, rv[child.stem]["databaseConnection"], 
                                                                     feederModelmRIDs.get(child.name))
                cimUtils.get_all_data(rv[child.stem]["graphModel"])
        if not self.persistentUuidFile:
            self.persistentUuidFile = xmlPath / "persistentUuids.json"
        return rv
    
    def loadUuidFile(self, uuidFile: Path):
        if not isinstance(uuidFile, Path):
            raise TypeError("Argument uuidFile must be a Path type. The provided value is of type "
                            f"{type(uuidFile)}")
        if uuidFile.is_file():
            self.persistentUuidFile = uuidFile
            with uuidFile.open(mode="r", encoding="utf-8") as fh:
                self.databaseUuids = json.load(fh)
        for xmlModel in self.baseXmls.keys():
            feederMrid = self.baseXmls[xmlModel]["graphModel"].container.mRID
            if feederMrid not in self.databaseUuids.keys():
                self.databaseUuids[feederMrid] = {}
            for cimClass in self.baseXmls[xmlModel]["graphModel"].graph.keys():
                if cimClass in [cim.Analog, cim.Discrete]:
                    if cimClass.__name__ not in self.databaseUuids[feederMrid].keys():
                        self.databaseUuids[feederMrid][cimClass.__name__] = {}
                    for cimObj in self.baseXmls[xmlModel]["graphModel"].graph[cimClass].values():
                        self.databaseUuids[cimClass.__name__][cimObj.name] = f"{cimObj.identifier}"
        for modelDict in self.databaseUuids.values():
            for cimClassDict in modelDict.values():
                for cimUuid in cimClassDict.values():
                    self.persistentUuids.append(UUID(cimUuid))

    def getUuid(self, feederMrid: str, cimClass: str, name: str) -> UUID:
        rv = None
        objUuid = self.databaseUuids.get(feederMrid).get(cimClass, {}).get(name)
        if objUuid:
            rv = UUID(objUuid)
        else:
            uuidGen = Random(name)
            objUuid = UUID(int=uuidGen.getrandbits(128), version=4)
            while objUuid in self.persistentUuids:
                objUuid = UUID(int=uuidGen.getrandbits(128), version=4)
            rv = objUuid
        return rv        

    def addMeasurement(self, measurementsModel: GraphModel, measurementObject):
        # check to see if measurementObject already exists before adding to graph.
        measurementIsDuplicate = False
        feederMrid = measurementsModel.container.mRID
        if isinstance(measurementObject, cim.Analog):
            for measurement in measurementsModel.graph.get(cim.Analog, {}).values():
                if (
                    measurement.measurementType == measurementObject.measurementType and 
                    measurement.phases == measurementObject.phases and 
                    measurement.PowerSystemResource.identifier == measurementObject.PowerSystemResource.identifier and 
                    measurement.Terminal.identifier == measurementObject.Terminal.identifier
                ):
                    measurementIsDuplicate = True
                    break
                if (
                    not isinstance(measurementObject.PowerSystemResource, 
                                   (cim.EnergyConsumer, cim.LinearShuntCompensator, cim.PowerElectronicsConnection)) and
                    not isinstance(measurement.PowerSystemResource, 
                                   (cim.EnergyConsumer, cim.PowerElectronicsConnection)) and
                    measurementObject.measurementType == "PNV" and
                    measurement.measurementType == measurementObject.measurementType and 
                    measurement.phases == measurementObject.phases and 
                    measurement.Terminal.ConnectivityNode.identifier ==
                        measurementObject.Terminal.ConnectivityNode.identifier
                ):
                    measurementIsDuplicate = True
                    break
        elif isinstance(measurementObject, cim.Discrete):
            for measurement in measurementsModel.graph.get(cim.Discrete, {}).values():
                if (
                    measurement.measurementType == measurementObject.measurementType and 
                    measurement.phases == measurementObject.phases and 
                    measurement.PowerSystemResource.identifier == measurementObject.PowerSystemResource.identifier and 
                    measurement.Terminal.identifier == measurementObject.Terminal.identifier
                ):
                    measurementIsDuplicate = True
                    break
        if not measurementIsDuplicate:
            measurementObject.PowerSystemResource.Measurements.append(measurementObject)
            measurementObject.Terminal.Measurements.append(measurementObject)
            logger.debug(f'Adding {measurementObject.__class__.__name__} for '
                         f'{type(measurementObject.PowerSystemResource).__name__}:'
                         f'{measurementObject.PowerSystemResource.name}')
            measurementsModel.add_to_graph(measurementObject)
            if measurementObject.identifier not in self.persistentUuids:
                self.persistentUuids.append(measurementObject.identifier)
            if type(measurementObject).__name__ not in self.databaseUuids[feederMrid].keys():
                self.databaseUuids[feederMrid][type(measurementObject).__name__] = {}
            if measurementObject.name not in self.databaseUuids[feederMrid][type(measurementObject).__name__].keys():
                self.databaseUuids[feederMrid][type(measurementObject).__name__][measurementObject.name] = \
                    f"{measurementObject.identifier}"
            elif f"{measurementObject.identifier}" != \
                self.databaseUuids[feederMrid][type(measurementObject).__name__][measurementObject.name]:
                logger.error(f"UUID for measurment {measurementObject.name} changed when it shouldn't have!\n"
                             f"new UUID:{measurementObject.identifier}\npersistent UUID: "
                             f"{self.databaseUuids[feederMrid][type(measurementObject).__name__][measurementObject.name]}")
        else:
            logger.debug(f"Duplicate or Redundant measurement.\nType: {measurementObject.measurementType}\nPhases: "
                         f"{measurementObject.phases.value}\nPowerSystemResource class type: "
                         f"{type(measurementObject.PowerSystemResource).__name__}\nPowerSystemResource name: "
                         f"{measurementObject.PowerSystemResource.name}\nConnectivityNode: "
                         f"{measurementObject.Terminal.ConnectivityNode.name}\nis a duplicate of \nType: "
                         f"{measurement.measurementType}\nPhases: "
                         f"{measurement.phases.value}\nPowerSystemResource class type: "
                         f"{type(measurement.PowerSystemResource).__name__}\nPowerSystemResource name: "
                         f"{measurement.PowerSystemResource.name}\nConnectivityNode: "
                         f"{measurement.Terminal.ConnectivityNode.name}")

    def createAnalogMeasurements(self, measurementsModel: GraphModel, cimObject):
        measurementTypes = ["A", "PNV", "VA", "SoC"]
        modelMrid = measurementsModel.container.mRID
        if isinstance(cimObject, cim.ACLineSegment):
            if cimObject.ACLineSegmentPhases:
                for acLineSegmentPhase in cimObject.ACLineSegmentPhases:  # don't add current and SoC measurements for lines
                    if acLineSegmentPhase.phase == cim.SinglePhaseKind.N:
                        continue
                    for measurementType in measurementTypes[1:-1]:
                        for terminal in cimObject.Terminals:
                            if measurementType in ["A", "VA"] and int(terminal.sequenceNumber) != 1:
                                continue
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                            name += f"{terminal.sequenceNumber}_{acLineSegmentPhase.phase.value}"
                            objUuid = self.getUuid(modelMrid, "Analog", name)
                            measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                     mRID = f"{objUuid}",
                                                     name = name, 
                                                     PowerSystemResource = cimObject, 
                                                     Terminal = terminal, 
                                                     phases = cim.PhaseCode(acLineSegmentPhase.phase.value), 
                                                     measurementType = measurementType)
                            self.addMeasurement(measurementsModel, measurement)
            else:
                phases = [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]
                for phase in phases:
                    for measurementType in measurementTypes[1:-1]:
                        for terminal in cimObject.Terminals:
                            if measurementType in ["A", "VA"] and int(terminal.sequenceNumber) != 1:
                                continue
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                            name += f"{terminal.sequenceNumber}_{phase.value}"
                            objUuid = self.getUuid(modelMrid, "Analog", name)
                            measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                     mRID = f"{objUuid}",
                                                     name = name, 
                                                     PowerSystemResource = cimObject, 
                                                     Terminal = terminal, 
                                                     phases = phase, 
                                                     measurementType = measurementType)
                            self.addMeasurement(measurementsModel, measurement)
        elif isinstance(cimObject, cim.Switch) and not isinstance(cimObject, cim.Cut):
            if cimObject.SwitchPhase:
                for switchPhase in cimObject.SwitchPhase:
                    for measurementType in measurementTypes[:-2]:  # dont't add SoC measurements for Switches
                        for terminal in cimObject.Terminals:
                            if measurementType in ["A", "VA"] and int(terminal.sequenceNumber) != 1:
                                continue
                            phase = cim.PhaseCode(getattr(switchPhase, f"phaseSide{terminal.sequenceNumber}").value)
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                            name += f"{terminal.sequenceNumber}_{phase.value}"
                            objUuid = self.getUuid(modelMrid, "Analog", name)
                            measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                     mRID = f"{objUuid}",
                                                     name = name, 
                                                     PowerSystemResource = cimObject, 
                                                     Terminal = terminal, 
                                                     phases = phase, 
                                                     measurementType = measurementType)
                            self.addMeasurement(measurementsModel, measurement)
            else:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for measurementType in measurementTypes[:-2]:  # dont't add SoC measurements for Switches
                        for terminal in cimObject.Terminals:
                            if measurementType in ["A", "VA"] and int(terminal.sequenceNumber) != 1:
                                continue
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                            name += f"{terminal.sequenceNumber}_{phase.value}"
                            objUuid = self.getUuid(modelMrid, "Analog", name)
                            measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                     mRID = f"{objUuid}",
                                                     name = name, 
                                                     PowerSystemResource = cimObject, 
                                                     Terminal = terminal, 
                                                     phases = cim.PhaseCode(phase), 
                                                     measurementType = measurementType)
                            self.addMeasurement(measurementsModel, measurement)
        elif isinstance(cimObject, cim.EnergyConsumer):
            if cimObject.EnergyConsumerPhase:
                for energyConsumerPhase in cimObject.EnergyConsumerPhase:
                    for measurementType in measurementTypes[1:-1]:  # don't add current and SoC measurements for EnergyConsumers
                        for terminal in cimObject.Terminals:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                            name += f"{terminal.sequenceNumber}_{energyConsumerPhase.phase.value}"
                            objUuid = self.getUuid(modelMrid, "Analog", name)
                            measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                     mRID = f"{objUuid}",
                                                     name = name, 
                                                     PowerSystemResource = cimObject, 
                                                     Terminal = terminal, 
                                                     phases = cim.PhaseCode(energyConsumerPhase.phase.value), 
                                                     measurementType = measurementType)
                            self.addMeasurement(measurementsModel, measurement)
            else:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for measurementType in measurementTypes[1:-1]:  # don't add current and SoC measurements for EnergyConsumers
                        for terminal in cimObject.Terminals:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                            name += f"{terminal.sequenceNumber}_{phase.value}"
                            objUuid = self.getUuid(modelMrid, "Analog", name)
                            measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                     mRID = f"{objUuid}",
                                                     name = name, 
                                                     PowerSystemResource = cimObject, 
                                                     Terminal = terminal, 
                                                     phases = phase, 
                                                     measurementType = measurementType)
                            self.addMeasurement(measurementsModel, measurement)                            
        elif isinstance(cimObject, cim.PowerElectronicsConnection):
            for powerElectronicsUnit in cimObject.PowerElectronicsUnit:
                if isinstance(powerElectronicsUnit, cim.PhotovoltaicUnit):
                    if cimObject.PowerElectronicsConnectionPhases:
                        for powerElectronicsConnectionPhase in cimObject.PowerElectronicsConnectionPhases:
                            for measurementType in measurementTypes[1:-1]:  # don't add current and SoC measurements for solar inverters
                                for terminal in cimObject.Terminals:
                                    phase = cim.PhaseCode(powerElectronicsConnectionPhase.phase.value)
                                    name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_" 
                                    name += f"{terminal.sequenceNumber}_{phase.value}"
                                    objUuid = self.getUuid(modelMrid, "Analog", name)
                                    measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                             mRID = f"{objUuid}",
                                                             name = name, 
                                                             PowerSystemResource = cimObject, 
                                                             Terminal = terminal, 
                                                             phases = phase, 
                                                             measurementType = measurementType)
                                    self.addMeasurement(measurementsModel, measurement) 
                    else:
                        for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                            for measurementType in measurementTypes[1:-1]:  # don't add current and SoC measurements for solar inverters
                                for terminal in cimObject.Terminals:
                                    name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                                    name += f"{terminal.sequenceNumber}_{phase.value}"
                                    objUuid = self.getUuid(modelMrid, "Analog", name)
                                    measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                             mRID = f"{objUuid}",
                                                             name = name, 
                                                             PowerSystemResource = cimObject, 
                                                             Terminal = terminal, 
                                                             phases = phase, 
                                                             measurementType = measurementType)
                                    self.addMeasurement(measurementsModel, measurement)
                elif isinstance(powerElectronicsUnit, cim.BatteryUnit):
                    if cimObject.PowerElectronicsConnectionPhases:
                        for powerElectronicsConnectionPhase in cimObject.PowerElectronicsConnectionPhases:
                            for measurementType in measurementTypes[1:-1]:  # don't add current measurements for battery inverters
                                for terminal in cimObject.Terminals:
                                    phase = cim.PhaseCode(powerElectronicsConnectionPhase.phase.value)
                                    name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                                    name += f"{terminal.sequenceNumber}_{phase.value}"
                                    objUuid = self.getUuid(modelMrid, "Analog", name)
                                    measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                             mRID = f"{objUuid}",
                                                             name = name, 
                                                             PowerSystemResource = cimObject, 
                                                             Terminal = terminal, 
                                                             phases = phase, 
                                                             measurementType = measurementType)
                                    self.addMeasurement(measurementsModel, measurement) 
                    else:
                        for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                            for measurementType in measurementTypes[1:-1]:  # don't add current measurements for battery inverters
                                for terminal in cimObject.Terminals:
                                    name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                                    name += f"{terminal.sequenceNumber}_{phase.value}"
                                    objUuid = self.getUuid(modelMrid, "Analog", name)
                                    measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                             mRID = f"{objUuid}",
                                                             name = name, 
                                                             PowerSystemResource = cimObject, 
                                                             Terminal = terminal, 
                                                             phases = phase, 
                                                             measurementType = measurementType)
                                    self.addMeasurement(measurementsModel, measurement) 
                    for terminal in cimObject.Terminals:
                        name = f"{cimObject.__class__.__name__}_{cimObject.name}_SoC"
                        objUuid = self.getUuid(modelMrid, "Analog", name)
                        measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                 mRID = f"{objUuid}",
                                                 name = name, 
                                                 PowerSystemResource = cimObject, 
                                                 Terminal = terminal, 
                                                 phases = cim.PhaseCode.none, 
                                                 measurementType = "SoC")
                        self.addMeasurement(measurementsModel, measurement) 
        elif isinstance(cimObject, cim.SynchronousMachine):
            for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:  # CIM standard for SynchronousMachines assume transmission level so three phase only at this point.
                for measurementType in measurementTypes[1:-1]:  # don't add current and SoC measurements for SynchronousMachine
                    for terminal in cimObject.Terminals:
                        name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                        name += f"{terminal.sequenceNumber}_{phase.value}"
                        objUuid = self.getUuid(modelMrid, "Analog", name)
                        measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                 mRID = f"{objUuid}",
                                                 name = name, 
                                                 PowerSystemResource = cimObject, 
                                                 Terminal = terminal, 
                                                 phases = phase, 
                                                 measurementType = measurementType)
                        self.addMeasurement(measurementsModel, measurement)
        elif isinstance(cimObject, cim.PowerTransformer):
            for transformerTank in cimObject.TransformerTanks:
                for transformerTankEnd in transformerTank.TransformerTankEnds:
                    phases = cim.PhaseCode.none.value
                    if self.cimProfile == "rc4_2021":
                        phases = transformerTankEnd.phases.value
                    elif self.cimProfile == "cimhub_2023":
                        phases = transformerTankEnd.orderedPhases.value
                    for measurementType in measurementTypes[1:-1]:  # don't add current and SoC measurement for Transformers
                        if (
                            (measurementType in ["A", "VA"] and 
                            int(transformerTankEnd.Terminal.sequenceNumber) == 1) or
                            measurementType == "PNV"
                        ):
                            if "A" in phases:
                                name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                                name += f"{transformerTankEnd.Terminal.sequenceNumber}_A"
                                objUuid = self.getUuid(modelMrid, "Analog", name)
                                measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                         mRID = f"{objUuid}",
                                                         name = name, 
                                                         PowerSystemResource = cimObject, 
                                                         Terminal = transformerTankEnd.Terminal, 
                                                         phases = cim.PhaseCode.A, 
                                                         measurementType = measurementType)
                                self.addMeasurement(measurementsModel, measurement)
                            if "B" in phases:
                                name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                                name += f"{transformerTankEnd.Terminal.sequenceNumber}_B"
                                objUuid = self.getUuid(modelMrid, "Analog", name)
                                measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                         mRID = f"{objUuid}",
                                                         name = name, 
                                                         PowerSystemResource = cimObject, 
                                                         Terminal = transformerTankEnd.Terminal, 
                                                         phases = cim.PhaseCode.B, 
                                                         measurementType = measurementType)
                                self.addMeasurement(measurementsModel, measurement)
                            if "C" in phases:
                                name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                                name += f"{transformerTankEnd.Terminal.sequenceNumber}_C"
                                objUuid = self.getUuid(modelMrid, "Analog", name)
                                measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                         mRID = f"{objUuid}",
                                                         name = name, 
                                                         PowerSystemResource = cimObject, 
                                                         Terminal = transformerTankEnd.Terminal, 
                                                         phases = cim.PhaseCode.C, 
                                                         measurementType = measurementType)
                                self.addMeasurement(measurementsModel, measurement)
            for powerTransformerEnd in cimObject.PowerTransformerEnd:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for measurementType in measurementTypes[1:-1]:
                        if (
                            (measurementType in ["A", "VA"] and 
                            int(powerTransformerEnd.Terminal.sequenceNumber) == 1) or
                            measurementType == "PNV"
                        ):
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                            name += f"{powerTransformerEnd.Terminal.sequenceNumber}_{phase.value}"
                            objUuid = self.getUuid(modelMrid, "Analog", name)
                            measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                     mRID = f"{objUuid}",
                                                     name = name, 
                                                     PowerSystemResource = cimObject, 
                                                     Terminal = powerTransformerEnd.Terminal, 
                                                     phases = phase, 
                                                     measurementType = measurementType)
                            self.addMeasurement(measurementsModel, measurement)
        elif isinstance(cimObject, cim.LinearShuntCompensator):
            if cimObject.ShuntCompensatorPhase:
                for shuntCompensatorPhase in cimObject.ShuntCompensatorPhase:
                    phase = cim.PhaseCode(shuntCompensatorPhase.phase.value)
                    for measurementType in measurementTypes[1:-1]:  # don't add current and SoC measurements for SynchronousMachine
                        for terminal in cimObject.Terminals:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                            name += f"{terminal.sequenceNumber}_{phase.value}"
                            objUuid = self.getUuid(modelMrid, "Analog", name)
                            measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                     mRID = f"{objUuid}",
                                                     name = name, 
                                                     PowerSystemResource = cimObject, 
                                                     Terminal = terminal, 
                                                     phases = phase, 
                                                     measurementType = measurementType)
                            self.addMeasurement(measurementsModel, measurement)
            else:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for measurementType in measurementTypes[1:-1]:  # don't add current and SoC measurements for SynchronousMachine
                        for terminal in cimObject.Terminals:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_{measurementType}_"
                            name += f"{terminal.sequenceNumber}_{phase.value}"
                            objUuid = self.getUuid(modelMrid, "Analog", name)
                            measurement = cim.Analog(identifier = deepcopy(objUuid),
                                                     mRID = f"{objUuid}",
                                                     name = name, 
                                                     PowerSystemResource = cimObject, 
                                                     Terminal = terminal, 
                                                     phases = phase, 
                                                     measurementType = measurementType)
                            self.addMeasurement(measurementsModel, measurement)
        else:
            logger.warning(f'cimObject is of an unhandled cim object type. Type: {type(cimObject).__name__}')

    def createDiscreteMeasurements(self, measurementsModel: GraphModel, cimObject):
        modelMrid = measurementsModel.container.mRID
        if isinstance(cimObject, cim.Switch) and not isinstance(cimObject, cim.Cut):
            if cimObject.SwitchPhase:
                for switchPhase in cimObject.SwitchPhase:
                    for terminal in cimObject.Terminals:
                        phase = cim.PhaseCode(getattr(switchPhase, f"phaseSide{terminal.sequenceNumber}").value)
                        if int(terminal.sequenceNumber) == 1:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_Pos_{terminal.sequenceNumber}_"
                            name += f"{phase.value}"
                            objUuid = self.getUuid(modelMrid, "Discrete", name)
                            measurement = cim.Discrete(identifier = deepcopy(objUuid),
                                                       mRID = f"{objUuid}",
                                                       name = name, 
                                                       PowerSystemResource = cimObject, 
                                                       Terminal = terminal, 
                                                       phases = phase, 
                                                       measurementType = "Pos")
                            self.addMeasurement(measurementsModel, measurement)
            else:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for terminal in cimObject.Terminals:
                        if int(terminal.sequenceNumber) == 1:
                            name = f"{cimObject.__class__.__name__}_{cimObject.name}_Pos_{terminal.sequenceNumber}_"
                            name += f"{phase.value}"
                            objUuid = self.getUuid(modelMrid, "Discrete", name)
                            measurement = cim.Discrete(identifier = deepcopy(objUuid),
                                                       mRID = f"{objUuid}",
                                                       name = name, 
                                                       PowerSystemResource = cimObject, 
                                                       Terminal = terminal, 
                                                       phases = phase, 
                                                       measurementType = "Pos")
                            self.addMeasurement(measurementsModel, measurement)
        elif isinstance(cimObject, cim.LinearShuntCompensator):
            if cimObject.ShuntCompensatorPhase:
                for shuntCompensatorPhase in cimObject.ShuntCompensatorPhase:
                    phase = cim.PhaseCode(shuntCompensatorPhase.phase.value)
                    for terminal in cimObject.Terminals:
                        name = f"{cimObject.__class__.__name__}_{cimObject.name}_Pos_{terminal.sequenceNumber}_"
                        name += f"{phase.value}"
                        objUuid = self.getUuid(modelMrid, "Discrete", name)
                        measurement = cim.Discrete(identifier = deepcopy(objUuid),
                                                   mRID = f"{objUuid}",
                                                   name = name, 
                                                   PowerSystemResource = cimObject, 
                                                   Terminal = terminal, 
                                                   phases = phase, 
                                                   measurementType = "Pos")
                        self.addMeasurement(measurementsModel, measurement)
            else:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for terminal in cimObject.Terminals:
                        name = f"{cimObject.__class__.__name__}_{cimObject.name}_Pos_{terminal.sequenceNumber}_"
                        name += f"{phase.value}"
                        objUuid = self.getUuid(modelMrid, "Discrete", name)
                        measurement = cim.Discrete(identifier = deepcopy(objUuid),
                                                   mRID = f"{objUuid}",
                                                   name = name, 
                                                   PowerSystemResource = cimObject, 
                                                   Terminal = terminal, 
                                                   phases = phase, 
                                                   measurementType = "Pos")
                        self.addMeasurement(measurementsModel, measurement)
        elif isinstance(cimObject, cim.PowerTransformer):
            regulatorEnds = []
            for powerTransformerEnd in cimObject.PowerTransformerEnd:
                if powerTransformerEnd.RatioTapChanger:
                    regulatorEnds.append(powerTransformerEnd)
            for transformerTank in cimObject.TransformerTanks:
                for tankEnd in transformerTank.TransformerTankEnds:
                    if tankEnd.RatioTapChanger:
                        regulatorEnds.append(tankEnd)
            for regEnd in regulatorEnds:
                if isinstance(regEnd, cim.PowerTransformerEnd):
                    phases = [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]
                    for phase in phases:
                        name = f"RatioTapChanger_{cimObject.name}_Pos_{regEnd.Terminal.sequenceNumber}_"
                        name += f"{phase.value}"
                        objUuid = self.getUuid(modelMrid, "Discrete", name)
                        measurement = cim.Discrete(identifier = deepcopy(objUuid),
                                                   mRID = f"{objUuid}",
                                                   name = name, 
                                                   PowerSystemResource = cimObject, 
                                                   Terminal = regEnd.Terminal, 
                                                   phases = phase, 
                                                   measurementType = "Pos")
                        self.addMeasurement(measurementsModel, measurement)
                else:
                    if regEnd.orderedPhases not in [cim.OrderedPhaseCodeKind.A, cim.OrderedPhaseCodeKind.AN, 
                                                    cim.OrderedPhaseCodeKind.B, cim.OrderedPhaseCodeKind.BN, 
                                                    cim.OrderedPhaseCodeKind.C, cim.OrderedPhaseCodeKind.CN]:
                        logger.debug(f"non Y configured regulator found!\nPowerTransformer: {cimObject.name}\n"
                                     f"TransformerEnd:{regEnd.name}\nTransformerEndPhase:{regEnd.orderedPhases}")
                    phases = cim.PhaseCode(regEnd.orderedPhases.value.replace("N",""))
                    name = f"RatioTapChanger_{cimObject.name}_Pos_{regEnd.Terminal.sequenceNumber}_"
                    name += f"{phases.value}"
                    objUuid = self.getUuid(modelMrid, "Discrete", name)
                    measurement = cim.Discrete(identifier = deepcopy(objUuid),
                                               mRID = f"{objUuid}",
                                               name = name, 
                                               PowerSystemResource = cimObject, 
                                               Terminal = regEnd.Terminal, 
                                               phases = phases, 
                                               measurementType = "Pos")
                    self.addMeasurement(measurementsModel, measurement)

    def catalogExistingMeasurements(self, graphModel: GraphModel):
        measurementsDict = {'count': 0}
        measurements = {}
        measurements.update(graphModel.graph.get(cim.Analog, {}))
        measurements.update(graphModel.graph.get(cim.Discrete, {}))
        for meas in measurements.values():
            classType = meas.PowerSystemResource.__class__.__name__
            type = meas.measurementType
            if isinstance(meas.PowerSystemResource, cim.PowerTransformer):
                isRegulator = False
                if meas.PowerSystemResource.PowerTransformerEnd:
                    for transformerEnd in meas.PowerSystemResource.PowerTransformerEnd:
                        if transformerEnd.RatioTapChanger:
                            isRegulator = True
                            break
                else:
                    for tank in meas.PowerSystemResource.TransformerTanks:
                        for transformerEnd in tank.TransformerTankEnds:
                            if transformerEnd.RatioTapChanger:
                                isRegulator = True
                                break
                        if isRegulator:
                            break
                if isRegulator:
                    classType = "RatioTapChanger"
            if type not in measurementsDict.keys():
                measurementsDict[type] = {'count': 0}
            if classType not in measurementsDict[type].keys():
                measurementsDict[type][classType] = {'count': 0}
            measurementsDict['count'] += 1
            measurementsDict[type]['count'] += 1
            measurementsDict[type][classType]['count'] += 1
        logger.info(f"Measurements Info:{json.dumps(measurementsDict, indent=4, sort_keys=True)}")     
    
    def populateModelWithMeasurements(self):
        for xmlDict in self.baseXmls.values():
            logger.info(f"Creating measurements for feeder {xmlDict['graphModel'].container.mRID}.")
            measurementsModel = xmlDict["graphModel"]
            for cimClass in [cim.LinearShuntCompensator, cim.EnergyConsumer, cim.SynchronousMachine,
                             cim.PowerElectronicsConnection, cim.PowerTransformer, cim.ACLineSegment,
                             cim.LoadBreakSwitch, cim.Breaker, cim.Recloser]:
                for cimObject in xmlDict["graphModel"].graph.get(cimClass, {}).values():
                    if len(cimObject.Measurements) == 0:
                        self.createAnalogMeasurements(measurementsModel, cimObject)
                        if cimClass in [cim.LinearShuntCompensator, cim.PowerTransformer, cim.LoadBreakSwitch,
                                        cim.Breaker, cim.Recloser]:
                            self.createDiscreteMeasurements(measurementsModel, cimObject)
            self.catalogExistingMeasurements(measurementsModel)
            logger.info(f"Finished creating measurements for feeder {xmlDict['graphModel'].container.mRID}.")

    def exportXmls(self):
        for xmlRootName, xmlDict in self.baseXmls.items():
            xmlFileName = xmlDict["outputDir"] / f"{xmlRootName}.xml"
            cimUtils.write_xml(xmlDict["graphModel"], xmlFileName)
        with self.persistentUuidFile.open(mode="w", encoding="utf-8") as fh:
            json.dump(self.databaseUuids, fh, cls=UuidEncoder, indent=4, sort_keys=True)
            

def main(database: str, databaseUrl: str, cimProfile: str, systemModelType: str, powergridModelsXmlDirectory: str, 
         uuidFile: str):
    t0 = time.time()
    cimMeasurementManager = CimMeasurementManager(database, databaseUrl, cimProfile, systemModelType,
                                                  Path(powergridModelsXmlDirectory), Path(uuidFile))
    t1 = time.time()
    cimMeasurementManager.populateModelWithMeasurements()
    t2 = time.time()
    logger.info(f"Time to initialize all models: {t1 - t0}")
    logger.info(f"Time to add all measurements: {t2 - t1}")
    cimMeasurementManager.exportXmls()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("database", help="The database type to connect to: Blazegraph, GraphDB, Neo4j, or xml.")
    parser.add_argument("database_url", 
                        help="The url of the database to connect to or the full file path of the xml file to use.")
    parser.add_argument("cim_profile", help="The cim profile to use.")
    parser.add_argument("system_model_type", help="The electrical domain model type: feeder, busBranch, nodeBreaker.")
    helpStr = "This should be the directory containing the xml files of the feeders from the PowergridModels "
    helpStr += "repository"
    parser.add_argument("powergrid_models_xml_directory", help=helpStr)
    parser.add_argument("uuid_file", nargs='?', default="persistentUuids.json",
                        help="The json file containing uuids contained in the database")
    args = parser.parse_args()
    main(args.database, args.database_url, args.cim_profile, args.system_model_type,
         args.powergrid_models_xml_directory, args.uuid_file)    
