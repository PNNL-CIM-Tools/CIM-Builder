import opendssdirect as dss
import os
import logging
import uuid

_log = logging.getLogger(__name__)

class DSStoCIM():
    def __init__(self):
        pass

    def convert_file(self, file_path:str = None, master_file:str = "convert.dss", feeder_mrid:str = None,
                     sub_name:str = "Substation", sub_geo:str = "SubGeoRegion", geo:str = "GeoRegion", uuids_file:str = None):
        if file_path is not None:
            os.chdir(file_path)
        if feeder_mrid is None:
            feeder_mrid = str(uuid.uuid4())

        if not os.path.isfile(master_file):
            for dirpath, subdirs, files in os.walk(file_path):
                for filename in files:
                    if filename == "Master.dss":
                        master_file = f"{dirpath}/{master_file}"

        try:
            # Compile OpenDSS Master File
            dss.run_command("Clear")
            dss.run_command(f"Redirect {master_file}")
            dss.run_command(f"Redirect {master_file}")
            dss.Solution.Solve()
            # Import persistent mRIDs if specified
            if uuids_file is not None:
                dss.run_command(f"uuids file = {uuids_file}")
            # Convert to CIM XML
            dss.run_command(f"export cim100 fid={feeder_mrid} substation={sub_name} subgeo={sub_geo} geo={geo} file=Master.xml")
        except:
            _log.warning(f"unable to compile master file {master_file}")

    

    def convert_directory(self, path, master):
        pass

