import cimprofiles.cim18.cim18v17 as cim

from cimbuilder.object_builder.line import WireConfigurationBuilder, XYSpacingBuilder


def test_wire_configuration_add_electrical_per_length_impedance(network, container):
    builder = WireConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="wc1")
    pli = cim.PerLengthSequenceImpedance(mRID="pli1")
    network.add_to_graph(pli)

    builder.add_electrical(config, PerLengthImpedance="pli1")
    assert config.PerLengthImpedance is pli


def test_wire_configuration_add_electrical_earth_resistivity_wrong_association_name(
    network, container
):
    """add_electrical's EarthResistivity branch calls
    graph_write.set_assc_from_mrid(self.network, config, CONST,
    'PerLengthImpedance', el_bal.EarthResistivity, EarthResistivity) -
    the association_name string is hardcoded to 'PerLengthImpedance' in
    BOTH branches (copy-paste from the PerLengthImpedance branch above),
    instead of 'EarthResistivity' for this one. Since EarthResistivity
    happens to also match PerLengthImpedance's target_class check at the
    resolve() step (an EarthResistivity object trivially isn't rejected
    because target_class=el_bal.EarthResistivity is correct, only the
    field name is wrong), this does NOT raise - it silently writes the
    EarthResistivity object into config.PerLengthImpedance instead of
    config.EarthResistivity, which is left None."""
    builder = WireConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="wc1")
    er = cim.EarthResistivity(mRID="er1")
    network.add_to_graph(er)

    builder.add_electrical(config, EarthResistivity="er1")

    assert config.EarthResistivity is None
    assert config.PerLengthImpedance is er


def test_wire_configuration_add_construction(network, container):
    builder = WireConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="wc1")
    xy_builder = XYSpacingBuilder(network=network, container=container)
    spacing = xy_builder.create(mRID="xy1")

    builder.add_construction(config, numberOfPhases=3, WireSpacing=spacing.mRID)
    assert config.numberOfPhases == 3
    assert config.WireSpacing is spacing
