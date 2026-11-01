from abc import ABC
from typing import TYPE_CHECKING, Optional, cast

from cimgraph.models import GraphModel
from cimtables import graph_write, impedance
from cimtables.binder import bind_row

if TYPE_CHECKING:
    from cimprofiles.cim18 import cim18v17

class ObjectBuilder(ABC):
    cim_class_name: str  # set by subclass, e.g. 'EnergyConsumer'

    def __init__(self, network: GraphModel, container: object):
        self.network = network
        self.container = cast(cim18v17.EquipmentContainer, container)
        self.cim = network.cim
        # self.cim = cast("cim18v17", network.cim)

    def create(self, *, mRID: Optional[str] = None, name: Optional[str] = None, identifier: Optional[str] = None) -> object:
        """
        Add a new object to the network graph
        * mRID: string identifier, unique to the local model
        * name: human-readable name, not required to be unique
        * identifier: seed string for persistent UUIDs for classes without name/mRID.

        Returns the new, unadded object."""
        cim_cls = getattr(self.network.cim, self.cim_class_name)
        
        if issubclass(cim_cls, self.cim.IdentifiedObject):
            new_object = cim_cls(name=name, mRID=mRID)
        else:
            new_object = cim_cls()
            new_object.uuid(mRID=identifier)
            
        self.network.add_to_graph(new_object)
        return new_object

