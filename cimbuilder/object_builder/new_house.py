import logging
import math
import requests
import json

from enum import Enum
from cimgraph.models import GraphModel

import cimgraph.data_profile.cimhub_2023 as cim #TODO: cleaner typying import
import cimbuilder.utils as utils

_log = logging.getLogger(__name__)

# RE-WRITE OF CREATEHOUSES.PY FROM CIMHUB, WRITTEN BY THAY838 ON JUN 25, 2018
# UPDATED BY AANDERSN TO USE ENUMS AND CIMGRAPH ON NOV 6, 2024

# Tuning parameter used in guessing how many houses there are per transformer.
# This is a more or less "out of the air" guess at the moment.
VA_PER_SQFT = 3.0

# We need to specify a power factor for the HVAC system. This could use a bit
# more research, here's something that seems reasonable:
HVAC_PF = (0.85, 0.95)


class TYPEHUQ(Enum):
    MOBILE_HOME = 1
    SINGLE_FAMILY_DETACHED = 2
    SINGLE_FAMILY_ATTACHED = 3
    APARTMENT_2_TO_4_UNITS = 4
    APARTMENT_5_OR_MORE_UNITS = 5

    _descriptions = {
        1: 'Mobile home',
        2: 'Single-family detached house',
        3: 'Single-family attached house',
        4: 'Apartment in a building with 2 to 4 units',
        5: 'Apartment in a building with 5 or more units'
    }

    def __str__(self):
        return self._descriptions[self.value]
    
    @classmethod
    def get_description(cls, value):
        return cls._descriptions.get(value, "Unknown value")
    
class CLIMATE_REGION_PUB(Enum):
    MARINE = 1
    COLD_OR_VERY_COLD = 2
    HOT_DRY_OR_MIXED_DRY = 3
    MIXED_HUMID = 4
    HOT_HUMID = 5

    _descriptions = {
        1: 'marine',
        2: 'cold/very cold',
        3: 'hot-dry/mixed-dry',
        4: 'mixed-humid',
        5: 'hot-humid'
    }

    def __str__(self):
        return self._descriptions[self.value]
    
    @classmethod
    def get_description(cls, value):
        return cls._descriptions.get(value, "Unknown value")
    
def estimate_num_houses(housing_data:dict, mag_s:float|cim.ApparentPower, scale:float) -> int:

    meanSqft = [0] * len(housing_data['TYPEHUQ'])

    # Loop over the housing types and compute the mean square footage.
    for housingInd, housingType in enumerate(housing_data['TYPEHUQ'].keys()):
        # Grab bin_edges.
        bin_edges = housing_data[housingType]['TOTSQFT_EN']['bin_edges']
        
        # Bin centers are left edge + half of the distance between bins.
        bin_centers = [
            bin_edges[i] + (bin_edges[i + 1] - bin_edges[i]) / 2
            for i in range(len(bin_edges) - 1)
        ]

        # Mean square footage is the sum of the probabilities times the values.
        pmf = housing_data[housingType]['TOTSQFT_EN']['pmf']
        meanSqft[housingInd] = sum(bin_centers[i] * pmf[i] for i in range(len(bin_centers)))
        
    # Use our (maybe trash) constant to convert square footages to power.
    mean_power = [sqft * VA_PER_SQFT / scale for sqft in meanSqft]

    # Compute the mean power for all housing types.
    total_mean = sum(mean_power[i] * housing_data['TYPEHUQ'][key] for i, key in enumerate(housing_data['TYPEHUQ'].keys()))
    
    # Estimate the number of houses.
    num = mag_s / total_mean
    
    return num

# def est_num_houses(housing_data:dict, load:cim.EnergyConsumer, scale:float) -> int:

    



def new_house(network:GraphModel, load:cim.EnergyConsumer, name: str = None) -> cim.House:
    
    # cim = network.connection.cim
    house_exists = False

    v = load.BaseVoltage.nominalVoltage

    for load_phase in load.EnergyConsumerPhase:
        if 's1' in load_phase.phase.value or 's2' in load_phase.phase.value:

            house = cim.House()
            house.uuid(name = name)

            house.floorArea = 1000

            house.coolingSystem = cim.HouseCooling.electric
            house.coolingSetpoint = 70

            house.heatingSystem = cim.HouseHeating.gas
            house.heatingSetpoint = 70

            house.hvacPowerFactor = 0.95

            house.numberOfStories = 1

            house.thermalIntegrity = cim.HouseThermalIntegrity.aboveNormal


            house.EnergyConsumer = load


            network.add_to_graph(house)








    