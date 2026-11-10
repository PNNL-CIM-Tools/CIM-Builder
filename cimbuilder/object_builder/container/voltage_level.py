import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class VoltageLevelBuilder(ObjectBuilder):
    """
    Builder for the equipment of one nominal voltage inside a substation. Builder functions to be
    called in the following order:
    * create() - instantiate the VoltageLevel, e.g. vl_<substation>_<kV>
    * add_connectivity() - the parent Substation and the BaseVoltage of everything in the level
    """

    cim_class_name = "VoltageLevel"

    def add_connectivity(
        self,
        voltage_level: CN.VoltageLevel,
        *,
        Substation: mRID,
        BaseVoltage: mRID,
    ) -> CN.VoltageLevel:
        """
        * Substation: mRID of the Substation holding the voltage level, e.g. sub_<name>
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=voltage_level,
            profile_part=CN,
            association_name="Substation",
            target_class=cn.Substation,
            target_mRID=Substation,
        )
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=voltage_level,
            profile_part=CN,
            association_name="BaseVoltage",
            target_class=cn.BaseVoltage,
            target_mRID=BaseVoltage,
        )
        return voltage_level


class BayBuilder(ObjectBuilder):
    """
    Builder for the switchgear grouping of one line, transformer or feeder connection.
    Builder functions to be called in the following order:
    * create() - instantiate the Bay, e.g. bay_<name>
    * add_connectivity() - the parent VoltageLevel and the bay's breaker/busbar arrangement
    """

    cim_class_name = "Bay"

    def add_connectivity(
        self,
        bay: CN.Bay,
        *,
        VoltageLevel: mRID,
        breakerConfiguration: str | None = None,
        busBarConfiguration: str | None = None,
    ) -> CN.Bay:
        """
        * VoltageLevel: mRID of the VoltageLevel holding the bay
        * breakerConfiguration: string, singleBreaker|breakerAndAHalf|doubleBreaker|noBreaker
        * busBarConfiguration: string, singleBus|doubleBus|mainWithTransfer|ringBus
        """
        cn: CN = self.cim  # type: ignore
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=bay,
            profile_part=CN,
            association_name="VoltageLevel",
            target_class=cn.VoltageLevel,
            target_mRID=VoltageLevel,
        )
        graph_write.set_attr(
            bay, CN, "breakerConfiguration", self._enum("BreakerConfiguration", breakerConfiguration)
        )
        graph_write.set_attr(
            bay, CN, "busBarConfiguration", self._enum("BusbarConfiguration", busBarConfiguration)
        )
        return bay
