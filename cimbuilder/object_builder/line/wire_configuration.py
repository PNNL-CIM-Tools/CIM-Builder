import cimprofiles.cim18.cim18v17.asset_deployment as AD
import cimprofiles.cim18.cim18v17.construction as CONST
import cimprofiles.cim18.cim18v17.electrical_unbalanced as EL_UNBAL
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class WireConfigurationBuilder(ObjectBuilder):
    """
    Builder for line geometry templates (equivalent to OpenDSS LineGeometry). Builder functions to be called in the following order:
    * create() - instantiate the WireConfiguration, number of phases and the WireSpacing (built with XYSpacingBuilder or ConductorDistanceSpacingBuilder)
    * add_wire_sequence_configuration() - one wire per conductor, in conductor order
    * add_electrical() - optional, the calculated PerLengthImpedance and the EarthResistivity
    """

    cim_class_name = "WireConfiguration"

    def create(
        self,
        *,
        mRID: str | None = None,
        name: str | None = None,
        identifier: str | None = None,
        description: str | None = None,
        numberOfPhases: int | None = None,
        WireSpacing: mRID | None = None,
    ) -> CONST.WireConfiguration:
        """
        * numberOfPhases: number of phases within the circuit group
        * WireSpacing: mRID string of an existing wire spacing
        """
        const: CONST = self.cim  # type: ignore
        config: CONST.WireConfiguration = super().create(
            mRID=mRID, name=name, identifier=identifier, description=description
        )  # type: ignore
        graph_write.set_attr(config, CONST, "numberOfPhases", numberOfPhases)
        if WireSpacing is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=config,
                profile_part=CONST,
                association_name="WireSpacing",
                target_class=const.WireSpacing,
                target_mRID=WireSpacing,
            )
        return config

    def add_electrical(
        self,
        config: EL_UNBAL.WireConfiguration,
        *,
        PerLengthImpedance: mRID | None = None,
        EarthResistivity: mRID | None = None,
    ) -> EL_UNBAL.WireConfiguration:
        """
        * PerLengthImpedance: mRID string of a PerLengthSequenceImpedance or PerLengthPhaseImpedance
        * EarthResistivity: mRID string of the EarthResistivity of all lines using this template
        """
        el_unbal: EL_UNBAL = self.cim  # type: ignore
        if PerLengthImpedance is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=config,
                profile_part=EL_UNBAL,
                association_name="PerLengthImpedance",
                target_class=el_unbal.PerLengthImpedance,
                target_mRID=PerLengthImpedance,
            )
        if EarthResistivity is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=config,
                profile_part=EL_UNBAL,
                association_name="EarthResistivity",
                target_class=el_unbal.EarthResistivity,
                target_mRID=EarthResistivity,
            )
        return config

    def add_wire_sequence_configuration(
        self,
        config: CONST.WireConfiguration,
        *,
        sequenceNumber: int,
        WireInfo: mRID,
    ) -> tuple[CONST.WireConfiguration, CONST.WireSequenceConfiguration]:
        """
        Adds the wire of one conductor
        * sequenceNumber: integer, conductor number, matches the XYConductorPosition and ACLineSegmentPhase sequenceNumber
        * WireInfo: mRID of the OverheadWireInfo or cable info of this conductor
        """
        const: CONST = self.cim  # type: ignore
        wire_sequence = const.WireSequenceConfiguration(mRID=f"{config.mRID}_{sequenceNumber}")
        graph_write.set_attr(wire_sequence, CONST, "sequenceNumber", sequenceNumber)
        graph_write.set_assc(wire_sequence, CONST, "WireConfiguration", config)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=wire_sequence,
            profile_part=AD,
            association_name="WireInfo",
            target_class=const.WireInfo,
            target_mRID=WireInfo,
        )
        graph_write.add_to_graph(self.network, wire_sequence)
        return config, wire_sequence
