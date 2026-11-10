from abc import ABC

import cimprofiles.cim18.cim18v17.asset_deployment as AD
import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimgraph.models import GraphModel
from cimtables import graph_write
from cimtables.binder import bind_row

mRID = str


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
        * identifier: seed string for persistent UUIDs, only for classes without name/mRID
        * description: free form comment text to describe object
        Returns the new object, already added to the graph."""
        cim_cls = getattr(self.network.cim, self.cim_class_name)

        if issubclass(cim_cls, self.cim.IdentifiedObject):
            if identifier is not None:
                raise ValueError(
                    f"{self.cim_class_name} is an IdentifiedObject: pass mRID, not identifier"
                )
            new_object = cim_cls(name=name, mRID=mRID, description=description)
        else:
            if mRID is not None or name is not None:
                raise ValueError(
                    f"{self.cim_class_name} has no mRID or name: pass identifier instead"
                )
            new_object = cim_cls()
            new_object.uuid(mRID=identifier)

        graph_write.add_to_graph(self.network, new_object)
        return new_object

    def _enum(self, enum_name: str, value: str | None):
        """The merged-profile enum member for a string value (set_attr rejects strings), None stays None"""
        if value is None:
            return None
        return getattr(self.cim, enum_name)(value)

    def add_asset_datasheet(
        self, obj: AD.PowerSystemResource, *, AssetDatasheet: mRID
    ) -> AD.PowerSystemResource:
        """
        Links a PowerSystemResource instance to its catalog AssetInfo (e.g. wire_556500_26_7,
        inv_catalog_1), so the instance's physical data comes from the catalog entry.
        AssetDatasheet is only sliced onto PowerSystemResource in the asset_deployment part, not
        onto every concrete subclass, so this writes both sides directly rather than through
        graph_write.set_assc (which looks up the field by the object's own, often-unsliced, class).
        * AssetDatasheet: mRID of the AssetInfo (or subclass) catalog entry
        """
        ad: AD = self.cim  # type: ignore
        info = graph_write.resolve(self.network, ad.AssetInfo, AssetDatasheet)
        if info is None:
            raise ValueError(
                f"{getattr(obj, 'mRID', obj)!r}: AssetDatasheet {AssetDatasheet!r} not found in graph "
                f"(build it before the object that references it)"
            )
        obj.AssetDatasheet = info
        if obj not in info.PowerSystemResources:
            info.PowerSystemResources.append(obj)
        return obj

    def from_table(self, row: object) -> object:
        """
        DSL/bulk entry point, binds a validated <Class>Row onto a
        freshly create()'d object via the generic, reflective bind_row

        * row: an already-validated `<Class>Row` dataclass instance (not a
          dict or raw CIM object) - bind_row reflects over its fields to
          populate the built object, including unit conversion for any Qty
          fields and FK resolution for any mRID-reference fields.

        Returns the object already added to the graph (bind_row's own
        contract, matching bind_row's direct callers) - unlike the direct
        create()/add_<part>()/add() API, do not call .add() again on the
        result. No `obj` is passed in: bind_row builds it itself (mRID,
        else identifier, else a random UUID) since a row is keyed by mRID
        """
        return bind_row(self.network, row, container=self.container)