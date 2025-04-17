import os
import unittest
from uuid import UUID

import cimgraph.data_profile.cimhub_2023 as cim
from cimgraph.models import GraphModel utils as cimg_utils
from cimgraph.databases import BlazegraphConnection, RDFlibConnection
from cimgraph.models import FeederModel, NodeBreakerModel
from cimgraph.queries import sparql

from cimbuilder.substation_builder import SingleBusSubstation


class TestBlazegraphSETO(unittest.TestCase):

    def setUp(self):

        # Set environment variables for testing
        os.environ['CIMG_CIM_PROFILE'] = 'cimhub_2023'
        os.environ['CIMG_URL'] = 'http://localhost:8889/bigdata/namespace/kb/sparql'
        os.environ['CIMG_NAMESPACE'] = 'http://iec.ch/TC57/CIM100#'
        os.environ['CIMG_IEC61970_301'] = '8'
        os.environ['CIMG_USE_UNITS'] = 'false'

        self.feeder_13 = '49AD8E07-3BF9-A4E2-CB8F-C3722F837B62'
        self.feeder_13assets = '49AD8E07-3BF9-A4E2-CB8F-C3722F837B62'

    def tearDown(self):
        # Restore environment variables
        for key, value in self.original_env.items():
            if value is not None:
                os.environ[key] = value
            else:
                os.environ.pop(key, None)