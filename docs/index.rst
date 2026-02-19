.. CIM-Builder

================================================
CIM-Builder Documentation
================================================

CIM-Builder is a new python library developed by Pacific Northwest National Laboratory for creating CIM models "from scratch" with no pre-existing model files. This is a significantly different capability than all other tooling, which requires a source file from which to start, such as OpenDSS, PSSE, or GIS data. The library currently inlcudes three main functionalities:

* automatic creation of new node-breaker substations in CIM based on interactive API calls.
* automatic insertion of existing distribution feeders in CIM into new node-breaker substations.
* automatic insertion of new aggregate feeder data in existing CIM transmission models.


.. toctree::
   :caption: Overview
   :maxdepth: 2

   01_overview/1_1_overview
   01_overview/1_2_installation
   01_overview/1_3_structure
   01_overview/1_4_contributing

.. toctree::
   :caption: Object Builder
   :maxdepth: 2

   02_object_builder/2_1_object_builder
   02_object_builder/2_2_one_terminal_object
   02_object_builder/2_3_two_terminal_object
   
.. toctree::
   :caption: Substation Builder
   :maxdepth: 2

   03_substation_builder/3_1_single_bus
   03_substation_builder/3_2_sectionalized_bus
   

