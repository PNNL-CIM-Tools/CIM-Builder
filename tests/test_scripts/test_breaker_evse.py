# Import transmission and distribution modeling classes
from cimgraph.models import FeederModel
from cimgraph.databases import  XMLFile
from cimgraph import utils
import uuid
import cimgraph.data_profile.cimhub_2023 as cim
from cimbuilder.object_builder import new_EVSE, new_EVSE_BU, new_EVSE_BV, new_EVSE_PEC, new_EVSE_PEU 

import os
os.environ['CIMG_CIM_PROFILE'] = 'cimhub_2023'
cim_profile = 'cimhub_2023'

# Import 13 bus model from XML file
ieee13_feeder = cim.Feeder(mRID =  str(uuid.uuid4()))
file = XMLFile(filename='/Users/vuth095/CIM-Builder/tests/test_models/IEEE13.xml') # path to your local IEEE 13 bus model XML file
ieee13_network = FeederModel(container=ieee13_feeder, connection=file)

# create Node to add EVSE objects
feeder_node = '650z'  # example node name from the IEEE 13 bus model

# create EVSE objects and connect to feeder_node
EVSE = new_EVSE.new_EVSE(ieee13_network, container=ieee13_feeder, name= 'evse', node = feeder_node, chargingMode = "charging") 
EVSE_BV = new_EVSE_BV.new_EVSE_BV(ieee13_network, container=ieee13_feeder, name='evse_bv', node = feeder_node, kV = 0.12)
EVSE_PEC = new_EVSE_PEC.new_EVSE_PEC(ieee13_network, container=ieee13_feeder, name='evse_pec', node = feeder_node, kW = 1.9)
EVSE_PEU = new_EVSE_PEU.new_EVSE_PEU(ieee13_network, container=ieee13_feeder, name='evse_peu', node = feeder_node, kWrated = 2.4)
EVSE_BU = new_EVSE_BU.new_EVSE_BU(ieee13_network, container=ieee13_feeder, name='evse_bu', node = feeder_node, kWhrated = 13.5, chargingMode = "charging")

# verify EVSE object were created
print("#####################################################")
print("EVSE Object:")
print(EVSE.__dict__)

print("#####################################################")

# verify EVSE objects were added to the network
print("Feeder Network with EVSE:")
print(ieee13_network)

