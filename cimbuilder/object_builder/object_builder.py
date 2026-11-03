from abc import ABC

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimgraph.models import GraphModel


class ObjectBuilder(ABC):
    cim_class_name: str  # set by subclass, e.g. 'EnergyConsumer'

    def __init__(self, network: GraphModel, container: CN.EquipmentContainer):
        self.network = network
        self.container = container
        self.cim = network.cim
        # self.cim = cast("cim18v17", network.cim)

    def create(
        self,
        *,
        mRID: str | None = None,
        name: str | None = None,
        identifier: str | None = None,
        description: str | None = None,
    ) -> object:
        """
        Add a new object to the network graph
        * mRID: string identifier, unique to the local model
        * name: human-readable name, not required to be unique
        * identifier: seed string for persistent UUIDs for classes without name/mRID.
        * description: free form comment text to describe object
        Returns the new, unadded object."""
        cim_cls = getattr(self.network.cim, self.cim_class_name)

        if issubclass(cim_cls, self.cim.IdentifiedObject):
            new_object = cim_cls(name=name, mRID=mRID, description=description)
        else:
            new_object = cim_cls()
            new_object.uuid(mRID=identifier)

        self.network.add_to_graph(new_object)
        return new_object
