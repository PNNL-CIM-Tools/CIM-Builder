from cimbuilder.object_builder.line.wire_info import WireInfoBuilder


class OverheadWireInfoBuilder(WireInfoBuilder):
    """
    Builder for bare overhead conductors (equivalent to OpenDSS WireData). Builder functions to be called in the following order:
    * create() - instantiate the OverheadWireInfo, e.g. wire_<name>
    * add_asset_info() - conductor geometry, resistances and ratings
    """

    cim_class_name = "OverheadWireInfo"
