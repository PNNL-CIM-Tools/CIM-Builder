# CIM-Builder

CIM-Builder is a new python library developed under the Grid Atlas and MAPLE LEAF projects for creating CIM models "from scratch" with no pre-existing model files. This is a significantly different capability than all other tooling, which requires a source file from which to start, such as OpenDSS, PSSE, or GIS data. The library currently inlcudes three main functionalities:

1) automatic creation of new node-breaker substations in CIM based on interactive API calls.

2) automatic insertion of existing distribution feeders in CIM into new node-breaker substations.

3) automatic insertion of new aggregate feeder data in existing CIM transmission models.

The library contains a set of classes for each type of common substation, which each contain two methods. The first is `add_feeder`, which automatically adds the specified distribution feeder to the substation and creates the chain of switching equipment between the sourcebus of the feeder and the correct breaker or airgap switch in the substation. The second is `add_branch`, which enables automated addition of transmission branches, transformers, and shunt equipment to the substation bus.

The classes supported within the first version of CIM-Builder are

* `SingleBusSubstation`
* `MainAndTransferSubstation`
* `RingBusSubstation`
* `DoubleBusSingleBreakerSubstation`
* `BreakerAndHalfSubstation`

When instantiated, these classes create a new CIMantic Graphs `DistributedArea` or `NodeBreakerModel` graph model with all CIM objects associated with the default bus configuration for that substation. Distribution feeders can then be added to the substation by instantiating each feeder as a new CIMantic Graphs `FeederModel`. The python library then builds the set of CIM associations to map the feeder to the substation and create all CIM objects for the breaker, airgap switches, and junctions.



## Attribution and Disclaimer

This software was created under a project sponsored by the U.S. Department of Energy’s Office of Electricity, an agency of the United States Government.  Neither the United States Government nor the United States Department of Energy, nor Battelle, nor any of their employees, nor any jurisdiction or organization that has cooperated in the development of these materials, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe privately owned rights.

Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof, or Battelle Memorial Institute. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

PACIFIC NORTHWEST NATIONAL LABORATORY
operated by
BATTELLE
for the
UNITED STATES DEPARTMENT OF ENERGY
under Contract DE-AC05-76RL01830
