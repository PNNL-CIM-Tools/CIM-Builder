# Import transmission and distribution modeling classes
from cimgraph.models import FeederModel, NodeBreakerModel
from cimgraph.databases import ConnectionParameters, RDFlibConnection, BlazegraphConnection
import cimgraph.utils as utils
import uuid

import importlib
from cimbuilder.substation_builder import BreakerAndHalfSubstation
import cimbuilder.object_builder as builder
import os
os.environ['CIMG_CIM_PROFILE'] = 'cimhub_2023'

cim_profile = 'cimhub_2023'
cim = importlib.import_module('cimgraph.data_profile.' + cim_profile)

params = ConnectionParameters(filename=None, cim_profile=cim_profile, iec61970_301=8)
connection = RDFlibConnection(params)
SubBuilder = BreakerAndHalfSubstation(connection=connection, name="breaker_and_half_sub", base_voltage = 115000)
substation = SubBuilder.substation
print(substation)

# Import 13 bus model from XML file
ieee13_feeder = cim.Feeder(mRID = '49AD8E07-3BF9-A4E2-CB8F-C3722F837B62')
params = ConnectionParameters(filename='/Users/vuth095/CIM-Builder/tests/test_models/IEEE13.xml', cim_profile=cim_profile, iec61970_301=8)
connection = RDFlibConnection(params)
ieee13_network = FeederModel(connection=connection, container=ieee13_feeder, distributed=False)

assets13_feeder = cim.Feeder(mRID = '5B816B93-7A5F-B64C-8460-47C17D6E4B0F')
params = ConnectionParameters(filename='/Users/vuth095/CIM-Builder/tests/test_models/IEEE13_Assets.xml', cim_profile=cim_profile, iec61970_301=8)
connection = RDFlibConnection(params)
assets13_network = FeederModel(connection=connection, container=assets13_feeder, distributed=False)

SubBuilder.new_feeder(breaker_number = 10, feeder=ieee13_feeder, feeder_network=ieee13_network, tie_number=2)
SubBuilder.new_feeder(breaker_number = 20, feeder=assets13_feeder, feeder_network=assets13_network, tie_number=2)
SubBuilder.network.pprint(cim.Substation)
SubBuilder.network.pprint(cim.Feeder)

utils.write_xml(SubBuilder.network, '../test_output/test_main_and_transfer.xml')

# create Node to add EVSE objects
# we may need to change this to a specific bus in the future if we want to run power flow.
# This can be do by getting the bus name and mRID from the xml file
# feeder_node = cim.ConnectivityNode(name=f'{assets13_feeder}_1', mRID=utils.new_mrid())
feeder_node = cim.ConnectivityNode(name=f'{assets13_feeder}_1', mRID=str(uuid.uuid4()))
feeder_node.ConnectivityNodeContainer = assets13_feeder
SubBuilder.network.add_to_graph(feeder_node)

 # create EVSE objects
    
EVSE = builder.new_EVSE(SubBuilder.network, container=assets13_feeder, name=f'{assets13_feeder}_evse', node = feeder_node, chargingMode = "charging") 
SubBuilder.network.add_to_graph(EVSE)

EVSE_BV = builder.new_EVSE_BV(SubBuilder.network, container=assets13_feeder, name=f'{assets13_feeder}_evse_bv', node = feeder_node, kV = 0.12)
SubBuilder.network.add_to_graph(EVSE_BV)

EVSE_PEC = builder.new_EVSE_PEC(SubBuilder.network, container=assets13_feeder, name=f'{assets13_feeder}_evse_pec', node = feeder_node, kW = 1.9)
SubBuilder.network.add_to_graph(EVSE_PEC)

EVSE_PEU = builder.new_EVSE_PEU(SubBuilder.network, container=assets13_feeder, name=f'{assets13_feeder}_evse_peu', node = feeder_node, kWrated = 2.4)
SubBuilder.network.add_to_graph(EVSE_PEU)

EVSE_BU = builder.new_EVSE_BU(SubBuilder.network, container=assets13_feeder, name=f'{assets13_feeder}_evse_bu', node = feeder_node, kWhrated = 13.5, chargingMode = "charging")
SubBuilder.network.add_to_graph(EVSE_BU) 

utils.write_xml(SubBuilder.network, '../test_output/breaker_and_half_with_evse.xml')