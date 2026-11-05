from abc import ABC, abstractmethod

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimgraph.models import GraphModel
from cimtables import Qty, connectivity, graph_write

mRID = str 

class SubstationBuilder(ABC):
    def __init__(self, network: GraphModel):
        self.network = network
        self.cim = network.cim

    def create(
        self,
        *,
        mRID: str | None = None,
        name: str | None = None,
        description: str | None = None,
        Region: mRID | None = None,
    ) -> CN.Substation:
        """
        Add a new object to the network graph
        * mRID: string identifier, unique to the local model
        * name: human-readable name of substation
        * identifier: seed string for persistent UUIDs for classes without name/mRID.
        * description: free form comment text to describe object
        Returns the new, unadded object."""

        cn:CN = self.cim #type:ignore

        substation = cn.Substation(name=name, mRID=mRID, description=description)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=substation,
            profile_part=CN,
            association_name="Region",
            target_class=cn.SubGeographicalRegion,
            target_mRID=Region,
        )
        graph_write.add_to_graph(self.network, substation)

        return substation

    def add_voltage_level(
            self,
            substation:CN.Substation,
            *,
            BaseVoltage: mRID

    )

    @abstractmethod
    def new_branch(self):
        raise RuntimeError("Must have implemented connect in inherited class")

    @abstractmethod
    def new_shunt(self):
        raise RuntimeError("Must have implemented connect in inherited class")

    @abstractmethod
    def new_feeder(self):
        raise RuntimeError("Must have implemented connect in inherited class")
